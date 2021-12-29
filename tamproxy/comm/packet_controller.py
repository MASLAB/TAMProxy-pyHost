from serial import SerialException
from multiprocessing import Process, Pipe, Event
from collections import namedtuple
from time import sleep, time
from struct import pack, unpack
import numpy as np
import logging
import signal

from .. import config as c
from .tamp_serial import *

logger = logging.getLogger('tamproxy.controller')

class PacketController(Process):

    # Constants
    WINDOW_SIZE =           c.host.window_size
    ENABLE_TIMEOUT =        c.host.enable_timeout
    INITIAL_TIMEOUT =       c.host.initial_timeout
    SRTT_ALPHA =            c.host.srtt_alpha
    RTTDEV_ALPHA =          c.host.rttdev_alpha
    SRTT_GAIN =             c.host.srtt_gain
    RTTDEV_GAIN =           c.host.rttdev_gain
    SERIAL_RETRIES =        c.host.serial_retries
    SERIAL_RETRY_TIMEOUT =  c.host.serial_retry_timeout
    PACK_FORMAT =           c.host.pack_format
    UNPACK_FORMAT =         c.host.unpack_format
    RESET_MSG =             c.host.reset_msg
    START_BYTE =            c.packet.start_byte
    DEVICELIST_CODE =       c.devices.devicelist.code
    HELLO_PAYLOAD =         c.devices.devicelist.hello_code

    compare_pids = lambda self, a,b: np.int16(b - a)

    def __init__(self):
        self._stop = Event()
        self._continuous = Event()
        self.tserial = None
        self.packet_parser = None
        self.pipe_inside, self.pipe_outside = Pipe()
        self.continuous_requests = set()
        self.weighted_tdma_list = []
        self.reset()
        super(PacketController, self).__init__()

    def reset(self, clear_pipe=False):
        self.rtt_smoothed = None
        self.rtt_deviation = None
        self.timeout = self.INITIAL_TIMEOUT
        self.en_route = dict()          # pid -> packet, time_sent
        self.receiving_buffer = dict()  # pid -> sent_packet, payload
        self.next_send_pid = np.uint16(0)
        self.next_recv_pid = np.uint16(0)
        self.weighted_tdma_pos = 0
        self.packets_received = 0
        if clear_pipe:
            while self.pipe_inside.poll():
                self.pipe_inside.recv()

    def connect(self):
        self.reset(True)
        raw_hello_packet = self.encode_raw_packet(0, self.DEVICELIST_CODE,
                                              self.HELLO_PAYLOAD)
        hello_response_length = len(raw_hello_packet) - 1
        self.tserial = TAMPSerial(raw_hello_packet, hello_response_length)
        self.packet_parser = PacketParser(self.tserial)
        self.pipe_inside.send((None, self.RESET_MSG))

    def encode_raw_packet(self, pid, dest, payload):
        pack_format = self.PACK_FORMAT.format(len(payload))
        length = len(payload) + 5
        payload = payload.encode()
        result = pack(pack_format, self.START_BYTE, pid, length, dest, payload)
        return result

    def set_continuous_enabled(self, bool):
        if bool: 
            self._continuous.set()
            logger.info("Enabled continuous requests")
        else:
            self._continuous.clear()
            logger.info("Disabled continuous requests")

    def get_new_packet_to_send(self):
        # process new requests
        while self.pipe_inside.poll():
            packet_request = PacketRequest(*self.pipe_inside.recv())
            if packet_request.is_continuous:
                if not packet_request.remove_continuous:
                    self.continuous_requests.add(packet_request[:2])
                    self.weighted_tdma_list += (
                        [packet_request[:2]] * packet_request.weight)
                else: 
                    self.continuous_requests.discard(packet_request[:2])
            else:
                return packet_request[:2]

        # resend exiting continuous_requests
        while self.weighted_tdma_list and self._continuous.is_set():
            key = self.weighted_tdma_list[self.weighted_tdma_pos]
            if key in self.continuous_requests:
                self.weighted_tdma_pos += 1
                self.weighted_tdma_pos %= len(self.weighted_tdma_list)
                return key
            else:
                # this item was removed
                self.weighted_tdma_list.pop(self.weighted_tdma_pos)
                if self.weighted_tdma_list:
                    self.weighted_tdma_pos += 1
                    self.weighted_tdma_pos %= len(self.weighted_tdma_list)

        # nothing else to do
        return None

    def slide_window(self):
        if self.ENABLE_TIMEOUT:
            # resend all en_route packets that have timed out
            for pid in self.en_route:
                packet, time_sent = self.en_route[pid]
                dt = time() - time_sent
                if dt > self.timeout:
                    logger.debug("Packet timed out, will retransmit: "
                        "pid={}, packet={}, timeout={}"
                        .format(pid, packet, self.timeout)
                    )
                    self.en_route[pid] = (packet, time())
                    self.transmit(pid, *packet[:2])
                    return

        # transmit the next packet
        if len(self.en_route) < self.WINDOW_SIZE:
            packet = self.get_new_packet_to_send()
            if packet:
                new_pid = self.next_send_pid
                self.en_route[new_pid] = (packet, time())
                self.transmit(new_pid, *packet)
                self.next_send_pid += np.uint16(1)

    def decode_raw_packet(self, raw_packet):
        payload_length = len(raw_packet) - 4
        unpack_format = self.UNPACK_FORMAT.format(payload_length)
        start_byte, pid, length, payload = unpack(unpack_format, raw_packet)
        return (np.uint16(pid), payload)

    def transmit(self, pid, dest, payload):
        if self.tserial.out_waiting > 50:
            self.tserial.flush()
        raw_packet = self.encode_raw_packet(pid, dest, payload)
        self.tserial.write(raw_packet)

    def receive(self):
        raw_packets = self.packet_parser.receive()
        packets = [self.decode_raw_packet(p) for p in raw_packets]
        for pid, payload in packets:
            if payload != self.HELLO_PAYLOAD:
                self.process_packet(pid, payload)
        return len(packets)

    def process_packet(self, pid, payload):
        self.packets_received += 1
        if pid not in self.en_route:
            logger.debug("Retransmitted packet received: pid={}, payload={}"
                            .format(pid,payload))
            return
        sent_packet, time_sent = self.en_route.pop(pid)
        if self.ENABLE_TIMEOUT:
            self.update_timeout(time_sent)
            if self.next_recv_pid == pid:
                self.pipe_inside.send((sent_packet, payload))
                i = 1
                while pid + i in self.receiving_buffer:
                    self.pipe_inside.send(self.receiving_buffer.pop(pid + i))
                    i += 1
                self.next_recv_pid = pid + np.uint16(i)
            elif self.compare_pids(self.next_recv_pid, pid) > 0:
                self.receiving_buffer[pid] = (sent_packet, payload)
        else: self.pipe_inside.send((sent_packet, payload))

    def update_timeout(self, time_sent):
        """
        Update the timeout value to use for future packets, by combining the
        smoothed round trip time, and the deviation in the round trip time
        """
        rtt = time() - time_sent

        if self.rtt_smoothed:
            self.rtt_smoothed = rtt*self.SRTT_ALPHA + (1-self.SRTT_ALPHA)*self.rtt_smoothed
        else:
            self.rtt_smoothed = rtt

        if self.rtt_deviation:
            self.rtt_deviation = (abs(rtt-self.rtt_smoothed)*self.RTTDEV_ALPHA
                           + (1-self.RTTDEV_ALPHA)*self.rtt_deviation)
        else:
            self.rtt_deviation = rtt

        self.timeout = self.SRTT_GAIN*self.rtt_smoothed + self.RTTDEV_GAIN*self.rtt_deviation

    def stop(self):
        logger.info('stop requested')
        self._stop.set()

    def run(self):
        # keyboard interrupt is handled by the main process
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        i = self.SERIAL_RETRIES
        while i >= 0:
            try:
                logger.info('Connecting to the teensy')
                self.connect()
                logger.info('Connected!')
                i = self.SERIAL_RETRIES
                while True:
                    self.slide_window()
                    self.receive()
                    if (self._stop.is_set()
                            and not self.pipe_inside.poll()
                            and not self.en_route):
                        logger.info('stopped')
                        return
            except (IOError, SerialException,
                    SerialPortUnavailableException) as e:
                logger.error(e)
                i -= 1
                if i == 0:
                    logger.critical('Giving up, hit maximum serial retries')
                    return
                else:
                    logger.warn("Retrying connection in 1 second, "
                                "{} tries left".format(i))
                    sleep(self.SERIAL_RETRY_TIMEOUT)
                    continue
            except SerialPortEstablishException as e:
                logger.critical('Giving up - could not establish a connection')
                return

class PacketParser(object):

    MAX_PACKET_SIZE =   c.packet.max_size
    MIN_PACKET_SIZE =   c.packet.min_response_size
    START_BYTE =        c.packet.start_byte.to_bytes(1, 'big')

    def __init__(self, tserial):
        self.tserial = tserial
        self.receive_buffer = bytearray()
        self.error_flag = False
        self.receive_length = self.MAX_PACKET_SIZE
        self.raw_packets = []

    def receive(self):
        self.raw_packets = []
        while True:
            new_byte = self.tserial.read()
            if not new_byte: break
            if new_byte == self.START_BYTE and not self.receive_buffer:
                # Starting a new raw packet
                self.error_flag = False
                self.receive_length = self.MAX_PACKET_SIZE
                self.process_byte(new_byte)
            elif not self.error_flag:
                if self.receive_buffer: self.process_byte(new_byte)
                else:
                    if new_byte in c.serial_errors:
                        self.raise_error_flag("Firmware: {}".format(
                            c.serial_errors[new_byte].msg))
                    else:
                        self.raise_error_flag("{}: {}".format(
                            c.serial_errors.N.msg, ord(new_byte)))
        return self.raw_packets

    def process_byte(self, byte):
        self.receive_buffer.extend(byte)
        if len(self.receive_buffer) == 4:
            if ord(byte) > self.MAX_PACKET_SIZE:
                self.raise_error_flag("Specified response length is too long")
            if ord(byte) < self.MIN_PACKET_SIZE:
                self.raise_error_flag("Specified response length is too short")
            else: self.receive_length = ord(byte)
        elif len(self.receive_buffer) == self.receive_length:
            # the packet is done
            self.raw_packets.append(self.receive_buffer)
            self.receive_buffer = bytearray()

    def raise_error_flag(self, msg):
        logger.error(msg)
        self.error_flag = True
        self.receive_buffer = bytearray()

PacketRequest = namedtuple('PacketRequest',
                           ["dest",
                           "payload",
                           "is_continuous",
                           "weight",
                           "remove_continuous"])
PacketRequest.__new__.__defaults__ = (False, 1, False)

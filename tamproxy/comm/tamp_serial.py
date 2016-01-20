import sys
import glob
import serial
import time
import logging
from .. import config as c


logger = logging.getLogger('tamproxy.connection')

class TAMPSerial(serial.Serial):
    """
    A normal serial interface, with the added features of:
    - Auto-detection of port
    - A simple "priming" handshake
    """

    PORT =          c.host.port
    BAUD_RATE =     c.firmware.baud_rate
    PRIME_TRIES =   c.host.prime_tries
    PRIME_COUNT =   c.host.prime_count

    def __init__(self, hello_packet=None, hello_response_length=None):
        if not self.PORT:
            self.serial_port = self.get_port()
            logger.info("Serial device found: {} {}".format(
                self.serial_port, self.BAUD_RATE))
        else: self.serial_port = self.PORT
        self.hello_packet = hello_packet
        self.hello_response_length = hello_response_length
        super(TAMPSerial, self).__init__(self.serial_port,
                                         self.BAUD_RATE,
                                         timeout=0,
                                         write_timeout=0)
        if hasattr(self, 'nonblocking'):
            self.nonblocking()
        if hello_packet: self.establish()

    def get_port(self):
        ports = self.detect_ports()
        if not ports:
            raise SerialPortUnavailableException("No suitable serial port detected")
        if len(ports) == 1: return ports[0]    
        else:
            print "Enter the index of the desired serial port:"
            for i,p in enumerate(ports): print i,p
            return ports[int(raw_input())]

    def detect_ports(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        # Graciously adapted from Stack Overflow:
        # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif (sys.platform.startswith('linux') or
              sys.platform.startswith('cygwin')):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.usb*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port, self.BAUD_RATE)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def establish(self):
        received = 0
        logger.info("Establishing a serial connection")
        for i in xrange(self.PRIME_TRIES):
            logger.debug("Sending {} HELLO packets".format(self.PRIME_COUNT))
            for i in xrange(self.PRIME_COUNT): 
                self.write(self.hello_packet)
            time.sleep(c.host.prime_sleep)
            n_received = ((self.in_waiting - received)
                          // self.hello_response_length)
            logger.debug("Received {} new HELLO responses".format(n_received))
            if n_received == self.PRIME_COUNT:
                self.read(self.in_waiting)
                logger.info("Serial connection established")
                return
            else:
                received = self.in_waiting
        raise SerialPortEstablishException((
                "[SerialPortEstablishException] Could not establish"
                " packet communication with "
                "port {} at baud {}".format(self.serial_port, self.BAUD_RATE)))

class SerialPortUnavailableException(IOError): pass
class SerialPortEstablishException(IOError): pass

__all__ = ['TAMPSerial', 'SerialPortUnavailableException', 'SerialPortEstablishException']
from threading import Thread, Event
from Queue import Queue, Empty
from .packet_controller import PacketController
from .. import config as c

class PacketForwarder(Thread):

    def __init__(self, reset_callback=None):
        super(PacketForwarder, self).__init__()
        self.__stop = Event()
        self.packets_received = 0
        self.sending_queue = Queue()
        self.callback_dict = dict()
        self.reset_callback = reset_callback
        self.pc = PacketController()
        self.pipe = self.pc.pipe_outside

    def stop(self):
        self.__stop.set()

    def empty_queue(self):
        while not self.sending_queue.empty():
            try: self.sending_queue.get(False)
            except Empty: pass

    def forward_requests(self):
        try:
            packet, callback = self.sending_queue.get_nowait()
            self.callback_dict[packet[:2]] = callback
            self.pipe.send(packet)
            self.sending_queue.task_done()
        except Empty:
            pass

    def callback_responses(self):
        while self.pipe.poll():
            request, response = self.pipe.recv()
            self.packets_received += 1
            if response == c.host.reset_msg: 
                self.empty_queue()
                if self.reset_callback: self.reset_callback()
            elif len(response) == 1 and response in c.responses:
                if response == 'G': continue
                print ("Firmware responded with an error: {} "
                       "for the request {}").format(
                            c.responses[response].msg, request)
            elif request in self.callback_dict:
                self.callback_dict[request](request, response)

    def run(self):
        self.pc.start()
        while not self.__stop.isSet():
            self.forward_requests()
            self.callback_responses()
        # Kill the pc process if thread stopped
        self.pc.stop()

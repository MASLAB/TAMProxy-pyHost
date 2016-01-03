from abc import ABCMeta, abstractproperty
from .. import TAMProxy

class Device:
    __metaclass__ = ABCMeta

    def __init__(self, tamproxy):
        self.tamp = tamproxy
        self.id = None
        self.tamp.add_device(self.add_payload, self.handle_add_response)

    @abstractproperty
    def add_payload(self):
        """
        Needs to be implemented by all derived classes
        It should generate and return a payload string that is used 
        to add the device to the microcontroller's device list.
        """
        raise NotImplementedError

    def handle_add_response(self, request, response):
        self.id = ord(response[1])
        self.tamp.recovery_data[self.id] = (self.add_payload,
                                          self.handle_add_response)

    def handle_remove_response(self, request, response):
        del self.tamp.recovery_add_packets[self.id]
        self.id = None
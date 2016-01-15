from abc import ABCMeta, abstractproperty
import logging

from .. import TAMProxy

logger = logging.getLogger('tamproxy.devices')

class Device(object):
    __metaclass__ = ABCMeta

    def __init__(self, tamproxy):
        self.tamp = tamproxy
        self.id = None
        self.tamp.add_device(self.add_payload, self.handle_add_response)
        logger.info('Adding device {}...'.format(self))
        while self.id is None: pass
        logger.info('Added device {}'.format(self))

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

    def __repr__(self):
        if self.id:
            return "<{}, id={}>".format(self.__class__.__name__, self.id)
        else:
            return super(Device, self).__repr__()

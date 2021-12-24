from abc import ABCMeta, abstractproperty, abstractmethod
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
        self.id = response[1]
        self.tamp.recovery_data[self.id] = (self.add_payload,
                                          self.handle_add_response)

    def handle_remove_response(self, request, response):
        del self.tamp.recovery_add_packets[self.id]
        self.id = None

    def __repr__(self, *args, **kwargs):
        if self.id is not None:
            kwargs['id'] = self.id

        arg_strs = [repr(arg) for arg in args]
        arg_strs += ["{}={!r}".format(k, v) for k, v in kwargs.items()]

        return "{}(tamp, {})".format(
            self.__class__.__name__,
            ', '.join(arg_strs)
        )


class ContinuousReadDevice(Device):
    __metaclass__ = ABCMeta

    def __init__(self, tamproxy, continuous=True):
        super(ContinuousReadDevice, self).__init__(tamproxy)
        if continuous: self.start_continuous()

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self._handle_update)

    def start_continuous(self, weight=1):
        self.tamp.send_request(self.id, self.READ_CODE, self._handle_update,
                             continuous=True, weight=weight)

    def stop_continuous(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.tamp.empty_callback,
                             continuous=True, weight=1, remove=True)

    @abstractmethod
    def _handle_update(self):
        raise NotImplementedError

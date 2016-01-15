from .device import ContinuousReadDevice
from .. import config as c

class AnalogInput(ContinuousReadDevice):

    DEVICE_CODE =   c.devices.analog_input.code
    READ_CODE =     c.devices.analog_input.read_code

    def __init__(self, tamproxy, pin, continuous=True):
        self.pin = pin
        self.val = 0
        super(AnalogInput, self).__init__(tamproxy, continuous)

    def __repr__(self):
        return super(AnalogInput, self).__repr__(self.pin)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pin)

    def _handle_update(self, request, response):
        self.val = (ord(response[0])<<8) + ord(response[1])

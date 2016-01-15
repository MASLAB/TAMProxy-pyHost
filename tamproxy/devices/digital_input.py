from .device import ContinuousReadDevice
from .. import config as c

class DigitalInput(ContinuousReadDevice):

    DEVICE_CODE =   c.devices.digital_input.code
    READ_CODE =     c.devices.digital_input.read_code

    def __init__(self, tamproxy, pin, pullup=True, continuous=True):
        self.pin = pin
        self.pullup = pullup
        self.val = 0
        self.prev_val = None
        super(DigitalInput, self).__init__(tamproxy, continuous)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pin) + chr(self.pullup)

    @property
    def changed(self):
        if self.prev_val is None:
            self.prev_val = self.val
            return False
        if self.val != self.prev_val:
            self.prev_val = self.val
            return True
        else: return False

    def _handle_update(self, request, response):
        self.val = ord(response)

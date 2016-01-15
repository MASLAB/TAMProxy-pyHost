from .device import Device
from .. import config as c

class DigitalOutput(Device):

    DEVICE_CODE =   c.devices.digital_output.code
    WRITE_CODE =    c.devices.digital_output.write_code

    def __init__(self, tamproxy, pin):
        self.pin = pin
        super(DigitalOutput, self).__init__(tamproxy)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pin)

    def write(self, value):
        self.tamp.send_request(self.id, self.WRITE_CODE + chr(value))

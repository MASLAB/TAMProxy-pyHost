from .device import ContinuousReadDevice
from .. import config as c

# Measures, computes, and returns color in the form of violet, blue, green, yellow, orange, red
class Color(ContinuousReadDevice):

    DEVICE_CODE = c.devices.color.code
    READ_CODE   = c.devices.color.read_code

    def __init__(self, tamproxy,
                 continuous=True):
        
        self.v = 0
        self.b = 0
        self.g = 0
        self.y = 0
        self.o = 0
        self.r = 0
        
        super(Color, self).__init__(tamproxy, continuous)

    @property
    def add_payload(self):
        # Note: Cannot have two color sensors, because there is only one I2C bus
        return self.DEVICE_CODE

    def _handle_update(self, request, response):
        assert len(response) == 12
        self.v = (response[0]<<8) + response[1]
        self.b = (response[2]<<8) + response[3]
        self.g = (response[4]<<8) + response[5]
        self.y = (response[6]<<8) + response[7]
        self.o = (response[8]<<8) + response[9]
        self.r = (response[10]<<8) + response[11]


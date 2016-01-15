from .device import ContinuousReadDevice
from .. import config as c

import ctypes

class Encoder(ContinuousReadDevice):

    DEVICE_CODE =   c.devices.encoder.code
    WRITE_CODE =    c.devices.encoder.write_code
    READ_CODE  =    c.devices.encoder.read_code

    def __init__(self, tamproxy, pin_a, pin_b, continuous=True):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.val = 0
        super(Encoder, self).__init__(tamproxy, continuous)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pin_a) + chr(self.pin_b)

    def write(self, value):
        value = int(value) & 0xFFFFFFFF
        self.tamp.send_request(self.id,
                               self.WRITE_CODE +
                               chr((int(value) >> 24) & 0xFF) +
                               chr((int(value) >> 16) & 0xFF) +
                               chr((int(value) >> 8) & 0xFF) +
                               chr(int(value) & 0xFF))

    def _handle_update(self, request, response):
        new_val = (
            (ord(response[0])<<24) |
            (ord(response[1])<<16) |
            (ord(response[2])<<8) |
            ord(response[3])
        )

        # this deals with unsigned overflow
        self.val += ctypes.c_int32(new_val - self.val).value

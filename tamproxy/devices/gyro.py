from .device import ContinuousReadDevice
from .. import config as c
import time

class Gyro(ContinuousReadDevice):

    DEVICE_CODE    = c.devices.gyro.code
    READ_CODE      = c.devices.gyro.read_code

    RANGE_250DPS = 1
    RANGE_500DPS = 2
    RANGE_2000DPS = 3

    def __init__(self, tamproxy, sdopin, range=RANGE_250DPS, integrate=True):
        self.range = range
        self.sdopin = sdopin
        self.integrate = integrate
        self.time = None
        self.x = 0
        self.y = 0
        self.z = 0
        super(Gyro, self).__init__(tamproxy, integrate)

    def __repr__(self):
        return super(Gyro, self).__repr__(self.range)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.sdopin) + chr(self.range)
    
    @staticmethod
    def _convert(response, start_index):
        # Get 16 bit value
        res = response[start_index] << 8 | response[start_index + 1]
        # Make signed
        if res > 0x7fff:
            res -= 0xffff
        return res
    
    def _handle_update(self, request, response):
        assert len(response) == 6
        # Assemble 16-bit returned values
        x = Gyro._convert(response, 0)
        y = Gyro._convert(response, 2)
        z = Gyro._convert(response, 4)
        
        if self.integrate:
            now = time.time()
            if self.time is not None:
                delta = now - self.time
                self.x += delta*x
                self.y += delta*y
                self.z += delta*z
            self.time = now
        else:
            self.x = x
            self.y = y
            self.z = z

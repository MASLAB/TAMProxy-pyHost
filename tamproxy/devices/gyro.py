from .device import ContinuousReadDevice
from .. import config as c
import time

class Gyro(ContinuousReadDevice):

    DEVICE_CODE = c.devices.gyro.code
    READ_CODE =   c.devices.gyro.read_code
    VALID_READ_STATUS = [0,1]

    def __init__(self, tamproxy, sspin, integrate=True):
        self.sspin = sspin
        self.val = 0
        self.status = None
        self.integrate = integrate
        self.time = None
        super(Gyro, self).__init__(tamproxy, integrate)

    def __repr__(self):
        return super(Gyro, self).__repr__(self.sspin)

    def reset_integration(self, angle=0.0):
        self.val = angle

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.sspin)

    def _handle_update(self, request, response):
        # print "handle_reading", response
        assert len(response) == 4
        # Assemble 32-bit returned value
        ret_word = ((ord(response[0])<<24) + (ord(response[1])<<16)
                    + (ord(response[2])<<8) + ord(response[3]))
        # Check status bits
        st0 = (ret_word >> 26) & 0x1
        st1 = (ret_word >> 27) & 0x1
        self.status = [st1,st0]
        if self.status != self.VALID_READ_STATUS:
            return
        # Extract rate reading
        reading = ((ret_word >> 10) & 0xffff)
        # Make signed
        if reading > 0x7fff:
            reading -= 0xffff
        reading /= 80.0 # Convert to degrees
        if self.integrate:
            now = time.time()
            if self.time is not None:
                delta = now - self.time
                self.val += delta*reading
            self.time = now
        else:
            self.val = reading

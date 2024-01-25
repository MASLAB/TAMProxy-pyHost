from .device import ContinuousReadDevice
from .. import config as c

# Unsigned 2 signed
def us2s(unsigned):
    signed = unsigned - 65536 if unsigned > 32767 else unsigned
    return signed

class Imu(ContinuousReadDevice):

    DEVICE_CODE = c.devices.imu.code
    READ_CODE   = c.devices.imu.read_code

    def __init__(self, tamproxy, dipin, continuous=True):
        self.dipin = dipin
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0
        self.mx = 0
        self.my = 0
        self.mz = 0
        super(Imu, self).__init__(tamproxy, continuous)

    def __repr__(self):
        return super(Imu, self).__repr__(self.dipin)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.dipin)

    def _handle_update(self, request, response):
        # print(response)
        assert len(response) == 18
        self.ax = us2s((response[0]<<8) | response[1]) / 1000.0
        self.ay = us2s((response[2]<<8) | response[3]) / 1000.0
        self.az = us2s((response[4]<<8) | response[5]) / 1000.0
        self.gx = us2s((response[6]<<8) | response[7]) / 1000.0
        self.gy = us2s((response[8]<<8) | response[9]) / 1000.0
        self.gz = us2s((response[10]<<8) | response[11]) / 1000.0
        self.mx = us2s((response[12]<<8) | response[13]) / 1000.0
        self.my = us2s((response[14]<<8) | response[15]) / 1000.0
        self.mz = us2s((response[16]<<8) | response[17]) / 1000.0


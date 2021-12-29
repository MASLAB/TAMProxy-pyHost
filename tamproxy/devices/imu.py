from .device import Device
from .. import config as c

# Unsigned 2 signed
def us2s(unsigned):
    signed = unsigned - 65536 if unsigned > 32767 else unsigned
    return signed

# Retreives continuous time-of-flight distance measurement in millimeters.
class Imu(Device):

    DEVICE_CODE = c.devices.imu.code
    READ_CODE   = c.devices.imu.read_code

    DEFAULT_ARES = 2.0 / 32768.0
    DEFAULT_GRES = 250.0 / 32768.0
    DEFAULT_MRES = 10 * 4912 / 32760

    def __init__(self, tamproxy, continuous=True):
        super(Imu, self).__init__(tamproxy)
        if continuous:
            self.start_continuous()
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0
        self.mx = 0
        self.my = 0
        self.mz = 0

    @property
    def add_payload(self):
        return self.DEVICE_CODE

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update)

    def start_continuous(self, weight=1):
        print("Starting continuous")
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update,
                               continuous=True, weight=weight)

    def stop_continuous(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.tamp.empty_callback,
                               continuous=True, weight=1, remove=True)

    def handle_update(self, request, response):
        assert len(response) == 18
        ax = us2s((response[0]<<8) + response[1])
        ay = us2s((response[2]<<8) + response[3])
        az = us2s((response[4]<<8) + response[5])
        gx = us2s((response[6]<<8) + response[7])
        gy = us2s((response[8]<<8) + response[9])
        gz = us2s((response[10]<<8) + response[11])
        mx = us2s((response[12]<<8) + response[13])
        my = us2s((response[14]<<8) + response[15])
        mz = us2s((response[16]<<8) + response[17])

        # scale values based on default sensor resolution
        self.ax = ax * self.DEFAULT_ARES
        self.ay = ay * self.DEFAULT_ARES
        self.az = az * self.DEFAULT_ARES
        self.gx = gx * self.DEFAULT_GRES
        self.gy = gy * self.DEFAULT_GRES
        self.gz = gz * self.DEFAULT_GRES
        self.mx = mx * self.DEFAULT_MRES
        self.my = my * self.DEFAULT_MRES
        self.mz = mz * self.DEFAULT_MRES


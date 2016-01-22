from .device import Device
from .. import config as c

# Measures, computes, and returns color in the form of RGB, clear (C), colorTemp
# and lux.
# Color temperature uses McCamy's formula
# Lux gives a heuristic calculation of luminescence
class Color(Device):

    DEVICE_CODE = c.devices.color.code
    READ_CODE   = c.devices.color.read_code

    # Integration time options
    INTEGRATION_TIME_2_4MS = 1
    INTEGRATION_TIME_24MS = 2
    INTEGRATION_TIME_50MS = 3
    INTEGRATION_TIME_101MS = 4
    INTEGRATION_TIME_154MS = 5
    INTEGRATION_TIME_700MS = 6

    # Gain options
    GAIN_1X = 1
    GAIN_4X = 2
    GAIN_16X = 3
    GAIN_60X = 4

    def __init__(self, tamproxy,
                 integrationTime=INTEGRATION_TIME_101MS,
                 gain=GAIN_1X, continuous=True):
        assert integrationTime >= 1 and integrationTime <= 6
        assert gain >= 1 and gain <= 4
        self.integrationTime = integrationTime
        self.gain = gain
        
        self.r = 0
        self.g = 0
        self.b = 0
        self.c = 0
        self.colorTemp = 0
        self.lux = 0
        
        super(Color, self).__init__(tamproxy)
        while self.id is None: pass
        if continuous:
            self.start_continuous()

    @property
    def add_payload(self):
        # Note: Cannot have two color sensors, because there is only one I2C bus
        return self.DEVICE_CODE + chr(self.integrationTime) + chr(self.gain)

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update)

    def start_continuous(self, weight=1):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update,
                               continuous=True, weight=weight)

    def stop_continuous(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.tamp.empty_callback,
                               continuous=True, weight=1, remove=True)

    def handle_update(self, request, response):
        assert len(response) == 12
        self.r = (ord(response[0])<<8) + ord(response[1])
        self.g = (ord(response[2])<<8) + ord(response[3])
        self.b = (ord(response[4])<<8) + ord(response[5])
        self.c = (ord(response[6])<<8) + ord(response[7])
        self.colorTemp = (ord(response[8])<<8) + ord(response[9])
        self.lux = (ord(response[10])<<8) + ord(response[11])

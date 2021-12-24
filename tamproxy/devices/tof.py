from .device import Device
from .. import config as c

# Retreives continuous time-of-flight distance measurement in millimeters.
class TimeOfFlight(Device):

    DEVICE_CODE = c.devices.tof.code
    READ_CODE   = c.devices.tof.read_code
    ENABLE_CODE = c.devices.tof.enable_code

    def __init__(self, tamproxy, xshut_pin, unique_id, continuous=True):
        self.dist = 0
        self.xshut_pin = xshut_pin
        self.unique_id = unique_id
        super(TimeOfFlight, self).__init__(tamproxy)
        while self.id is None: pass
        if continuous:
            self.start_continuous()

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.xshut_pin) + chr(self.unique_id)

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update)

    def enable(self):
        self.tamp.send_request(self.id, self.ENABLE_CODE, self.handle_enable)

    def start_continuous(self, weight=1):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update,
                               continuous=True, weight=weight)

    def stop_continuous(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.tamp.empty_callback,
                               continuous=True, weight=1, remove=True)

    def handle_update(self, request, response):
        assert len(response) == 2
        self.dist = (ord(response[0])<<8) + ord(response[1])

    def handle_enable(self, request, response):
        print("Enabled TOF", "{0:b}".format(ord(response[0])))

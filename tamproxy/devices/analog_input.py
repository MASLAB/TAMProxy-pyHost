from .device import Device
from .. import config as c

class AnalogInput(Device):

    DEVICE_CODE =   c.devices.analog_input.code
    READ_CODE =     c.devices.analog_input.read_code

    def __init__(self, tamproxy, pin, continuous=True):
        self.pin = pin
        self.val = 0
        super(AnalogInput, self).__init__(tamproxy)
        while self.id is None: pass
        if continuous: self.start_continuous()

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pin)

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_pin_update)

    def start_continuous(self, weight=1):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_pin_update, 
                             continuous=True, weight=weight)

    def stop_continuous(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.tamp.empty_callback, 
                             continuous=True, weight=1, remove=True)

    def handle_pin_update(self, request, response):
        self.val = (ord(response[0])<<8) + ord(response[1])

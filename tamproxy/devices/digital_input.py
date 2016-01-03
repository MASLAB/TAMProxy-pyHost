from device import Device
from .. import config as c

class DigitalInput(Device):

    DEVICE_CODE =   c.devices.digital_input.code
    READ_CODE =     c.devices.digital_input.read_code

    def __init__(self, tamproxy, pin, pullup=True, continuous=True):
        self.pin = pin
        self.pullup = True
        self.val = 0
        self.prev_val = None
        super(DigitalInput, self).__init__(tamproxy)
        while self.id is None: pass
        self.start_continuous()

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pin) + chr(self.pullup)

    @property
    def changed(self):
        if self.prev_val is None:
            self.prev_val = self.val
            return False
        if self.val != self.prev_val:
            self.prev_val = self.val
            return True
        else: return False

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_pin_update)

    def start_continuous(self, weight=1):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_pin_update, 
                             continuous=True, weight=weight)

    def stop_continuous(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.tamp.empty_callback, 
                             continuous=True, weight=1, remove=True)

    def handle_pin_update(self, request, response):
        self.val = ord(response)
from .device import Device
from .. import config as c

class Servo(Device):

    DEVICE_CODE =   c.devices.servo.code
    WRITE_CODE =    c.devices.servo.write_code

    def __init__(self, tamproxy, pwm_pin):
        self.pwm_pin = pwm_pin
        super(Servo, self).__init__(tamproxy)
        while self.id is None: pass

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pwm_pin)

    def write(self, uS):
        self.tamp.send_request(self.id,
                               self.WRITE_CODE +  
                               chr((int(uS) >> 8) & 0xFF) + 
                               chr(int(uS) & 0xFF))

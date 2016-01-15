from .device import Device
from .. import config as c

class Motor(Device):

    DEVICE_CODE =   c.devices.motor.code
    WRITE_CODE =    c.devices.motor.write_code

    def __init__(self, tamproxy, dir_pin, pwm_pin):
        self.dir_pin = dir_pin
        self.pwm_pin = pwm_pin
        super(Motor, self).__init__(tamproxy)

    def __repr__(self):
        return super(Motor, self).__repr__(self.dir_pin, self.pwm_pin)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.dir_pin) + chr(self.pwm_pin)

    def write(self, direction, pwm):
        self.tamp.send_request(self.id,
                               self.WRITE_CODE + 
                               chr(direction > 0) + 
                               chr((int(pwm) >> 8) & 0xFF) + 
                               chr(int(pwm) & 0xFF))

from .device import Device
from .. import config as c

class Servo(Device):

    DEVICE_CODE =   c.devices.servo.code
    WRITE_CODE =    c.devices.servo.write_code

    def __init__(self, tamproxy, pwm_pin, lower_uS=544, upper_uS=2400):
        self.pwm_pin = pwm_pin
        self.lower_uS = lower_uS
        self.upper_uS = upper_uS
        self.uS_range = self.upper_uS - self.lower_uS
        super(Servo, self).__init__(tamproxy)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.pwm_pin)

    def write(self, degrees):
        uS = degrees/180.*(self.uS_range)+self.lower_uS
        self.write_microseconds(uS)

    def write_microseconds(self, uS):
        self.tamp.send_request(self.id,
                               self.WRITE_CODE +  
                               chr((int(uS) >> 8) & 0xFF) + 
                               chr(int(uS) & 0xFF))
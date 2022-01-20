from .device import Device
from .. import config as c

class FeedbackMotor(Device):

    DEVICE_CODE =   c.devices.feedback_motor.code
    WRITE_CODE =    c.devices.feedback_motor.write_code

    def __init__(self, tamproxy, a_pin, b_pin, pwm_pin):
        self.a_pin = a_pin
        self.b_pin = b_pin
        self.pwm_pin = pwm_pin
        super(FeedbackMotor, self).__init__(tamproxy)

    def __repr__(self):
        return super(FeedbackMotor, self).__repr__(self.a_pin, self.b_pin, self.pwm_pin)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.a_pin) + chr(self.b_pin) + chr(self.pwm_pin)

    def write(self, direction, pwm):
        self.tamp.send_request(self.id,
                               self.WRITE_CODE + 
                               chr(direction > 0) + 
                               chr((int(pwm) >> 8) & 0xFF) + 
                               chr(int(pwm) & 0xFF))

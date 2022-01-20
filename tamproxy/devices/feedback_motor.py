from .device import ContinuousReadDevice
from .. import config as c

import ctypes
import struct

class FeedbackMotor(ContinuousReadDevice):

    DEVICE_CODE =   c.devices.feedback_motor.code
    WRITE_CODE =    c.devices.feedback_motor.write_code
    READ_CODE =     c.devices.encoder.read_code

    def __init__(self, tamproxy, motor_pin_a, motor_pin_b, motor_pin_pwm, enc_pin_a, enc_pin_b, continuous=True):
        self.motor_pin_a = motor_pin_a
        self.motor_pin_b = motor_pin_b
        self.motor_pin_pwm = motor_pin_pwm
        self.enc_pin_a = enc_pin_a
        self.enc_pin_b = enc_pin_b

        self.enc_count = 0

        super(FeedbackMotor, self).__init__(tamproxy)

    def __repr__(self):
        return super(FeedbackMotor, self).__repr__(self.motor_pin_a, self.motor_pin_b, self.motor_pin_pwm, self.enc_pin_a, self.enc_pin_b)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.motor_pin_a) + chr(self.motor_pin_b) + chr(self.motor_pin_pwm) + chr(self.enc_pin_a) + chr(self.enc_pin_b)

    def write(self, desired_angle):
        self.tamp.send_request(self.id,
                               self.WRITE_CODE + 
                               chr(desired_angle > 0) + 
                               chr((int(abs(desired_angle)) >> 16) & 0xFF) + 
                               chr((int(abs(desired_angle)) >> 8) & 0xFF) + 
                               chr(int(abs(desired_angle)) & 0xFF))

    def _handle_update(self, request, response):
        new_val = (
            (response[0]<<24) |
            (response[1]<<16) |
            (response[2]<<8) |
            (response[3])
        )

        # this deals with unsigned overflow
        self.enc_count += ctypes.c_int32(new_val - self.enc_count).value
from .device import ContinuousReadDevice
from .. import config as c

import ctypes
import struct

class FeedbackMotor(ContinuousReadDevice):

    DEVICE_CODE =   c.devices.feedback_motor.pos_code
    WRITE_CODE =    c.devices.feedback_motor.write_code
    READ_CODE =     c.devices.encoder.read_code

    def __init__(self, tamproxy, motor_pin_a, motor_pin_b, motor_pin_pwm, enc_pin_a, enc_pin_b, velocity_control, continuous=True):
        self.motor_pin_a = motor_pin_a
        self.motor_pin_b = motor_pin_b
        self.motor_pin_pwm = motor_pin_pwm
        self.enc_pin_a = enc_pin_a
        self.enc_pin_b = enc_pin_b
        self.velocity_control = velocity_control

        self.enc_count = 0
        self.estimated_velocity = 0.0

        if self.velocity_control:
            self.DEVICE_CODE = c.devices.feedback_motor.vel_code
        else:
            self.DEVICE_CODE = c.devices.feedback_motor.pos_code

        super(FeedbackMotor, self).__init__(tamproxy)

    def __repr__(self):
        return super(FeedbackMotor, self).__repr__(self.motor_pin_a, self.motor_pin_b, self.motor_pin_pwm, self.enc_pin_a, self.enc_pin_b, self.velocity_control)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.motor_pin_a) + chr(self.motor_pin_b) + chr(self.motor_pin_pwm) + chr(self.enc_pin_a) + chr(self.enc_pin_b)

    def write(self, setpoint):
        # convert float into byte array
        ba = bytearray(struct.pack("f", float(setpoint)))
        payload = self.WRITE_CODE + chr(ba[0]) + chr(ba[1]) + chr(ba[2]) + chr(ba[3])
        self.tamp.send_request(self.id, payload)
                               
    def _handle_update(self, request, response):
        if self.velocity_control:
            [new_val] = struct.unpack('f', response)
            self.estimated_velocity = float(new_val)
        else:
            new_val = (
                (response[0]<<24) |
                (response[1]<<16) |
                (response[2]<<8) |
                (response[3])
            )
            # this deals with unsigned overflow
            self.enc_count += ctypes.c_int32(new_val - self.enc_count).value
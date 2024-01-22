from .device import ContinuousReadDevice
from .. import config as c

import ctypes
import struct

class FeedbackMotor(ContinuousReadDevice):

    DEVICE_CODE =   c.devices.feedback_motor.pos_code
    WRITE_CODE =    c.devices.feedback_motor.write_code
    READ_CODE =     c.devices.encoder.read_code

    def __init__(self, tamproxy, dir_pin, pwm_pin, enc_pin_a, enc_pin_b, velocity_control, gear_ratio=10.0, continuous=True):
        self.dir_pin = dir_pin
        self.pwm_pin = pwm_pin
        self.enc_pin_a = enc_pin_a
        self.enc_pin_b = enc_pin_b
        self.velocity_control = velocity_control
        self.gear_ratio = gear_ratio

        self.enc_count = 0
        self.estimated_velocity = 0.0

        if self.velocity_control:
            self.DEVICE_CODE = c.devices.feedback_motor.vel_code
        else:
            self.DEVICE_CODE = c.devices.feedback_motor.pos_code

        super(FeedbackMotor, self).__init__(tamproxy)

    def __repr__(self):
        return super(FeedbackMotor, self).__repr__(self.dir_pin, self.pwm_pin, self.enc_pin_a, self.enc_pin_b, self.velocity_control, self.gear_ratio)

    @property
    def add_payload(self):
        return self.DEVICE_CODE + chr(self.dir_pin) + chr(self.pwm_pin) + chr(self.enc_pin_a) + chr(self.enc_pin_b)

    def write(self, setpoint):
        # convert float into byte array
        ba = bytearray(struct.pack("f", float(setpoint)))
        payload = self.WRITE_CODE + chr(ba[0]) + chr(ba[1]) + chr(ba[2]) + chr(ba[3]) + chr(self.gear_ratio)
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
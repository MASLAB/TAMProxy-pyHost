from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor, DigitalOutput
import math
import logging

class FeedbackMotorWrite(Sketch):
    LEFT_ENC_VCC = 30
    LEFT_ENC_GND = 29

    RIGHT_ENC_VCC = 34
    RIGHT_ENC_GND = 33

    def setup(self):
        self.left_enc_power = DigitalOutput(self.tamp, self.LEFT_ENC_VCC)
        self.left_enc_ground = DigitalOutput(self.tamp, self.LEFT_ENC_GND)
        self.left_enc_power.write(True)
        self.left_enc_ground.write(False)

        self.right_enc_power = DigitalOutput(self.tamp, self.RIGHT_ENC_VCC)
        self.right_enc_ground = DigitalOutput(self.tamp, self.RIGHT_ENC_GND)
        self.right_enc_power.write(True)
        self.right_enc_ground.write(False)

        self.lmotor = FeedbackMotor(self.tamp, 16, 15, 32, 31, True)
        self.left_motor_vel_rad_per_s = 1
        
        self.rmotor = FeedbackMotor(self.tamp, 14, 13, 36, 35, True)
        self.right_motor_vel_rad_per_s = -1

        self.timer = Timer()
        self.debug_timer = Timer()

        self.GR = 50.0 # gear ratio
        self.CPR = 64.0 # counts per revolution

        self.logger = logging.getLogger('tamproxy')

    def loop(self):
        if (self.timer.millis() > 5):
            self.lmotor.write(self.left_motor_vel_rad_per_s)
            self.rmotor.write(self.right_motor_vel_rad_per_s)
            self.timer.reset()
        if (self.debug_timer.millis() > 100):
            self.logger.info("Left Desired V: {:.2f} Measured V: {:.2f}   Right Desired V: {:.2f} Measured V: {:.2f}".format(self.left_motor_vel_rad_per_s, self.lmotor.estimated_velocity, self.right_motor_vel_rad_per_s, self.rmotor.estimated_velocity))
            self.debug_timer.reset()
            
if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
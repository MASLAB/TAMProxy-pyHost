from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor, DigitalOutput
import math
import logging

class FeedbackMotorWrite(Sketch):
    ENC_VCC = 30
    ENC_GND = 29

    def setup(self):
        self.enc_power = DigitalOutput(self.tamp, self.ENC_VCC)
        self.enc_ground = DigitalOutput(self.tamp, self.ENC_GND)
        self.enc_power.write(True)
        self.enc_ground.write(False)

        self.motor = FeedbackMotor(self.tamp, 16, 15, 32, 31, True)
        self.motor_vel_rad_per_s = 6.28
        
        self.timer = Timer()
        self.debug_timer = Timer()

        self.GR = 50.0 # gear ratio
        self.CPR = 64.0 # counts per revolution

        self.logger = logging.getLogger('tamproxy')

    def loop(self):
        if (self.timer.millis() > 5):
            self.motor.write(self.motor_vel_rad_per_s)
            self.timer.reset()
        if (self.debug_timer.millis() > 100):
            self.logger.info("Desired V: {} Measured V: {}".format(self.motor, self.motor.estimated_velocity))
            self.debug_timer.reset()
            
if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
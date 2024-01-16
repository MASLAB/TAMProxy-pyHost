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

        # dir pin, pwm pin, enc pin a, encoder pin b, enableVelocityControl?
        self.motor = FeedbackMotor(self.tamp, 16, 15, 32, 31, False)
        self.motor.write(0.0)
        self.motorangle = 360.0
        self.timer = Timer()
        self.debug_timer = Timer()

        self.GR = 50.0 # gear ratio
        self.CPR = 64.0 # counts per revolution
        
        self.logger = logging.getLogger('tamproxy')

    def loop(self):
        if (self.timer.millis() > 5):
            self.motor.write(self.motorangle)
            self.timer.reset()
        if (self.debug_timer.millis() > 1000):
            self.logger.info("Desired Angle: {} Measured Angle: {}".format(self.motorangle, 360.0*self.motor.enc_count/(self.GR*self.CPR)))
            self.timer.reset()
    
if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor, DigitalOutput
import math

class FeedbackMotorWrite(Sketch):
    ENC_VCC = 36
    ENC_GND = 35

    def setup(self):
        self.enc_power = DigitalOutput(self.tamp, self.ENC_VCC)
        self.enc_ground = DigitalOutput(self.tamp, self.ENC_GND)
        self.enc_power.write(True)
        self.enc_ground.write(False)

        self.motor = FeedbackMotor(self.tamp, 3, 5, 7, 37, 38, False)
        self.motor.write(0.0)
        self.motorangle = 360.0
        self.timer = Timer()

        self.GR = 50.0 # gear ratio
        self.CPR = 64.0 # counts per revolution

    def loop(self):
        self.motor.write(self.motorangle)
        if (self.timer.millis() > 100):
            self.timer.reset()
            print("Desired Angle: {} Measured Angle: {}".format(self.motorangle, 360.0*self.motor.enc_count/(self.GR*self.CPR)))

if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
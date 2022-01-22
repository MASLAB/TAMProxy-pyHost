from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor, DigitalOutput
import math

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class FeedbackMotorWrite(Sketch):
    ENC_VCC = 8
    ENC_GND = 9

    def setup(self):
        self.enc_power = DigitalOutput(self.tamp, self.ENC_VCC)
        self.enc_ground = DigitalOutput(self.tamp, self.ENC_GND)
        self.enc_power.write(True)
        self.enc_ground.write(False)

        self.motor = FeedbackMotor(self.tamp, 3, 4, 5, 7, 6)
        self.motor.write(0)
        self.motorangle = math.pi
        self.timer = Timer()

        self.GR = 50.0 # gear ratio
        self.CPR = 64.0 # counts per revolution

    def loop(self):
        self.motor.write(self.convert_to_angle_cmd(self.motorangle))
        if (self.timer.millis() > 100):
            self.timer.reset()
            print("Desired Angle: {} Measured Angle: {}".format(180/math.pi*self.motorangle, 360.0*self.motor.enc_count/(self.GR*self.CPR)))

    def convert_to_angle_cmd(self, angle):
        # factor of 4 due to signed int
        return angle/(4*math.pi)*255

if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
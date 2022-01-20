from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor, DigitalOutput

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
        self.motor.write(1,0)
        self.delta = 25
        self.motorval = 0
        self.timer = Timer()

    def loop(self):
        if (self.timer.millis() > 100):
            self.timer.reset()
            if abs(self.motorval) > 255: self.delta = -self.delta
            self.motorval += self.delta
            self.motor.write(self.motorval>0, abs(self.motorval))
            print("Encoder Count: {}".format(self.motor.enc_count))

if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
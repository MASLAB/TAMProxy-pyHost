from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class FeedbackMotorWrite(Sketch):

    def setup(self):
        self.motor = FeedbackMotor(self.tamp, 3, 4, 5)
        self.motor.write(1,0)
        self.delta = 1
        self.motorval = 0
        self.timer = Timer()

    def loop(self):
        if (self.timer.millis() > 10):
            self.timer.reset()
            if abs(self.motorval) == 255: self.delta = -self.delta
            self.motorval += self.delta
            self.motor.write(self.motorval>0, abs(self.motorval))

if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
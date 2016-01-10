from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Servo

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class ServoWrite(Sketch):

    def setup(self):
        self.servo = Servo(self.tamp, 9)
        self.servo.write(1050)
        self.timer = Timer()
        self.end = False

    def loop(self):
        if (self.timer.millis() > 2000):
            self.timer.reset()
            if self.end:
				self.servo.write(1050)
            else:
				self.servo.write(1950)
            self.end = not self.end

if __name__ == "__main__":
    sketch = ServoWrite()
    sketch.run()
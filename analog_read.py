from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput

# Reads the analog voltage at one of the analog pins

class AnalogRead(SyncedSketch):

    adc_pin = 0

    def setup(self):
        self.testpin = AnalogInput(self.tamp, self.adc_pin)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.testpin.val

if __name__ == "__main__":
    sketch = AnalogRead(1, -0.00001, 100)
    sketch.run()
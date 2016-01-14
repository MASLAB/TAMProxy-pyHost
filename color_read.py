from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color

# Prints RGB, clear(C), colorTemp, and lux values read and
# computed from the device. For more details, see the Adafruit_TCS34725
# Arduino library, from which the colorTemp and lux computations are
# used.

# Color sensor should be connected to the I2C ports (SDA and SCL)

class ColorRead(SyncedSketch):

    def setup(self):
        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.color.r, self.color.g, self.color.b, self.color.c
            print self.color.colorTemp, self.color.lux

if __name__ == "__main__":
    sketch = ColorRead(1, -0.00001, 100)
    sketch.run()

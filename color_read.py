from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color

# Prints violet, blue, green, yellow, orange, red values read and
# computed from the device. For more details, see the Adafruit_AS726x
# Arduino library

# Color sensor should be connected to the I2C ports (SDA and SCL)

class ColorRead(SyncedSketch):

    def setup(self):
        self.color = Color(self.tamp)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 10:
            # self.color.update()
            self.timer.reset()
            print(self.color.v, self.color.b, self.color.g)
            print(self.color.y, self.color.o, self.color.r)

if __name__ == "__main__":
    sketch = ColorRead(1, -0.00001, 100)
    sketch.run()

from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro

# Prints integrated Gyro readings

class GyroRead(SyncedSketch):

    # Set me!
    ss_pin = 10

    def setup(self):
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits
            print "{:6f}, raw: 0x{:08x} = 0b{:032b}".format(self.gyro.val, self.gyro.raw, self.gyro.raw)

if __name__ == "__main__":
    sketch = GyroRead(1, -0.00001, 100)
    sketch.run()

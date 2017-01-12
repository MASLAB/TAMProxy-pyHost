from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import TimeOfFlight

# Print millimeter distance read. Time-of-flight VL53L0X sensor should be
# connected to the I2C ports (SDA and SCL).

class TimeOfFlightRead(SyncedSketch):

    def setup(self):
        self.tof = TimeOfFlight(self.tamp, 0)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.tof.dist, "mm"

if __name__ == "__main__":
    sketch = TimeOfFlightRead(1, -0.00001, 100)
    sketch.run()

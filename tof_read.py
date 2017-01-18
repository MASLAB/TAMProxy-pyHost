from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import TimeOfFlight

# Print millimeter distance read. Time-of-flight VL53L0X sensor should be
# connected to the I2C ports (SDA and SCL).

# Your code should always set up all ToF sensors with unique ids (1-15) FIRST,
# and only then enable them all. Otherwise they will walk over each other
# on the I2C bus, since they will all have the same address.

class TimeOfFlightRead(SyncedSketch):

    # Set these to the digital inputs connected to each xshut pin
    tof_pin = 20
    tof2_pin = 21

    def setup(self):
        # Add all ToFs
        self.tof = TimeOfFlight(self.tamp, self.tof_pin, 1)
        self.tof2 = TimeOfFlight(self.tamp, self.tof2_pin, 2)

        # Now enable them all
        self.tof.enable()
        self.tof2.enable()
        
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.tof.dist, "mm", "/", self.tof2.dist, "mm"

if __name__ == "__main__":
    sketch = TimeOfFlightRead(1, -0.00001, 100)
    sketch.run()

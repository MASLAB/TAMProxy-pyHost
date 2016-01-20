from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro

# Prints integrated Gyro readings

class GyroRead(SyncedSketch):

    # Set me!
    ss_pin = 10

    def setup(self):
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.timer = Timer()
        self.cali_timer = Timer()
        self.calibration = 0.0
        self.calibrated = False

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits
            print "{:6f}, raw: 0x{:08x} = 0b{:032b}".format(self.gyro.val, self.gyro.raw, self.gyro.raw)
        # Janky autocalibration scheme
        if not self.calibrated and self.cali_timer.millis() > 3000:
            drift = self.gyro.val / (self.cali_timer.millis() / 1000.0)
            # Arbitrary calibration tolerance of 0.1 deg/sec
            if abs(drift) > 0.1:
                self.calibration += drift
                print "Calibration:", self.calibration
                self.gyro.calibrate_bias(self.calibration)
            else:
                print "Calibration complete:", self.calibration
                self.calibrated = True
            self.gyro.reset_integration()
            self.cali_timer.reset()
            
if __name__ == "__main__":
    sketch = GyroRead(1, -0.00001, 100)
    sketch.run()

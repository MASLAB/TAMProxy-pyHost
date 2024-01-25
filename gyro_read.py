from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro

# Prints integrated Gyro readings

class GyroRead(SyncedSketch):

    # Set me!
    sdo_pin = 20

    def setup(self):
        self.gyro = Gyro(self.tamp, self.sdo_pin, range=Gyro.RANGE_250DPS)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print("x: {:6f}, y: {:6f}, z: {:6f}".format(self.gyro.x, self.gyro.y, self.gyro.z))
            
if __name__ == "__main__":
    sketch = GyroRead(1, -0.00001, 100)
    sketch.run()

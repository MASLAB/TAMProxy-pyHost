from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Imu

# Print x, y, and z axis acceleration, gyro, and magnetometer values. IMU should
# be connected to the I2C ports (SDA and SCL).

class ImuRead(SyncedSketch):

    def setup(self):
        self.imu = Imu(self.tamp)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print "Accel x: {} g, y: {} g, z: {} g".format(
                self.imu.ax, self.imu.ay, self.imu.az)
            print "Gyro x: {} deg/sec, y: {} deg/sec, z: {} deg/sec".format(
                self.imu.gx, self.imu.gy, self.imu.gz)
            print "Mag x: {} mG, y: {} mG, z: {} mG".format(
                self.imu.mx, self.imu.my, self.imu.mz)

if __name__ == "__main__":
    sketch = ImuRead(1, -0.00001, 100)
    sketch.run()

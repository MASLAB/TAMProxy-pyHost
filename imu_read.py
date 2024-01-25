from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Imu

# Print x, y, and z axis acceleration, gyro, and magnetometer values. IMU should
# be connected to the I2C ports (SDA and SCL).

class ImuRead(SyncedSketch):

    # Set me!
    di_pin = 20

    def setup(self):
        self.imu = Imu(self.tamp, self.di_pin)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 1000:
            self.timer.reset()
            print("Accel x: {} m/s^2, y: {} m/s^2, z: {} m/s^2".format(
                self.imu.ax, self.imu.ay, self.imu.az))
            print("Gyro x: {} rad/sec, y: {} rad/sec, z: {} rad/sec".format(
                self.imu.gx, self.imu.gy, self.imu.gz))
            print("Mag x: {} uT, y: {} uT, z: {} uT\n".format(
                self.imu.mx, self.imu.my, self.imu.mz))

if __name__ == "__main__":
    sketch = ImuRead(1, -0.00001, 100)
    sketch.run()

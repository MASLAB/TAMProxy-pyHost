from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import FeedbackMotor, DigitalOutput
import math

class FeedbackMotorWrite(Sketch):
    ENC_VCC_left = 10
    ENC_GND_left = 11

    ENC_VCC_right = 38
    ENC_GND_right = 39

    def setup(self):
        self.enc_power_left = DigitalOutput(self.tamp, self.ENC_VCC_left)
        self.enc_ground_left = DigitalOutput(self.tamp, self.ENC_GND_left)
        self.enc_power_left.write(True)
        self.enc_ground_left.write(False)

        # self.enc_power_right = DigitalOutput(self.tamp, self.ENC_VCC_right)
        # self.enc_ground_right = DigitalOutput(self.tamp, self.ENC_GND_right)
        # self.enc_power_right.write(True)
        # self.enc_ground_right.write(False)

        self.left_motor = FeedbackMotor(self.tamp, 16, 15, 32, 31, True)
        self.left_motor_vel = 0.1
        
        # self.right_motor = FeedbackMotor(self.tamp, 4, 2, 6, 37, 36, True)
        # self.right_motor_vel = -22.0

        self.left_motor.write(0.0)
        # self.right_motor.write(0.0)
        self.timer = Timer()

        self.GR = 50.0 # gear ratio
        self.CPR = 64.0 # counts per revolution

    def loop(self):
        self.left_motor.write(self.left_motor_vel)
        # self.right_motor.write(self.right_motor_vel)
        if (self.timer.millis() > 100):
            self.timer.reset()
            #print("Left Vd: {} V: {:.4f}   Right Vd: {} V: {:.4f}".format(self.left_motor_vel, self.left_motor.estimated_velocity, self.right_motor_vel, self.right_motor.estimated_velocity))
            print("Left Vd: {} V: {:.4f} ".format(self.left_motor_vel, self.left_motor.estimated_velocity))

if __name__ == "__main__":
    sketch = FeedbackMotorWrite()
    sketch.run()
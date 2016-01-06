from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogOutput

# Sweeps a PWM output from 0 to 255 every 2560 ms (increment by 1 each 10ms)

class AnalogWrite(Sketch):

    PWM_PIN = 3

    def setup(self):
        self.pwm = AnalogOutput(self.tamp, self.PWM_PIN)
        self.pwm_value = 0
        self.pwm_timer = Timer()

    def loop(self):
        if (self.pwm_timer.millis() > 10):
            self.pwm_timer.reset()
            self.pwm_value = (self.pwm_value + 1) % 256
            self.pwm.write(self.pwm_value)

if __name__ == "__main__":
    sketch = AnalogWrite()
    sketch.run()
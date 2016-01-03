from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import DigitalOutput

# The classic blink sketch. The Hello World of Arduino

class Blink(Sketch):

    def setup(self):
        self.led = DigitalOutput(self.tamp, 13)
        self.led_timer = Timer()
        self.led_state = False

    def loop(self):
        if self.led_timer.millis() > 1000:
            self.led_timer.reset()
            self.led_state = not self.led_state
            self.led.write(self.led_state)

if __name__ == "__main__":
    sketch = Blink()
    sketch.run()
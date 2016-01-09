
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Encoder


class EncoderRead(SyncedSketch):

    pins = 5, 6

    def setup(self):
        self.encoder = Encoder(self.tamp, *self.pins, continuous=True)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.encoder.val

if __name__ == "__main__":
    sketch = EncoderRead(1, -0.00001, 100)
    sketch.run()
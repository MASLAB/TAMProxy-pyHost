from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Encoder, DigitalOutput

# Prints a quadrature encoder's position
class EncoderRead(SyncedSketch):

    ENC_VCC = 35
    ENC_GND = 36

    pins = 33, 34

    def setup(self):
        self.enc_power = DigitalOutput(self.tamp, self.ENC_VCC)
        self.enc_ground = DigitalOutput(self.tamp, self.ENC_GND)
        self.enc_power.write(True)
        self.enc_ground.write(False)
        self.encoder = Encoder(self.tamp, *self.pins, continuous=True)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print(self.encoder.val)

if __name__ == "__main__":
    sketch = EncoderRead(1, -0.00001, 100)
    sketch.run()

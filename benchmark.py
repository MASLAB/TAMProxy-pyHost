from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import DigitalInput

# Reads from all pins for 5 seconds, then prints throughput, frequency,
# and sleep duration
# If you switch out the comments in lines 10,11 and 31,32, you can see
# how SyncedSketch can maintain a good ratio of packet throughput 
# (packets per second) to control loop frequency (loops per second)

class Benchmark(Sketch):
#class benchmark(SyncedSketch):

    testpin_pin = 0

    def setup(self):
        self.testpins = []
        for i in xrange(34):
            self.testpins.append(DigitalInput(self.tamp, i))

    def loop(self):
        if self.elapsed > 5:
            print self.throughput
            print self.frequency
            print self.sleep_duration
            self.stop()
        for i in xrange(34):
            if self.testpins[i].changed:
                print i, self.testpins[i].val

if __name__ == "__main__":
    sketch = Benchmark(0.001)
    #sketch = benchmark(1, -0.00001, 100)
    sketch.run()
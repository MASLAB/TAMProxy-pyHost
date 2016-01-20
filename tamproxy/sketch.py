from abc import ABCMeta, abstractmethod
from tamproxy import TAMProxy
from time import sleep, time
from . import config as c

class Sketch(object):
    __metaclass__ = ABCMeta

    def __init__(self, sleep_duration=c.host.default_sleep_duration):
        self.sleep_duration = sleep_duration
        self.tamp = TAMProxy()
        self.stopped = False
        self.start_time = None

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def loop(self):
        raise NotImplementedError

    def start(self):
        self.start_time = time()
        self.iterations = 0 # float cuz this can get big
        if not self.tamp.started: self.tamp.start()
        self.stopped = False

    def stop(self):
        self.stopped = True

    @property
    def elapsed(self):
        return time() - self.start_time

    @property
    def throughput(self):
        return self.tamp.pf.packets_received / self.elapsed

    @property
    def frequency(self):
        return self.iterations / self.elapsed

    def run(self):
        self.start()
        try:
            self.setup()
            self.tamp.pf.pc.set_continuous_enabled(True)
            print "Entered loop"
            while not self.stopped:
                self.loop()
                self.iterations += 1
                sleep(self.sleep_duration)
        except KeyboardInterrupt:
            self.stop() # as if the sketch had called it
        self.tamp.pf.pc.set_continuous_enabled(False)
        self.tamp.stop()
        print "Sketch finished running"

class SyncedSketch(Sketch):

    def __init__(self, ratio, gain, interval,
                 sleep_interval=c.host.default_sleep_duration):
        self.sync_ratio = ratio
        self.sync_gain = gain
        self.interval = interval
        super(SyncedSketch, self).__init__(sleep_interval)

    def start(self):
        self.last_packets_received = 0
        super(SyncedSketch, self).start()

    def adjust_sleeptime(self):
        new_packets_received = self.tamp.pf.packets_received
        dp = new_packets_received - self.last_packets_received
        error = float(dp)/self.interval - self.sync_ratio
        self.sleep_duration = min(max(self.sleep_duration + 
                                      error * self.sync_gain, 0), .1)
        #print error/self.sync_ratio, self.sleep_duration
        self.last_packets_received = new_packets_received

    def run(self):
        self.start()
        try:
            self.setup()
            print "Entered loop"
            self.tamp.pf.pc.set_continuous_enabled(True)
            while not self.stopped:
                self.loop()
                self.iterations += 1
                if not self.iterations % self.interval:
                    self.adjust_sleeptime()
                sleep(self.sleep_duration)
        except KeyboardInterrupt:
            self.stop()
        self.tamp.pf.pc.set_continuous_enabled(False)
        self.tamp.stop()
        print "\nSketch finished running"

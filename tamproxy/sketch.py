from abc import ABCMeta, abstractmethod
from tamproxy import TAMProxy
from time import sleep, time
import signal
import sys
try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
    rclpy_installed = True
except ImportError:
    rclpy_installed = False

try:
    import rospy
    from std_msgs.msg import String
    rospy_installed = True
except ImportError:
    rospy_installed = False

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

    def pre_setup(self):
        self.start_time = time()
        self.iterations = 0
        self.tamp.start()
        self.stopped = False

    def post_setup(self):
        self.tamp.pf.pc.set_continuous_enabled(True)
        print("Entering Loop")

    def pre_loop(self):
        pass

    def post_loop(self):
        self.iterations += 1
        sleep(self.sleep_duration)

    def on_exit(self):
        self.tamp.stop()
        print("Sketch finished running")

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
        try:
            self.pre_setup()
            self.setup()
            self.post_setup()
            while not self.stopped:
                self.pre_loop()
                self.loop()
                self.post_loop()
        except KeyboardInterrupt:
            self.stop() # as if the sketch had called it
        self.on_exit()

class SyncedSketch(Sketch):

    def __init__(self, ratio, gain, interval,
                 sleep_interval=c.host.default_sleep_duration):
        self.sync_ratio = ratio
        self.sync_gain = gain
        self.interval = interval
        super(SyncedSketch, self).__init__(sleep_interval)

    def pre_setup(self):
        self.last_packets_received = 0
        super(SyncedSketch, self).pre_setup()

    def post_loop(self):
        super(SyncedSketch, self).post_loop()
        if not self.iterations % self.interval:
            self.adjust_sleeptime()

    def adjust_sleeptime(self):
        new_packets_received = self.tamp.pf.packets_received
        dp = new_packets_received - self.last_packets_received
        error = float(dp)/self.interval - self.sync_ratio
        self.sleep_duration = min(max(self.sleep_duration + 
                                      error * self.sync_gain, 0), .1)
        self.last_packets_received = new_packets_received


if rclpy_installed:
    class ROS2Sketch(Sketch, Node):

        def __init__(self, rate=100, node_name="teensy"):
            super().__init__()                       # Calls Sketch.__init__()
            super(Sketch, self).__init__(node_name)  # Calls Node.__init__()
            def signal_handler(sig, frame):
                print('Stopping TAMProxy')
                self.on_exit()
                sys.exit()
            signal.signal(signal.SIGINT, signal_handler)

        def run_setup(self):
            self.pre_setup()
            self.setup()
            self.post_setup()

        def destroy(self):
            self.on_exit()

if rospy_installed:
    class ROSSketch(Sketch):

        def __init__(self, rate=100, node_name="teensy", pub_topic="tamproxy"):
            super(ROSSketch, self).__init__()
            rospy.init_node(node_name, anonymous=True)
            self.pub = rospy.Publisher(pub_topic, String, queue_size=10)
            self.rate = rospy.Rate(rate)

        def post_loop(self):
            try:
                self.iterations += 1
                self.rate.sleep()
                # Just some diagnostic info
                self.pub.publish("Throughput: {}, Frequency:{}".format(self.throughput, self.frequency))
                # ensure that we handle the ROS node lifecycle correctly
                if rospy.is_shutdown():
                    print("ROS shutdown")
                    self.stop()
            except rospy.exceptions.ROSException:
                self.stop()

        def run(self):
            # Let ROS catch KeyboardInterrupts
            self.pre_setup()
            self.setup()
            self.post_setup()
            while not self.stopped:
                self.pre_loop()
                self.loop()
                self.post_loop()
            self.on_exit()

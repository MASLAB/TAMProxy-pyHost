import logging

from .comm import PacketForwarder
from . import config as c


logger = logging.getLogger('tamproxy')

class TAMProxy(object):

    DEVICELIST_CODE =   c.devices.devicelist.code
    ADD_CODE =          c.devices.devicelist.add_code
    REMOVE_CODE =       c.devices.devicelist.remove_code
    CLEAR_CODE =        c.devices.devicelist.clear_code

    def __init__(self):
        # used to reinitialize devices on a restart
        self.recovery_data = dict()

        self.start()

    def start(self):
        self.started = False
        self.pf = PacketForwarder(self.handle_device_reset)
        self.pf.start()
        while self.pf.is_alive() and not self.started: pass
        if not self.started:
            raise Exception('Forwarder exited before reset was completed')

    def stop(self):
        self.clear_devices()
        self.pf.stop()
        self.pf.join()
        self.started = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        logger.info("Stopping tamproxy")
        self.stop()

    def handle_device_reset(self):
        if self.recovery_data:
            logger.warn("A reset occured with active devices - attempting to recover")
    
        self.clear_devices()
        for device_id, add_vals in self.recovery_data.iteritems():
            self.add_device(*add_vals)
        if not self.started: self.started = True

    def add_device(self, add_payload, callback):
        self.send_request(self.DEVICELIST_CODE,
                          self.ADD_CODE + add_payload,
                          callback)

    def remove_device(self, device_id, callback):
        self.send_request(self.DEVICELIST_CODE,
                          self.REMOVE_CODE + device_id,
                          callback)

    def clear_devices(self):
        self.send_request(self.DEVICELIST_CODE,
                          self.CLEAR_CODE,
                          self.empty_callback)

    def send_request(self, device_id, payload, callback=None, 
                     continuous=False, weight=1, remove=False):
        """
        Make a request to the underlying PacketForwarder
        """
        if not callback: callback = self.empty_callback
        if device_id is not None: 
            self.pf.enqueue(device_id, payload, callback, continuous, weight, remove)
            return True
        else: return False

    def empty_callback(self, request, response):
        pass

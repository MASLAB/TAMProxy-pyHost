from comm import PacketForwarder
from . import config as c

class TAMProxy(object):

    DEVICELIST_CODE =   c.devices.devicelist.code
    ADD_CODE =          c.devices.devicelist.add_code
    REMOVE_CODE =       c.devices.devicelist.remove_code
    CLEAR_CODE =        c.devices.devicelist.clear_code

    def __init__(self):
        self.recovery_data = dict()
        self.start()

    def start(self):
        self.started = False
        self.pf = PacketForwarder(self.handle_device_reset)
        self.pf.start()
        self.q = self.pf.sending_queue
        while not self.started: pass

    def stop(self):
        self.pf.stop()
        self.pf.join()
        self.started = False

    def handle_device_reset(self):
        self.clear_devices()
        for device_id, add_vals in self.recovery_data.iteritems():
            self.add_device(*add_vals)
        if not self.started: self.started = True

    def add_device(self, add_payload, callback):
        payload = self.ADD_CODE + add_payload
        self.send_request(self.DEVICELIST_CODE,
                         payload,
                         callback)

    def remove_device(self, device_id, callback):
        payload = self.REMOVE_CODE + device_id
        self.send_request(self.DEVICELIST_CODE,
                         payload,
                         callback)

    def clear_devices(self):
        self.send_request(self.DEVICELIST_CODE,
                         self.CLEAR_CODE,
                         self.empty_callback)

    def send_request(self, device_id, payload, callback=None, 
                     continuous=False, weight=1, remove=False):
        if not callback: callback = self.empty_callback
        if device_id is not None: 
            self.q.put(((device_id, payload, continuous, weight, remove),
                        callback))
            return True
        else: return False

    def empty_callback(self, request, response):
        pass

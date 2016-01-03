from time import time
import yaml
import os

class dotdict(dict):
    marker = object()
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'expected dict'

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, dotdict):
            value = dotdict(value)
        super(dotdict, self).__setitem__(key, value)

    def __getitem__(self, key):
        found = self.get(key, dotdict.marker)
        if found is dotdict.marker:
            found = dotdict()
            super(dotdict, self).__setitem__(key, found)
        return found

    __setattr__ = __setitem__
    __getattr__ = __getitem__

target = os.path.dirname(os.path.realpath(__file__)) + "/config.yaml"
with open(target, 'r') as config_file:
    config_yaml = config_file.read()

config = dotdict(yaml.load(config_yaml))

class Timer():

    def __init__(self):
        self.val = time()

    def millis(self):
        return round((time() - self.val)*1e3)

    def micros(self):
        return round((time() - self.val)*1e6)

    def set(self, new_value):
        self.val = new_value

    def reset(self):
        self.val = time()
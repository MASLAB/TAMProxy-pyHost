from .utils import dotdict, Timer, config
from .tamproxy import TAMProxy
from .sketch import Sketch, SyncedSketch
try:
	from .sketch import ROSSketch # Only declared if rospy installed
except ImportError:
	pass

def _init_logging():
    # do this in a function to avoid exposing globals
    from utils import config as c
    import logging.config
    logging.config.dictConfig(c.logging)

_init_logging()

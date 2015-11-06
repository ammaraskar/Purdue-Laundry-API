# Create a config.py to override any of these

DEBUG = False
HOST = "0.0.0.0"
PORT = 80

try:
    from config import *
except ImportError:
    pass

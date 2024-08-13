#
# Copy this file to your homework folder
# Do not upload this file with submission; only upload main.py
#
import random

class Sensor:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
    def read(self):
        return max(0, min(5*random.expovariate(2)+random.random()*0.1, 5.0))


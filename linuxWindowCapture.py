from mss import mss, tools
import numpy as np

monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

class linuxWindowCapture:
    def __init__(self, window_name=None):
        self.sct = mss()


    def get_screenshot(self):
        shot = np.array(self.sct.grab(monitor))
        return shot[...,:3]
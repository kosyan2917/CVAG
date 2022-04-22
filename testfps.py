import time

import numpy as np
import win32gui, win32ui, win32con
import d3dshot
import cv2
from threading import Thread



def kkk():

    b = kekwCapture(2000, 1100)

class kekwCapture:
    def __init__(self, left, top):

        self.d = d3dshot.create(capture_output="numpy", frame_buffer_size = 5)
        self.d.capture(target_fps=60, region=(left, top, left + 3840, top + 2160))
        if len(self.d.displays) > 1:
            self.d.display = self.d.displays[2]
            print(self.d.display)
        time.sleep(1)

    def get_screenshot(self):
        return self.d.get_latest_frame()[0:20, 0:5]
        return(cv2.cvtColor(self.d.get_latest_frame(), cv2.COLOR_RGB2BGR))


a = kekwCapture(0, 0)
print(a.get_screenshot())
# a.d.benchmark()
# th = Thread(target=kkk, args=())
# # И запускаем его
# th.start()

# kok = [
#     [[1,2,3],[1,4,2]],
# [[1,26,3],[1,41,2]]
# ]
# print(kok[0:1, 0:1, :, :])
input()
start = time.time()
while True:
    # time.sleep(1)
    kok = a.get_screenshot()

    print(time.time() - start)
    start = time.time()
    # time.sleep(0.03)

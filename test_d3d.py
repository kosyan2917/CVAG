import cv2
import d3dshot
import time
import numpy
import PIL

d = d3dshot.create(capture_output="numpy")

d.capture(target_fps = 30)
# time.sleep(5)  # Capture is non-blocking so we wait explicitely
# d.stop()
# time1 = 0
# while True:
#     print(time.time() - time1)
#     d.get_latest_frame()
#     time1 = time.time()

time.sleep(1)
kok0 = d.get_latest_frame()
kok0 = cv2.cvtColor(kok0, cv2.COLOR_RGB2BGR)
time1 = 0
while True:
    kok1 = d.get_latest_frame()
    kok1 = cv2.cvtColor(kok1, cv2.COLOR_RGB2BGR)
    # if not numpy.array_equal(kok0, kok1):
    #     kok0 = kok1
    #
    #     print(time.time() - time1)
    #     time1 = time.time()
    time.sleep(0.03)
    # cv2.imshow('adasf', kok)
    # cv2.waitKey(0)
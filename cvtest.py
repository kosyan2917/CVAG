import time

import cv2
import numpy as np
from WindowCapture import WindowCapture
import win32api
import win32con

def click_hold(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

def _get_green_channel(image): #delete later
    crystals = {
        "green": {  # ^
            "lower": [0, 223, 0],
            "upper": [0, 248, 0]
        },
        "lava": {  # ^
            "lower": [0, 0, 223],
            "upper": [0, 0, 248]
        },
        "ice": {  # ^
            "lower": [253, 254, 0],
            "upper": [253, 255, 34]  # if very 30,254,253
        },
        "purple": {  # ^
            "lower": [253, 1, 154],
            "upper": [254, 20, 238]
        },
    }
    lower = np.array(crystals["green"]["lower"])
    upper = np.array(crystals["green"]["upper"])
    mask = cv2.inRange(image, lower, upper)
    return mask

def play():
        #image = self.driver.get_screenshot_as_png()
        #data = np.fromstring(image, dtype=np.uint8)
        #image = cv2.imdecode(data, 1)
        image = cv2.imread("Testcases/green2.png")
        print(image)
        print(len(image))
        mask = _get_green_channel(image)
        coords = cv2.findNonZero(mask)
        print()
        min = 1000000000000
        target = ()
        for coord in coords:
            print(coord)
            num = (coord[0][0]-682)**2+(coord[0][1]-341)**2
            if num < min:
                min, target = num, (coord[0][0], coord[0][1])
        click_hold(*target)
        
def windows():
    print(WindowCapture.list_window_names())

def edge():
    while True:
        window = "Яндекс — Яндекс.Браузер"
        wincap = WindowCapture(window)
        screenshot = wincap.get_screenshot()
        cv2.imshow("window", screenshot)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

play()
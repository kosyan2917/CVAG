import time

import win32api
import win32con

from WindowCapture import WindowCapture
import cv2 as cv
import numpy as np

class AI:
    def __init__(self, window=None):
        self._previous_target = False
        self._previous_target_frames = 0
        self.wincap = WindowCapture()
        if window:
            self.window = window
        else:
            self.window = None
        self.crystals = {
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
                "lower": [253, 1, 122],
                "upper": [254, 20, 185]
            },
        }
    
    def play(self):
        while True:
            screenshot = self.wincap.get_screenshot()
            masks = [screenshot for i in range(4)]
            coords = self._get_channels(screenshot)
            if coords:
                target = self._nearest_crystals(coords)



                self.click_hold(*target)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 , 0)
            # mask1 = np.concatenate((masks[0], masks[1]), axis=1)
            # mask2 = np.concatenate((masks[2], masks[3]), axis=1)
            # res = np.concatenate((mask1, mask2), axis=0)
            #cv.imshow("ComputerVision", mask2)
             #   break
            cv.waitKey(1)
            
    def _get_green_channel(self, image):
        lower = np.array(self.crystals["green"]["lower"])
        upper = np.array(self.crystals["green"]["upper"])
        mask = cv.inRange(image, lower, upper)
        return mask
    
    def _get_channels(self, image):
        result = []
        seing = []
        for crystal in self.crystals:
            lower = np.array(self.crystals[crystal]["lower"])  # BGR-code of your lowest colour
            upper = np.array(self.crystals[crystal]["upper"])  # BGR-code of your highest colour
            mask = cv.inRange(image, lower, upper)
            coords = cv.findNonZero(mask)
            new_coords = []
            if coords is not None:
                if crystal == "purple":
                    for coord in coords:
                        if not (coord[0][0] <= 300 and coord[0][1] >= 780):
                            new_coords.append(coord)
                    if new_coords:
                        result.append(new_coords)
                        seing.append(crystal)
                        #print(new_coords)
                else:
                    result.append(coords)
                    seing.append(crystal)
                    #print(coords, crystal)
            #print(result, crystal)
        #print("Вижу:", seing)
        return result

    def _nearest_crystals(self, cords):
        x_offset = 955
        y_offset = 535
        min = 10000
        #print(cords, "cords")
        for mas in cords:
            #print(mas, type(mas), "mas")
            for cord in mas:
                path = abs(cord[0][0]-x_offset) + abs(cord[0][1]-y_offset)
                if path < min:
                    min, target = path, (cord[0][0], cord[0][1]+15)

        if self._previous_target != False:
            if abs(target[0] - self._previous_target[0]) > 30 and abs(target[1] - self._previous_target[1]) > 30 and self._previous_target_frames < 2:
                self._previous_target_frames += 1
                return self._previous_target
            else:
                self._previous_target_frames = 0
                self._previous_target = False
        return target

    def test_method(self):
        kaks = [[[1]]]
        sss = [[[3]]]
        print(kaks + sss)

    @staticmethod
    def click_hold(x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

            
            
if __name__ == "__main__":
    ai = AI()
    ai.test_method()
    ai.play()
from WindowCapture import WindowCapture
import cv2 as cv
import numpy as np

class AI:
    def __init__(self, window=None):
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
                "lower": [253, 1, 154],
                "upper": [254, 20, 238]
            },
        }
    
    def play(self):
        while True:
            screenshot = self.wincap.get_screenshot()
            masks = [screenshot for i in range(4)]
            #masks = self._get_channels(screenshot)
            mask1 = np.concatenate((masks[0], masks[1]), axis=1)
            mask2 = np.concatenate((masks[2], masks[3]), axis=1)
            res = np.concatenate((mask1, mask2), axis=0)
            cv.imshow("ComputerVision", res)
             #   break
            cv.waitKey(1)
            
    def _get_green_channel(self, image):
        lower = np.array(self.crystals["green"]["lower"])
        upper = np.array(self.crystals["green"]["upper"])
        mask = cv.inRange(image, lower, upper)
        return mask
    
    def _get_channels(self, image):
        masks = []
        for crystal in self.crystals:
            lower = np.array(self.crystals[crystal]["lower"])  # BGR-code of your lowest colour
            upper = np.array(self.crystals[crystal]["upper"])  # BGR-code of your highest colour
            masks.append(cv.inRange(image, lower, upper))
        return masks
        
            
            
if __name__ == "__main__":
    ai = AI()
    ai.play()
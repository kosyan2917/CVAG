import time

import win32api
import win32con
import threading
from selenium.webdriver import ActionChains

from WindowCapture import *
import cv2 as cv
import numpy as np


class AI:
    def __init__(self, driver, capture):
        self.driver = driver

        self.wincap = capture

        self.skipframes = 15

        self.crystals = {
            "green": {  # ^
                "lower": [37, 253, 60],
                "upper": [37, 253, 60]
            },
            # "lava": {  # ^daaaaaa
            #     "lower": [190, 2, 0],
            #     "upper": [248, 25, 25]
            # },
            # "ice": {  # ^d
            #     "lower": [34, 240, 240],
            #     "upper": [45, 254, 254]  # if very 30,254,253aa
            #     # [248 249  32]
            #     # [249 250  33]
            #     # da
            # },
            # "purple": {  # ^
            #     "lower": [122, 1, 247],
            #     "upper": [185, 37, 254]
            # },
        }
        self._player = (961, 542)
        self.action_key_down = {}
        self.action_key_up = {}
        self.action_key_down['w'] = ActionChains(driver).key_down("w")
        self.action_key_up['w'] = ActionChains(driver).key_up("w")
        self.action_key_down['a'] = ActionChains(driver).key_down("a")
        self.action_key_up['a'] = ActionChains(driver).key_up("a")
        self.action_key_down['s'] = ActionChains(driver).key_down("s")
        self.action_key_up['s'] = ActionChains(driver).key_up("s")
        self.action_key_down['d'] = ActionChains(driver).key_down("d")
        self.action_key_up['d'] = ActionChains(driver).key_up("d")

    def play_real(self):
        start = time.time()
        cyc_time = 0
        try:
            while True:
                cyc_time_reset = False


                screenshot = self.wincap.get_screenshot()
                # start1 = time.time()
                coords = self._get_channels(screenshot)
                # print("getcoords", time.time() - start1)
                if self.exit:
                    print('exit&&&&&&&&&&&&&&&&&&&&&&&&')
                    break
                if coords is not None:

                    target = self._nearest_crystals(coords)
                    cyc_time_reset = self._move(*target, cyc_time)
                else:
                    if self._previous_target != False:
                        if self._previous_target_frames < self.skipframes:
                            # print('иду к успеху')
                            self._previous_target_frames += 1
                            cyc_time_reset = self._move(*self._previous_target, cyc_time)
                        else:

                            self._previous_target_frames = 0
                            self._previous_target = False
                            # print('stop')
                            self._reveal_key()
                            self._key_pressed_now = False
                    else:
                        self._previous_target_frames = 0
                        self._previous_target = False
                        # print('stop')gob
                        try:
                            self._reveal_key()
                        except:
                            pass
                        self._key_pressed_now = False
                if cyc_time_reset:
                    cyc_time = 0
                else:
                    cyc_time = time.time() - start

                # print("FPS:", time.time() - start)
                start = time.time()


        except Exception as e:
            print('megaerror', e)
            self.errored_play = True
        print('вышел из потока')
    
    def play(self):
        self._previous_target = False
        self._previous_target_frames = 0
        self._key_pressed_now = False
        self.errored_play = False
        self.timer = 0
        self.exit = False
        threading.Thread(target=self.play_real, args=()).start()
        while True:
            if not self._is_playing():
                self.exit = True
                raise Exception('Game has broken')
            if self.errored_play:
                raise Exception('Game has broken2')
            time.sleep(1)
            
    def _is_playing(self):
        el = self.driver.find_elements_by_css_selector(".portal")
        if el:
            return False
        el = self.driver.find_elements_by_xpath("//*[contains(text(),'unexpected error')]")
        if el:
            print('found error')
            return False
        el = self.driver.find_elements_by_xpath("//*[contains(text(),'connect wallet')]")
        if el:
            print('found connect wallet')
            return False
        return True
    
    def _get_green_channel(self, image):
        lower = np.array(self.crystals["green"]["lower"])
        upper = np.array(self.crystals["green"]["upper"])
        mask = cv.inRange(image, lower, upper)
        return mask

    def _get_channels(self, image):
        result = []
        seing = []

        mask = self._get_green_channel(image)
        coords = cv.findNonZero(mask)


        return coords
        if self.current_color:
            crystal = self.current_color
            result[crystal] = []
            lower = np.array(self.crystals[crystal]["lower"])  # BGR-code of your lowest colour
            upper = np.array(self.crystals[crystal]["upper"])  # BGR-code of your highest colour
            mask = cv.inRange(image, lower, upper)
            coords = cv.findNonZero(mask)
            new_coords = []
            if coords is not None:
                if crystal == "purple":
                    for coord in coords:
                        if not (coord[0][0] <= 300 and coord[0][1] >= 775):
                            new_coords.append(coord)
                    if new_coords:
                        result[crystal].append(new_coords)
                        seing.append(crystal)
                        # print(new_coords)
                else:
                    result[crystal].append(coords)
                    seing.append(crystal)
        else:
            for crystal in self.crystals:
                result[crystal] = []
                lower = np.array(self.crystals[crystal]["lower"])  # BGR-code of your lowest colour
                upper = np.array(self.crystals[crystal]["upper"])  # BGR-code of your highest colour
                mask = cv.inRange(image, lower, upper)
                coords = cv.findNonZero(mask)
                new_coords = []
                if coords is not None:
                    if crystal == "purple":
                        for coord in coords:
                            if not (coord[0][0] <= 300 and coord[0][1] >= 775):
                                new_coords.append(coord)
                        if new_coords:
                            result[crystal].append(new_coords)
                            seing.append(crystal)
                            # print(new_coords)
                    else:
                        result[crystal].append(coords)
                        seing.append(crystal)
                        # print(coords, crystal)a
                # print(result, crystal)
        print('вижу', seing)
        return result

    def _nearest_crystals(self, cords):
        x_offset, y_offset = self._player[0], self._player[1]
        min = 10000
        # print(cords, "cords")

        for cord in cords:
            path = abs(cord[0][0] - x_offset) + abs(cord[0][1] - y_offset)
            if path < min:
                min, target = path, (cord[0][0], cord[0][1] + 15)


        if self._previous_target != False:
            if abs(target[0] - self._previous_target[0]) > 30 and abs(
                    target[1] - self._previous_target[1]) > 30 and self._previous_target_frames < self.skipframes:
                self._previous_target_frames += 1
                return self._previous_target
            else:
                self._previous_target_frames = 0
                self._previous_target = False
        self._previous_target = target
        self._previous_target_frames = 0
        return target


    def _move(self, x, y, cyc_time):
        x_distance = x - self._player[0]
        y_distance = y - self._player[1]
        abs_x_distance = abs(x_distance)
        abs_y_distance = abs(y_distance)
        if (abs_x_distance < 100 and abs_y_distance < 100):
            self.timer += cyc_time
        else:
            self.timer = 0
        if self.timer > 10:
            self._unstuck(x_distance, y_distance)
            return True
        else:
            # if 8 < abs_y_distance < 300:
            #     if y_distance > 8:
            #         key_to_press = 's'
            #     else:
            #         key_to_press = 'w'
            # elif 8 < abs_x_distance < 300:
            #     if x_distance > 8:
            #         key_to_press = 'd'
            #     else:
            #         key_to_press = 'a'
            if abs_x_distance > abs_y_distance:
                if x_distance > 0:
                    key_to_press = 'd'
                else:
                    key_to_press = 'a'
            else:
                if y_distance > 0:
                    key_to_press = 's'
                else:
                    key_to_press = 'w'



            if self._key_pressed_now:
                if self._key_pressed_now != key_to_press:
                    self._reveal_key()
                    self.action_key_down[key_to_press].perform()
                    self._key_pressed_now = key_to_press
            else:
                self.action_key_down[key_to_press].perform()
                self._key_pressed_now = key_to_press
            return False

    def _reveal_key(self):
        # win32api.keybd_event(self._key_pressed_now, 0, win32con.KEYEVENTF_KEYUP, 0)
        self.action_key_up[self._key_pressed_now].perform()

    def _hold_key(self, key_to_press, time_to_hold):
        run_time = 15
        self.action_key_down[key_to_press].perform()
        time.sleep(time_to_hold * run_time)
        self.action_key_up[key_to_press].perform()

    def _unstuck(self, x_distance, y_distance):
        if -x_distance > 0:
            key_to_press_x = 'd'
        else:
            key_to_press_x = 'a'

        if -y_distance > 0:
            key_to_press_y = 's'
        else:
            key_to_press_y = 'w'

        x_abs = abs(x_distance)
        y_abs = abs(y_distance)
        self._hold_key(key_to_press_x, x_abs / (x_abs + y_abs))
        self._hold_key(key_to_press_y, y_abs / (x_abs + y_abs))

        self._previous_target = False
        self._previous_target_frames = 0
        print('stop')
        self._key_pressed_now = False


if __name__ == "__main__":
    ai = AI()
    ai.play()
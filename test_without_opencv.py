import time
from multiprocessing import Process
import win32api
import win32con
import concurrent.futures

from WindowCapture import *
# from  linuxWindowCapture import *
import cv2 as cv
import numpy as np

# from pymouse import *
# # from schedule import every, repeat, run_pending
#
# m = PyMouse ()


VK_CODE = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'F1': 0x70,
           'F2': 0x71,
           'F3': 0x72,
           'F4': 0x73,
           'F5': 0x74,
           'F6': 0x75,
           'F7': 0x76,
           'F8': 0x77,
           'F9': 0x78,
           'F10': 0x79,
           'F11': 0x7A,
           'F12': 0x7B,
           'F13': 0x7C,
           'F14': 0x7D,
           'F15': 0x7E,
           'F16': 0x7F,
           'F17': 0x80,
           'F18': 0x81,
           'F19': 0x82,
           'F20': 0x83,
           'F21': 0x84,
           'F22': 0x85,
           'F23': 0x86,
           'F24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           '`': 0xC0,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE,
           '`': 0xC0}

count = cv2.cuda.getCudaEnabledDeviceCount()
print(count)
class AI:
    def __init__(self):
        # self.driver = driver
        self._previous_target = False
        self._previous_target_frames = 0
        self._key_pressed_now = False
        self.wincap = kekwCapture()
        self.timer = 0
        self.crystals = {
            "green": {  # ^
                "lower": [0, 220, 0],
                "upper": [40, 248, 60]
            },
            "lava": {  # ^daaaaaa
                "lower": [190, 2, 0],
                "upper": [248, 25, 25]
            },
            "ice": {  # ^d
                "lower": [34, 240, 240],
                "upper": [45, 254, 254]  # if very 30,254,253aa
                # [248 249  32]
                # [249 250  33]
                # da
            },
            "purple": {  # ^
                "lower": [122, 1, 247],
                "upper": [185, 37, 254]
            },
        }
        self._player = (961, 542)
        # m.move(-1920 + self._player[0], self._player[1])

    def run_cpu_tasks_in_parallel(self, tasks):
        res = np.array([])
        running_tasks = [Process(target=task) for task in tasks]
        for running_task in running_tasks:
            running_task.start()
        for running_task in running_tasks:
            running_task.join()
            # np.append(res, running_task.join())
        return res


    def play(self):
        start = time.time()
        cyc_time = 0
        while True:
            screenshot = self.wincap.get_screenshot()
            # cv.imshow('asdasd', screenshot)
            # if cv2.waitKey(1) == ord('q'):
            #     cv2.destroyAllWindows()
            #     break
            print('src', time.time() - start)
            coords = self._get_channels(screenshot)

            # if not self._is_playing():
            #     raise Exception('Game has broken')
            if coords:
                print()
                print(screenshot[coords[0][0][0][1]][coords[0][0][0][0]])
                target = self._nearest_crystals(coords)
                self._move(*target, cyc_time)
            else:
                if self._previous_target != False:
                    if self._previous_target_frames < 5:
                        print('иду к успеху')
                        self._previous_target_frames += 1
                        self._move(*self._previous_target, cyc_time)
                    else:

                        self._previous_target_frames = 0
                        self._previous_target = False

                        self._previous_target_frames = 0
                        self._previous_target = False
                        self._reveal_key()
                        self._key_pressed_now = False
            cyc_time = time.time() - start

            print("FPS:", time.time() - start)
            start = time.time()

            # mask1 = np.concatenate((masks[0], masks[1]), axis=1)
            # mask2 = np.concatenate((masks[2], masks[3]), axis=1)
            # res = np.concatenate((mask1, mask2), axis=0)
            # cv.imshow("ComputerVision", mask2)
            #   break

    # def _is_playing(self):
    #     el = self.driver.find_elements_by_xpath(".//img[@class='jsx-653981903 portal ']")
    #     if el:
    #         return False
    #     return True

    def _get_green_channel(self, image):
        lower = np.array(self.crystals["green"]["lower"])
        upper = np.array(self.crystals["green"]["upper"])
        mask = cv.inRange(image, lower, upper)
        return mask

    def _get_channels(self, image):
        result = []
        seing = []

        t1 = time.time()
        # hue = image[..., 0]

        (rows1, cols1) = np.where(np.logical_and(np.logical_and(np.logical_and(image[..., 0] >= 0, image[..., 0] <= 40),
                                                 np.logical_and(image[..., 2] >= 0, image[..., 2] <= 60)),
                                                 np.logical_and(image[..., 1] >= 0, image[..., 1] <= 40)))
        print(rows1, cols1)
        # print(hue)
        print(time.time() - t1)
        input()

        t1 = time.time()
        future = []
        for crystal in self.crystals:

            lower = np.array(self.crystals[crystal]["lower"])  # BGR-code of your lowest colour
            upper = np.array(self.crystals[crystal]["upper"])  # BGR-code of your highest colour

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future.append(executor.submit(lambda image, lower, upper: cv.findNonZero(cv.inRange(image, lower, upper)), image, lower, upper))


        for x in future:
            return_value = x.result()
            print(return_value)
        print(time.time() - t1)
        input()
            # mask = cv.inRange(image, lower, upper)
            # coords = cv.findNonZero(mask)
            # new_coords = []
            # if coords is not None:
            #     if crystal == "purple":
            #         for coord in coords:
            #             if not (coord[0][0] <= 300 and coord[0][1] >= 775):
            #                 new_coords.append(coord)
            #         if new_coords:
            #             result.append(new_coords)
            #             seing.append(crystal)
            #             print(new_coords)
            #     else:
            #         result.append(coords)
            #         seing.append(crystal)
                    # print(coords, crystal)
            # print(result, crystal)

        print("Вижу:", seing)
        return result

    def _nearest_crystals(self, cords):
        x_offset, y_offset = self._player[0], self._player[1]
        min = 10000
        # print(cords, "cords")
        for mas in cords:
            # print(mas, type(mas), "mas")
            for cord in mas:
                path = abs(cord[0][0] - x_offset) + abs(cord[0][1] - y_offset)
                if path < min:
                    min, target = path, (cord[0][0], cord[0][1] + 15)

        if self._previous_target != False:
            if abs(target[0] - self._previous_target[0]) > 30 and abs(
                    target[1] - self._previous_target[1]) > 30 and self._previous_target_frames < 4:
                self._previous_target_frames += 1
                return self._previous_target
            else:
                self._previous_target_frames = 0
                self._previous_target = False
        self._previous_target = target
        self._previous_target_frames = 0
        return target

    def test_method(self):
        kaks = [[[1]]]
        sss = [[[3]]]
        print(kaks + sss)

    def _move(self, x, y, cyc_time):
        x_distance = x - self._player[0]
        y_distance = y - self._player[1]
        if (abs(x_distance) < 100 and abs(y_distance < 100)):
            self.timer += cyc_time
        else:
            self.timer = 0
        if self.timer > 10:
            self._unstuck(x_distance, y_distance)
        else:
            # if self._key_pressed_now:
            #     if self._key_pressed_now == VK_CODE['d'] or self._key_pressed_now == VK_CODE['a']:
            #         if abs(x_distance) > 40:
            #             return
            #     else:
            #         if abs(y_distance) > 40:
            #             return
            if abs(x_distance) > abs(y_distance):
                if x_distance > 0:
                    key_to_press = VK_CODE['d']
                else:
                    key_to_press = VK_CODE['a']
            else:
                if y_distance > 0:
                    key_to_press = VK_CODE['s']
                else:
                    key_to_press = VK_CODE['w']

            # if abs(x_distance) < abs(y_distance):
            #     if y_distance > 0:
            #         key_to_press = VK_CODE['s']
            #     elif y_distance < 0:
            #         key_to_press = VK_CODE['w']
            # else:
            #
            #     if y_distance > 40:
            #         key_to_press = VK_CODE['s']
            #     elif y_distance < -40:
            #         key_to_press = VK_CODE['w']
            #     elif x_distance > 8:
            #         key_to_press = VK_CODE['d']
            #     else:
            #         key_to_press = VK_CODE['a']

            if self._key_pressed_now:
                if self._key_pressed_now != key_to_press:
                    self._reveal_key()
                    win32api.keybd_event(key_to_press, 0, 0, 0)
                    self._key_pressed_now = key_to_press
            else:
                win32api.keybd_event(key_to_press, 0, 0, 0)
                self._key_pressed_now = key_to_press

    def _reveal_key(self):
        win32api.keybd_event(self._key_pressed_now, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _hold_key(self, key_to_press, time_to_hold):
        run_time = 10
        win32api.keybd_event(key_to_press, 0, 0, 0)
        time.sleep(time_to_hold * run_time)
        win32api.keybd_event(key_to_press, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _unstuck(self, x_distance, y_distance):
        if -x_distance > 0:
            key_to_press_x = VK_CODE['d']
        else:
            key_to_press_x = VK_CODE['a']

        if -y_distance > 0:
            key_to_press_y = VK_CODE['s']
        else:
            key_to_press_y = VK_CODE['w']

        x_abs = abs(x_distance)
        y_abs = abs(y_distance)
        self._hold_key(key_to_press_x, x_abs / (x_abs + y_abs))
        self._hold_key(key_to_press_y, y_abs / (x_abs + y_abs))
        self.timer = 0


if __name__ == "__main__":
    ai = AI()
    ai.test_method()
    ai.play()
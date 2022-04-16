from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from multiprocessing import Pool
from io import BytesIO
from PIL import Image
import time, cv2, json, copy, numpy as np
from fake_useragent import UserAgent
from collections import defaultdict
from WindowCapture import WindowCapture

class Selenium:
    def __init__(self) -> None:
        pass

    def start_driver(self):
        options = webdriver.FirefoxOptions()

        options.set_preference("general.useragent.override", UserAgent().firefox)
        options.set_preference('intl.accept_languages', 'en-US, en')
        # options.add_argument("--headless")
        # fp = webdriver.FirefoxProfile(r'C:\Users\den\AppData\Roaming\Mozilla\Firefox\Profiles\p84efvee.vegotchi1')
        driver = webdriver.Firefox(
            executable_path="utils\\geckodriver.exe",
            options=options
        )
        self.driver = driver
        self.ac = ActionChains(driver)
        return driver

    def take_element(self, path, timeout=20, delay=0):
        element = ""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(("css selector", path)))
        except Exception as e:
            print(f"No element after {timeout} seconds of waiting!!!")
            return None
        if element is not None:
            time.sleep(delay)
            return element
        else: print(f"NO SUCH ELEMENT!\n Path: {path}")
        self.driver.execute_script("""document.body.style.backgroundColor = 'green'""")
        input()

    def del_extra_element(self, path):
        self.driver.execute_script(f'document.querySelector("{path}").remove();')

    def send_keys_delay(element, string, delay=0):
        for character in string:
            element.send_keys(character)
            time.sleep(delay)

    def hold_key(self, key, delay=0):
        ac = ActionChains(self.driver)
        ac.key_down(key).pause(delay).key_up(key).perform()


class Metamask(Selenium):
    def __init__(self, mnemonic, password, driver) -> None:
        self.mnemonic = mnemonic
        self.password = password
        self.driver = driver
    
    def install(self, url):
        self.driver.install_addon(url, temporary=True)
    
    def restore_wallet(self):
        self.take_element("button").click()  # enter mm
        self.take_element("button").click()  # choose restoration by mnemonic
        self.take_element("button").click()  # don't send telemetry
        self.take_element("input").send_keys(self.mnemonic)  # put mnemonic
        self.take_element("#password").send_keys(self.password)  # put password
        self.take_element("#confirm-password").send_keys(self.password)  # repeat password
        self.take_element(".first-time-flow__terms").click()  # agree terms
        self.take_element("button").click()  # login to mm
        self.take_element("button[role='button']").click()  # access invitation
    
    def add_network(self, network, rpc, chain_id, currency, explorer):
        self.driver.get(self.driver.current_url.split('#')[0] + "#settings/networks/add-network")
        network_inputs = self.take_element(".networks-tab__add-network-form-body").find_elements("css selector",
                                                                                                 ".form-field__input")
        Metamask.send_keys_delay(network_inputs[0], network)
        Metamask.send_keys_delay(network_inputs[1], rpc)
        Metamask.send_keys_delay(network_inputs[2], chain_id)
        Metamask.send_keys_delay(network_inputs[3], currency)
        Metamask.send_keys_delay(network_inputs[4], explorer)
        self.take_element("button.button:nth-child(2)").click()  # save network
        time.sleep(2)
        
class Aavegotchi(Metamask):
    def __init__(self, driver, profile_name) -> None:
        self.driver = driver
        self.profile_name = str(profile_name)
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
        self.window = "Play | Gotchiverse — Mozilla Firefox"
        
        
    
    def go_to_site(self):
        self.driver.get("https://verse.aavegotchi.com/")
        return self
    
    def login(self):
        print("Login")
        time.sleep(2)
        # input("Press Enter to continue...")
        connect_mm = self.take_element(".retro-border > button", timeout=10, delay=1) # connect mm
        if not connect_mm: return
        connect_mm.click()
        choose_mm = self.take_element('.wallet-card', timeout=10,  delay=1)
        if not choose_mm: return
        choose_mm.click() # choose mm
        time.sleep(3)
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1]) # go to mm window
            self.take_element('.btn-primary').click() # confirm mm
            self.take_element('.btn-primary').click() # confirm double mm
            self.driver.switch_to.window(self.driver.window_handles[0]) # go to main window
    
    
    def prepare_game(self):
        self._turn_off_everything()
        self.take_element('.lazyload-wrapper').click() # choose aavegotchi
        for i in range(4):
            portal = self.take_element('.selected-gotchi-container', delay=1) # choose portal
            portal.click() # go to portal
            self.driver.switch_to.window(self.driver.window_handles[1])# go to mm window
            self.take_element('.btn-primary').click() # sign mm
            self.driver.switch_to.window(self.driver.window_handles[0])# go to main window
            time.sleep(15)
            upd_portal = self.take_element('.selected-gotchi-container', timeout=0.5)
            if upd_portal is None:
                return True
    
    def _turn_off_everything(self):
        settings = self.driver.find_element_by_xpath(".//button") #Поиск настроек
        settings.click()
        checkboxes = self.driver.find_elements_by_xpath(".//span[@class='jsx-1081654359 slider']") #Вырубаем все
        for checkbox in checkboxes:
            checkbox.click()
        exit = self.driver.find_element_by_xpath(".//button[@class='jsx-3937147940 button-container   ']") #Выходим
        exit.click()
    
    def is_game_loaded(self):
        return bool(self.take_element(".input[value='35']", 100, delay=10)) # check for loading game
    
    def increase_vision(self):
        self.increase_measure()
        extra_dom_elements = [".top-left-container", ".pocket-container", ".top-right-container", ".action-button-container", ".bottom-right-container"]
        for el in extra_dom_elements:
            self.del_extra_element(el)
    
    def increase_measure(self):
        measure_input = self.take_element("input[type='range']")
        time.sleep(7)
        ac = ActionChains(self.driver)
        ac.click_and_hold(measure_input).move_by_offset(0, 120).release().perform()
        time.sleep(7)
    
    def timetest(self, image):
        sum = 0
        for i in range(100):
            start = time.time()
            self._get_crystals_locations(image)
            res = time.time() - start
            sum += res
        print(f"Tested:", sum / 100)
    
    def _get_crystals_locations(self, image):
        data = np.fromstring(image, dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        crystal_locations = []
        for crystal in self.crystals:
            lower = np.array(self.crystals[crystal]["lower"])  # BGR-code of your lowest colour
            upper = np.array(self.crystals[crystal]["upper"])  # BGR-code of your highest colour
            # print(crystal)
            mask = cv2.inRange(image, lower, upper)
            coord = cv2.findNonZero(mask)
            if coord is not None:
                for i in range(len(coord)):
                    crystal_locations.append(coord[i][0].tolist())
                    print(crystal, coord[i][0])
        return crystal_locations
    
    def _get_green_channel(self, image): #delete later
        lower = np.array(self.crystals["green"]["lower"])
        upper = np.array(self.crystals["green"]["upper"])
        mask = cv2.inRange(image, lower, upper)
        return mask
    
    @staticmethod
    def nearest_crystal(coords):
        min = 1000000000000
        target = ()
        for coord in coords:
            print(coord)
            num = (coord[0][0] - 682) ** 2 + (coord[0][1] - 341) ** 2
            if num < min:
                min, target = num, (coord[0][0], coord[0][1])
        return target
        
    def _click(self, x, y):
        self.ac.move_to_element_with_offset(self.driver.find_element_by_tag_name('body'), 0,0)
        self.ac.move_by_offset(x,y).click_and_hold().perform()
        time.sleep(0.1)
        self.ac.release().perform()
    
    def play(self):
        start = time.time()
        while True:
            start
            image = self.driver.get_screenshot_as_png()
            data = np.fromstring(image, dtype=np.uint8)
            image = cv2.imdecode(data, 1)
            mask = self._get_green_channel(image)
            coord = cv2.findNonZero(mask)
            if coord is not None:
                self._click(*self.nearest_crystal(coord))
            print(time.time()-start)
            start = time.time()
            
def worker(account):
    profile_name, mnemonic, password = account
    print("Start with:", profile_name, mnemonic, password)
    
    while True:
        try:
            driver_session = Selenium()
            driver = driver_session.start_driver()
            metamask = Metamask(mnemonic, password, driver)
            metamask.install(r"D:\Nik\aavegotchiBot\utils\MetaMask.xpi")
            driver.close()  # close starter blank page
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])  # switch to mm window
            print("MetaMask was started")
            metamask.restore_wallet()
            print("add Polygon")
            metamask.add_network("Matic Mainnet", "https://rpc-mainnet.maticvigil.com/", "137", "MATIC",
                                 "https://explorer.matic.network/")
            print("Polygon added")
            break
        except Exception as e:
            print(e)
    aavegotchi = Aavegotchi(driver, profile_name)
    
    while True:
        # try:
        aavegotchi.go_to_site().login()
        if not aavegotchi.prepare_game():
            continue
        print("Aavegotchi go to portal")
        if not aavegotchi.is_game_loaded():
            print("Game Not loaded")
            continue
        print("Aavegotchi loaded")
        aavegotchi.increase_vision()
        aavegotchi.play()
        cv2.waitKey(0)
        if not aavegotchi.is_crystals_airdrop():
            continue
        print("Aavegotchi airdrop")
        
        aavegotchi.play_game()
        
        input("GG WP...")
    # except Exception as e:
    #   print(e)

def make_list_from_file(file):
  with open(file, 'r') as f:
    return [x for x in f.read().split("\n") if x]

if __name__ == "__main__":
    mnemonics = make_list_from_file("accounts.txt")
    accounts = [(str(i + 1), mnemonics[i], "vegotchi" + str(i + 1)) for i in range(len(mnemonics))]
    print(accounts)
    p = Pool(processes=len(accounts))
    p.map(worker, accounts)
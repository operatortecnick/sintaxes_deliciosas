from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent

@dataclass
class InstagramAccount:
    email: str
    name: str
    username: str
    password: str

class InstagramBot:
    def __init__(self, proxy: Optional[str] = None, headless: bool = False):
        self.proxy = proxy
        self.headless = headless
        self.driver = self._init_driver()

    def _init_driver(self) -> webdriver.Chrome:
        ua = UserAgent()
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if self.proxy:
            options.add_argument(f"--proxy-server={self.proxy}")
        return webdriver.Chrome(options=options)

    def create_account(self, account: InstagramAccount) -> None:
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        wait = WebDriverWait(driver, 15)

        try:
            wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
            driver.find_element(By.NAME, "emailOrPhone").send_keys(account.email)
            driver.find_element(By.NAME, "fullName").send_keys(account.name)
            driver.find_element(By.NAME, "username").send_keys(account.username)
            driver.find_element(By.NAME, "password").send_keys(account.password)
            time.sleep(2)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        except Exception as exc:  # pragma: no cover - purely integration
            raise RuntimeError(f"Failed to fill the form: {exc}")

    def close(self) -> None:
        if self.driver:
            self.driver.quit()

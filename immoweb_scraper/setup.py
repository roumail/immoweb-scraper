from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def browser_setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    return browser


def page_setup(browser: WebDriver, webpage_url: str):
    # Open webpage
    browser.get(webpage_url)

    WebDriverWait(browser, 4)

    # wait and click privacy.. only the first time browser page opened
    # every other time, we skip this part
    try:
        browser.find_element(By.XPATH, "//button[@id='uc-btn-accept-banner']").click()
    except NoSuchElementException:
        pass
    return

from selenium import webdriver
from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def browser_setup():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    return browser


def page_setup(browser: WebDriver, webpage_url: str):
    # Open webpage
    browser.get(webpage_url)

    WebDriverWait(browser, 4)

    # wait and click privacy.. only the first time browser page opened
    # the button itself has the id "//button[@data-testid='uc-accept-all-button']"
    ok_button = browser.execute_script(
        'return document.querySelector("#usercentrics-root").shadowRoot.querySelector("#uc-center-container > div.sc-eBMEME.ixkACg > div > div.sc-jsJBEP.bHqEwZ > div > div > button.sc-dcJsrY.gwuZOI");'
    )
    if ok_button:
        ok_button.click()

    # Wait until the overflow box is hidden
    wait = WebDriverWait(browser, 10)
    wait.until_not(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#usercentrics-root"))
    )
    return

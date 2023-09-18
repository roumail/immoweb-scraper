from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def browser_setup():
    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    # exe_path = r"C:\UCB\learnings\scraping-test\geckodriver.exe"
    # # Browser setup
    # profile = webdriver.FirefoxProfile()
    # profile.accept_untrusted_certs = True
    # browser = webdriver.Firefox(firefox_profile=profile, executable_path=exe_path)
    # # Add implicit wait
    # browser.implicitly_wait(7)  # seconds
    return browser


def page_setup(browser, web_page):
    # Open webpage
    browser.get(web_page)

    browser.implicitly_wait(4)  # seconds

    # wait and click privacy.. only the first time browser page opened
    # every other time, we skip this part
    try:
        browser.find_element_by_xpath("//button[@id='uc-btn-accept-banner']").click()
    except NoSuchElementException:
        pass
    return

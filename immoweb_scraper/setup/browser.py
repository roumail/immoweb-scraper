from selenium import webdriver


def browser_setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    return browser

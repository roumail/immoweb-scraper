import pandas as pd
from loguru import logger
from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from immoweb_scraper.scrape.parse import parse_link_element


def click_accept_banner(browser: WebDriver, webpage_url: str):
    # Open webpage
    browser.get(webpage_url)
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


def retrieve_page_links(browser: "WebDriver") -> pd.Series:
    # , location_a_list: list[int], max_price: float
    elements = browser.find_element(
        By.CLASS_NAME, "search-results__list"
    ).find_elements(By.XPATH, ".//li[@class='search-results__item']")

    rows = []
    for i, element in enumerate(elements):
        base = element.find_elements(By.CLASS_NAME, "card--result__body")
        if not base:
            continue
        #  isinstance(base, list) and len(base) == 1
        else:
            base = next(iter(base))
            parsed = parse_link_element(base)
            logger.debug(
                f"Parsed property number {i + 1} on page with identifier: {parsed['immoweb_identifier']}"
            )
        rows.append(parsed)
    return rows

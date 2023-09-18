import typing as tp
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from immoweb_scraper.parse import retrieve_page_links
from immoweb_scraper.setup import page_setup
from immoweb_scraper.url import build_url

if tp.TYPE_CHECKING:
    from selenium.webdriver import Chrome as WebDriver


def scrape(browser: "WebDriver"):
    ## PARAMETERS ##
    # check online the last page and update...
    web_page = build_url()
    page_num = 1
    url = web_page.format(str(page_num))
    # Handle the clicking of privacy if needed
    page_setup(browser, url)
    collection = []
    max_pages = 25
    # location_a_list = [1030,1040,1050,1060,1150,1180,1190,1200]
    # max_price = 1300
    for page_i in range(max_pages):
        # if page_i == 2:
        #     break
        try:
            _info = retrieve_page_links(browser)
            collection.extend(_info)
            # preparation for next page..
            page_num += 1
            new_url = web_page.format(str(page_num))
            sleep(5)
            page_setup(browser, new_url)
        except NoSuchElementException:
            break
    return collection

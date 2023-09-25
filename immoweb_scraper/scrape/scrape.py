import typing as tp

import pandas as pd
from loguru import logger
from selenium.common.exceptions import NoSuchElementException

from immoweb_scraper.scrape.locators import click_accept_banner, retrieve_page_links

if tp.TYPE_CHECKING:
    from selenium.webdriver import Chrome as WebDriver


def scrape(
    browser: "WebDriver", url_builder_method: tp.Callable[[str], str]
) -> pd.DataFrame:
    collection = []
    max_pages = 99
    for page_i in range(1, max_pages + 1):
        logger.debug(f"Scraping page number {page_i}")
        url = url_builder_method(page=str(page_i))
        # Handle the clicking of privacy if needed
        click_accept_banner(browser, url)
        # if page_i == 2:
        #     break
        try:
            _info = retrieve_page_links(browser)
            collection.extend(_info)
            # preparation for next page..
        except NoSuchElementException:
            logger.info(f"Stopped at page {page_i}")
            break
    df = pd.concat(collection, axis="columns").T
    return df
import typing as tp

import pandas as pd
from selenium.common.exceptions import NoSuchElementException

from immoweb_scraper.parse import retrieve_page_links
from immoweb_scraper.setup import click_accept_banner

if tp.TYPE_CHECKING:
    from selenium.webdriver import Chrome as WebDriver


def scrape(
    browser: "WebDriver", url_builder_method: tp.Callable[[str], str]
) -> pd.DataFrame:
    collection = []
    max_pages = 25
    for page_i in range(1, max_pages + 1):
        url = url_builder_method(page=str(page_i))
        if page_i == 1:
            # Handle the clicking of privacy if needed
            click_accept_banner(browser, url)
        # if page_i == 2:
        #     break
        try:
            _info = retrieve_page_links(browser)
            collection.extend(_info)
            # preparation for next page..
        except NoSuchElementException:
            break
    breakpoint()
    df = pd.concat(collection, axis="columns").T
    return df

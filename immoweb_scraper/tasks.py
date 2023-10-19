import datetime
import typing as tp

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger

from immoweb_scraper.batcher.PostalCodeBatcher import PostalCodeBatcher
from immoweb_scraper.db.addition import add_properties
from immoweb_scraper.models import PurchaseProperty, RentalProperty, to_property
from immoweb_scraper.scrape.scrape import parse_card_element


# TODO: This is a continuously running task
def get_postal_codes(initial_index) -> tuple[list[str], int]:
    batcher = PostalCodeBatcher(initial_index)
    batches = batcher.get_next_batch()
    new_index = batcher.get_current_index()
    return batches, new_index


# TODO: This is a task to be performed after the successful scraping of rental and purchase properties
def add_to_db(rent_df: pd.DataFrame, sale_df: pd.DataFrame, db_conn, today_date: str):
    # add today date to both dataframes
    current_time_dt = datetime.datetime.strptime(today_date, "%Y-%m-%d-%H:%M:%S")
    today = current_time_dt.strftime("%Y-%m-%d")
    rent_df.loc[:, "collection_date"] = today
    sale_df.loc[:, "collection_date"] = today
    rental_properties = [
        to_property(row, RentalProperty) for _, row in rent_df.iterrows()
    ]
    sale_properties = [
        to_property(row, PurchaseProperty) for _, row in sale_df.iterrows()
    ]
    # TODO: Add a separate task for the saving of the state
    add_properties(db_conn, rental_properties, sale_properties)


def scrape(url_builder_method: tp.Callable[[str], str]) -> pd.DataFrame:
    collection = []
    max_pages = 99
    for page_i in range(1, max_pages + 1):
        logger.debug(f"Scraping page number {page_i}")
        url = url_builder_method(page=str(page_i))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_div = soup.find("div", {"class": "container-main-content"}).find(
            "div", {"class": "results"}
        )
        cards = main_div.find_all("iw-search-card-rendered")
        if not cards:
            logger.info(f"No more results found on page {page_i}")
            break
        for card in cards:
            parsed = parse_card_element(card)
            collection.append(parsed)
    df = pd.concat(collection, axis="columns").T
    return df

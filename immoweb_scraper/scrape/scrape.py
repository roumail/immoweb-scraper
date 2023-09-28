import json
import re
import typing as tp

import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from loguru import logger
from prefect import task


def parse_card_element(card: Tag) -> pd.Series:
    link = card.find("h2").find("a")["href"]
    app_type = card.find("h2", {"class": "card__title"}).text.strip()
    price_json_str = card.find("p", {"class": "card--result__price"}).find("iw-price")[
        ":price"
    ]
    price_dict = json.loads(price_json_str)
    main_price = price_dict.get("mainValue", None)
    additional_value = price_dict.get("additionalValue", None)
    price = (main_price, additional_value)

    # Extracting space in square meters and bedrooms
    property_info = card.find(
        "p",
        {
            "class": "card__information card--result__information card__information--property"
        },
    )
    beds, space = None, None
    if property_info:
        beds_text, space_text = property_info.text.split("·")
        beds = (
            int(re.findall(r"(\d+)", beds_text)[0])
            if re.findall(r"(\d+)", beds_text)
            else None
        )
        space = int(re.sub(r"[^\d]+", "", space_text.strip())) if space_text else None
    space = (beds, space)

    # Extracting commune
    locality_info = card.find(
        "p",
        {
            "class": "card__information card--results__information--locality card__information--locality"
        },
    )
    commune = None
    if locality_info:
        commune_text = locality_info.text.split()[0]
        commune = int(re.sub(r"[^\d]+", "", commune_text)) if commune_text else None

    out = {
        "immoweb_identifier": link.split("/")[-1],
        "build_type": app_type,
        "link": link,
        "price": price,
        "commune": commune,
        "space": space,
    }
    return pd.Series(out)


@task
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

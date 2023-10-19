import json
import re

import pandas as pd
from bs4.element import Tag


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

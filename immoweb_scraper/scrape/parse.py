import re
import typing as tp

import pandas as pd
from selenium.webdriver.common.by import By

if tp.TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


def parse_link_element(element: "WebElement"):
    link = element.find_element(By.XPATH, ".//h2/a").get_attribute("href")
    app_type = element.find_element(By.XPATH, ".//h2/a").text
    price = element.find_element(
        By.XPATH, ".//p[contains(@class,'card--result__price')]"
    ).text
    other_info = element.find_elements(By.XPATH, ".//div/p")
    space, location = tuple(map(lambda x: x.text, other_info))
    out = pd.Series(
        {
            "immoweb_identifier": link.split("/")[-1],
            "build_type": app_type,
            "link": link,
            "price": clean_price(price),
            "commune": int(re.sub(r"[^\d]+", "", location)) if location else None,
            "space": clean_space(space) if space else tuple([None, None]),
        }
    )

    return out


def clean_price(p) -> tuple[int, int]:
    "Remove , otherwise breaks"
    price = re.sub(",", "", p).split("\n")[0]
    prices = re.findall(r"€(\d{2,4})", price)
    prices = tuple(map(int, prices))
    # Ensure the tuple has exactly two values
    while len(prices) < 2:
        prices += (None,)

    return prices[:2]


def clean_space(p) -> tuple[int, int]:
    beds, sq_m = p.split("·")
    beds_matches = re.findall(r"(\d)\sbedrooms", beds.lower())
    beds = beds_matches[0] if beds_matches else None
    sq_m = int(re.sub(r"[^\d]+", "", sq_m))
    return beds, sq_m

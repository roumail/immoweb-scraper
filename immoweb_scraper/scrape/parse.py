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
            "build_type": app_type,
            "link": link,
            "price": clean_price(price),
            "commune": int(re.sub(r"[^\d]+", "", location)) if location else location,
            "space": clean_space(space) if space else space,
        }
    )

    return out


def clean_price(p):
    "Remove , otherwise breaks"
    price = re.sub(",", "", p).split("\n")[0]
    prices = re.findall(r"€(\d{2,4})", price)
    return list(map(int, prices))


def clean_space(p):
    beds, sq_m = p.split("·")
    beds = re.findall(r"(\d)\sbedrooms", beds)[0]
    sq_m = int(re.sub(r"[^\d]+", "", sq_m))
    return beds, sq_m

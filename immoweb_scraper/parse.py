import re

import pandas as pd


def retrieve_page_links(browser, location_a_list, max_price):
    elements = browser.find_element_by_class_name(
        "search-results__list"
    ).find_elements_by_xpath("//li[@class='search-results__item']")

    rows = []
    for i, element in enumerate(elements):
        # print(f"parsing {i}/{len(elements)}")
        base = element.find_elements_by_class_name("card--result__body")
        if not base or "Sponsored" in element.text:
            continue
        #  isinstance(base, list) and len(base) == 1
        else:
            base = next(iter(base))
            parsed = parse_link_element(base)
        if any(x > max_price for x in parsed["price"]):
            continue
        if parsed["commune"] not in location_a_list:
            continue
        else:
            rows.append(parsed)
    return rows


def parse_link_element(element):
    link = element.find_element_by_xpath(".//h2/a").get_attribute("href")
    app_type = element.find_element_by_xpath(".//h2/a").text
    price = element.find_element_by_xpath(
        ".//p[contains(@class,'card--result__price')]"
    ).text
    other_info = element.find_elements_by_xpath(".//div/p")
    space, location = tuple(map(lambda x: x.text, other_info))
    out = pd.Series(
        {
            "build_type": app_type,
            "link": link,
            "price": clean_price(price),
            "commune": int(re.sub(r"[^\d]+", "", location)),
            "space": clean_space(space),
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

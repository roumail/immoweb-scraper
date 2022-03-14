# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 10:46:18 2021

@author: U055555
"""
from selenium import webdriver
from selenium.webdriver.edge.service import Service

from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re


def page_setup(browser, web_page):
    # Open webpage
    browser.get(web_page)
    
    browser.implicitly_wait(4)  # seconds
    
    # wait and click privacy.. only the first time browser page opened
    # every other time, we skip this part
    try:
        browser.find_element_by_xpath("//button[@id='uc-btn-accept-banner']").click()
    except NoSuchElementException:
        pass
    return
    


def browser_setup(exe_path):
    """
    This function sets up a firefox browser, signs in, goes to the searh page, returning the webpage that contains
    links to all dr. profiles
    :return: a selenium web browser
    """


    # Browser setup
    s = Service(executable_path=exe_path)
    browser = webdriver.Edge(service=s) # firefox_profile=profile, 
    # Add implicit wait
    browser.implicitly_wait(7)  # seconds
    
    return browser


def retrieve_page_links(browser, location_a_list, max_price):
    elements = (
        browser
        .find_element_by_class_name("search-results__list")
        .find_elements_by_xpath("//li[@class='search-results__item']")
     )
    
    
    rows = []
    for i, element in enumerate(elements):
        # print(f"parsing {i}/{len(elements)}")
        base = element.find_elements_by_class_name("card--result__body")
        if not base or "Sponsored" in element.text:
            continue
        else: #  isinstance(base, list) and len(base) == 1
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
    price = element.find_element_by_xpath(".//p[contains(@class,'card--result__price')]").text  
    other_info = element.find_elements_by_xpath(".//div/p")
    space, location = tuple(map(lambda x: x.text, other_info))
    # TODO: add english name of commune, not just code
    commune = int(re.sub(r'[^\d]+', '', location))
    num_beds, sqm = clean_space(space)
    pat = re.compile("https://www.immoweb.be\/(?:.*)(\d{7})\?searchId=(?:.*)+")
    # add immo code
    immo_code = re.findall(pat, link)[0]
    out = pd.Series({
        "build_type" : app_type,
        "link" : link,
        "price" : clean_price(price),
        "commune" : commune,
        "num_bedrooms" : num_beds,
        "square_meters" : sqm,
        "immoweb_code" : ,
        })
    
    return out

def clean_price(p):
    "Remove , otherwise breaks"
    price = re.sub(',','',p).split("\n")[0]
    prices = re.findall("€(\d{2,4})", price)
    return list(map(int, prices))

def clean_space(p):
    beds, sq_m= p.split("·")
    beds = re.findall(r'(\d)\sbedrooms', beds)[0]
    sq_m = int(re.sub(r'[^\d]+', '', sq_m))
    return beds, sq_m

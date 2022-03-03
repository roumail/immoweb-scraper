# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 10:45:17 2021

@author: U055555
"""
from src import browser_setup, retrieve_page_links, page_setup
import pandas as pd
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import datetime
import pickle
from pathlib import Path

def main(web_page, exe_path, location_a_list, max_price, sort_by="cheapest",max_pages=5):
    browser = browser_setup(exe_path)
    # initialize link
    page_num=1
    url = web_page.format(str(page_num), sort_by)
    page_setup(browser,url)
    collection = []
    for page_i in range(max_pages):
        # if page_i == 2:
        #     break
        try:
            _info = retrieve_page_links(browser, location_a_list, max_price)
            collection.extend(_info)
            
            # preparation for next page..
            page_num+=1
            new_url= web_page.format(str(page_num), sort_by)
            sleep(5)
            page_setup(browser, new_url)
        except NoSuchElementException:
            break

    today_date = datetime.date.today()
    date_time = datetime.datetime.strftime(today_date, '%Y_%m_%d')    
    
    with open(f"{date_time}_pickle.pkl","wb") as f:
        pickle.dump(collection, f)
    
    df = pd.concat(collection, axis="columns").T
    
    df.to_csv(f"{date_time}_output.csv",index=False)

    return df




if __name__ == "__main__":
    ## PARAMETERS ## 
    exe_path = Path(r"C:\UCB\personal-development\scraping-test\edgedriver_win64\msedgedriver.exe")
    assert exe_path.exists()
    sort_by = "cheapest" # newest, postal_code, relevance
    
    # check online the last page and update...
    max_pages= 25
    location_a_list = [1030,1040,1050,1150,1180,1200] # 1190, 1060 - Forest and saint gilles dropped.. 
    max_price = 1500
    # TODO , create a function to take the parameters and make the query on the fly
    web_page = "https://www.immoweb.be/en/search/apartment/for-rent?countries=BE&minBedroomCount=2&minSurface=95&postalCodes=1030,1040,1050,1060,1150,1180,1200&maxPrice=1500&page={}&orderBy={}"
    #web_page = "https://www.immoweb.be/en/search/apartment/for-rent/etterbeek/1040?countries=BE&maxBedroomCount=4&maxPrice=1300&minBedroomCount=2&minSurface=95&page=1&orderBy={}"
    # web_page = "https://www.immoweb.be/en/search/apartment/for-rent?countries=BE&hasKitchenSetup=true&isAnInvestmentProperty=false&isFurnished=false&maxBedroomCount=4&maxPrice=1400&minBedroomCount=2&minSurface=90&postalCodes=1030,1040,1050,1060,1150,1180,1190,1200&priceType=MONTHLY_RENTAL_PRICE&propertySubtypes=APARTMENT,DUPLEX,PENTHOUSE,TRIPLEX,LOFT&provinces=BRUSSELS&page={}&orderBy={}"
    
    # call
    main(web_page, exe_path, location_a_list, max_price,sort_by, max_pages)

    
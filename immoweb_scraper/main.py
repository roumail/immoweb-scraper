import typer

app = typer.Typer()


@app.command()
def main():
    # old_main()
    pass


# def old_main(web_page, location_a_list, max_price, sort_by="cheapest",max_pages=5):
#     exe_path = ""
#     browser = browser_setup(exe_path)
#     # initialize link
#     page_num=1
#     web_page = "https://www.immoweb.be/en/search/apartment/for-rent?countries=BE&hasKitchenSetup=true&isAnInvestmentProperty=false&isFurnished=false&maxBedroomCount=4&maxPrice=1400&minBedroomCount=2&minSurface=90&postalCodes=1030,1040,1050,1060,1150,1180,1190,1200&priceType=MONTHLY_RENTAL_PRICE&propertySubtypes=APARTMENT,DUPLEX,PENTHOUSE,TRIPLEX,LOFT&provinces=BRUSSELS&page={}&orderBy={}"
#     ## PARAMETERS ##
#     sort_by = "cheapest" # newest, postal_code, relevance
#     # check online the last page and update...
#     max_pages=25
#     location_a_list = [1030,1040,1050,1060,1150,1180,1190,1200]
#     max_price = 1300
#     url = web_page.format(str(page_num), sort_by)
#     page_setup(browser,url)
#     collection = []
#     for page_i in range(max_pages):
#         # if page_i == 2:
#         #     break
#         try:
#             _info = retrieve_page_links(browser, location_a_list, max_price)
#             collection.extend(_info)

#             # preparation for next page..
#             page_num+=1
#             new_url= web_page.format(str(page_num), sort_by)
#             sleep(5)
#             page_setup(browser, new_url)
#         except NoSuchElementException:
#             break

#     today_date = datetime.date.today()
#     date_time = datetime.datetime.strftime(today_date, '%Y_%m_%d')

#     with open(f"{date_time}_pickle.pkl","wb") as f:
#         pickle.dump(collection, f)

#     df = pd.concat(collection, axis="columns").T

#     df.to_csv(f"{date_time}_output.csv",index=False)

#     return df

if __name__ == "__main__":
    app()

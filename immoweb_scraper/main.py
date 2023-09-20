import datetime

import typer
from loguru import logger
from selenium.webdriver import Chrome as WebDriver

from immoweb_scraper.db.addition import add_properties
from immoweb_scraper.db.DBConnection import DBConnection
from immoweb_scraper.models import PurchaseProperty, RentalProperty, to_property
from immoweb_scraper.scrape.scrape import scrape
from immoweb_scraper.scrape.url import ImmoWebURLBuilder
from immoweb_scraper.setup.browser import browser_setup

app = typer.Typer()


@app.command()
def main():
    today_date = datetime.datetime.today()
    date_time = today_date.strftime("%Y-%m-%d-%H:%M:%S")
    logger.info(f"Scraping started at {date_time}")
    browser: WebDriver = browser_setup()
    logger.debug("browser setup.")
    builder = ImmoWebURLBuilder()
    logger.info("Scraping rentals properties")
    rent_df = scrape(browser, builder.for_rent)
    rental_properties = [
        to_property(row, RentalProperty) for _, row in rent_df.iterrows()
    ]
    # Scrape for sale
    logger.info("Scraping sale properties")
    sale_df = scrape(browser, builder.for_sale)
    sale_properties = [
        to_property(row, PurchaseProperty) for _, row in sale_df.iterrows()
    ]
    logger.info("Adding to sqlite")
    db_conn = DBConnection(path2db="var/db/properties.sqlite")
    add_properties(db_conn, rental_properties, sale_properties)
    db_conn.close()
    today_date = datetime.datetime.today()
    date_time = today_date.strftime("%Y-%m-%d-%H:%M:%S")
    logger.info(f"Script finished at {date_time}")


if __name__ == "__main__":
    app()

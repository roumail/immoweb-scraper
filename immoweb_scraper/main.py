import datetime
import sys

import typer
from loguru import logger
from prefect import flow, task
from selenium.webdriver import Chrome as WebDriver

from immoweb_scraper.batcher.BatchStateHandler import BatchStateHandler
from immoweb_scraper.batcher.PostalCodeBatcher import PostalCodeBatcher
from immoweb_scraper.db.addition import add_properties
from immoweb_scraper.db.DBConnection import DBConnection
from immoweb_scraper.models import PurchaseProperty, RentalProperty, to_property
from immoweb_scraper.scrape.scrape import scrape
from immoweb_scraper.scrape.url import ImmoWebURLBuilder
from immoweb_scraper.setup.browser import browser_setup

app = typer.Typer()


@task
def setup():
    # setup logger
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    today_date = datetime.datetime.today()
    date_time = today_date.strftime("%Y-%m-%d-%H:%M:%S")
    logger.info(f"Scraping started at {date_time}")
    # browser setup
    browser: WebDriver = browser_setup()
    logger.debug("browser setup.")

    # setup database
    path2db = "var/db/properties.sqlite"
    db_conn = DBConnection(path2db=path2db)
    logger.debug("sqlite database connection setup.")
    return browser, db_conn


@task
def get_postal_codes(batch_state):
    batcher = PostalCodeBatcher(batch_state)
    batches = batcher.get_next_batch()
    logger.info(f"Scraping for the following post codes: {','.join(batches)}")
    return batches


@task
def scrape_rentals(browser, postal_codes):
    logger.info("Scraping rentals properties")
    builder = ImmoWebURLBuilder(postal_codes)
    df = scrape(browser, builder.for_rent)
    logger.info("Scraping completed")
    return df


@task
def scrape_sales(browser, postal_codes):
    logger.info("Scraping sale properties")
    builder = ImmoWebURLBuilder(postal_codes)
    df = scrape(browser, builder.for_sale)
    logger.info("Scraping completed ")
    return df


@task
def add_to_db(rent_df, sale_df, db_conn):
    rental_properties = [
        to_property(row, RentalProperty) for _, row in rent_df.iterrows()
    ]
    sale_properties = [
        to_property(row, PurchaseProperty) for _, row in sale_df.iterrows()
    ]
    logger.info("Adding to sqlite")
    add_properties(db_conn, rental_properties, sale_properties)
    logger.info("Properties added to tables")


@flow(name="Immoweb Scraper")
def scrape_immoweb_flow():
    browser, db_conn = setup()
    logger.debug("Initialize batcher to get state where we left off")
    batch_state = BatchStateHandler(db_conn)
    postal_codes = get_postal_codes(batch_state)
    rent_df = scrape_rentals(browser, postal_codes)
    sale_df = scrape_sales(browser, postal_codes)
    add_to_db(rent_df, sale_df, db_conn)
    db_conn.close()
    today_date = datetime.datetime.today()
    date_time = today_date.strftime("%Y-%m-%d-%H:%M:%S")
    logger.info(f"Script finished at {date_time}")


@app.command()
def run_flow():
    """Run the scraping flow."""
    # Execute the flow
    scrape_immoweb_flow()


if __name__ == "__main__":
    app()

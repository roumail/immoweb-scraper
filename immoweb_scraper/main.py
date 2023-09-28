import datetime

import pandas as pd
import typer
from prefect import flow, get_run_logger, task

from immoweb_scraper.batcher.BatchStateHandler import BatchStateHandler
from immoweb_scraper.batcher.PostalCodeBatcher import PostalCodeBatcher
from immoweb_scraper.db.addition import add_properties
from immoweb_scraper.db.DBConnection import DBConnection
from immoweb_scraper.models import PurchaseProperty, RentalProperty, to_property
from immoweb_scraper.scrape.scrape import scrape
from immoweb_scraper.scrape.url import ImmoWebURLBuilder
from immoweb_scraper.utils import get_current_time_str

app = typer.Typer()


@task
def get_postal_codes(initial_index) -> tuple[list[str], int]:
    batcher = PostalCodeBatcher(initial_index)
    batches = batcher.get_next_batch()
    new_index = batcher.get_current_index()
    return batches, new_index


@task
def add_to_db(rent_df: pd.DataFrame, sale_df: pd.DataFrame, db_conn, today_date: str):
    # add today date to both dataframes
    current_time_dt = datetime.datetime.strptime(today_date, "%Y-%m-%d-%H:%M:%S")
    today = current_time_dt.strftime("%Y-%m-%d")
    rent_df.loc[:, "collection_date"] = today
    sale_df.loc[:, "collection_date"] = today
    rental_properties = [
        to_property(row, RentalProperty) for _, row in rent_df.iterrows()
    ]
    sale_properties = [
        to_property(row, PurchaseProperty) for _, row in sale_df.iterrows()
    ]
    add_properties(db_conn, rental_properties, sale_properties)


@flow(name="Immoweb Scraper")
def scrape_immoweb_flow():
    logger = get_run_logger()
    date_time = get_current_time_str()
    logger.info(f"Scraping started at {date_time}")
    # setup database
    path2db = "var/db/properties.sqlite"
    db_conn = DBConnection(path2db=path2db)
    logger.debug("sqlite database connection setup.")
    logger.debug("Initialize batcher to get state where we left off")
    batch_state = BatchStateHandler(db_conn)
    initial_index = batch_state.load_state()
    logger.info(f"Starting index: {initial_index}")
    postal_codes, new_index = get_postal_codes(initial_index)
    logger.info(f"New index: {new_index}")
    logger.info(f"Scraping for the following post codes: {','.join(postal_codes)}")
    success_flag = False
    try:
        builder = ImmoWebURLBuilder(postal_codes)
        logger.info("Scraping rentals properties")
        rent_df = scrape(builder.for_rent)
        logger.info("Scraping completed")
        logger.info("Scraping sale properties")
        sale_df = scrape(builder.for_sale)
        logger.info("Scraping completed")
        date_time = get_current_time_str()
        logger.info("Adding to sqlite")
        # Adding properties to database
        add_to_db(rent_df, sale_df, db_conn, date_time)
        logger.info("Properties added to tables")
        success_flag = True
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    if success_flag:
        # Add the current index to the batch_state
        batch_state.save_state(new_index)
    db_conn.close()
    finish_time = get_current_time_str()
    logger.info(f"Script finished at {finish_time}")


@app.command()
def run_flow():
    """Run the scraping flow."""
    # Execute the flow
    scrape_immoweb_flow()


if __name__ == "__main__":
    app()

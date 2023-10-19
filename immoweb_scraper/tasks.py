import datetime

import pandas as pd
from prefect import task

from immoweb_scraper.batcher.PostalCodeBatcher import PostalCodeBatcher
from immoweb_scraper.db.addition import add_properties
from immoweb_scraper.models import PurchaseProperty, RentalProperty, to_property


# This is a continuously running task
@task
def get_postal_codes(initial_index) -> tuple[list[str], int]:
    batcher = PostalCodeBatcher(initial_index)
    batches = batcher.get_next_batch()
    new_index = batcher.get_current_index()
    return batches, new_index


# This is a task to be performed after the successful scraping of rental and purchase properties
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


# Add a separate task for the saving of the state

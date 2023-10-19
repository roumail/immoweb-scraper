import typer
from loguru import logger

from immoweb_scraper.batcher.BatchStateHandler import BatchStateHandler
from immoweb_scraper.db.DBConnection import DBConnection
from immoweb_scraper.scrape.url import ImmoWebURLBuilder
from immoweb_scraper.tasks import add_to_db, get_postal_codes, scrape
from immoweb_scraper.utils import get_current_time_str

app = typer.Typer()


@app.command()
def scrape_immoweb():
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
        raise e
    if success_flag:
        # Add the current index to the batch_state
        batch_state.save_state(new_index)
    db_conn.close()
    finish_time = get_current_time_str()
    logger.info(f"Script finished at {finish_time}")


if __name__ == "__main__":
    app()

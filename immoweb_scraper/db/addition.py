from loguru import logger

from immoweb_scraper.db.DBConnection import DBConnection
from immoweb_scraper.db.sqlalchemy import PurchasePropertyTable, RentalPropertyTable
from immoweb_scraper.models import PurchaseProperty, RentalProperty


def insert_rental_property(db_conn: DBConnection, data: RentalProperty):
    db_property = RentalPropertyTable(**data.model_dump())
    with db_conn.session_scope() as session:
        session.add(db_property)


def insert_purchase_property(db_conn: DBConnection, data: PurchaseProperty):
    db_property = PurchasePropertyTable(**data.model_dump())
    with db_conn.session_scope() as session:
        session.add(db_property)


def add_properties(
    db_conn: DBConnection,
    rental_properties: RentalProperty,
    purchase_properties: PurchaseProperty,
):
    logger.info("Adding rental properties to database")
    insert_rental_property(db_conn, rental_properties)
    logger.info("Adding purchase properties to database")
    insert_purchase_property(db_conn, purchase_properties)

import typing as tp

from loguru import logger

from immoweb_scraper.db.models import Base, PurchasePropertyTable, RentalPropertyTable

if tp.TYPE_CHECKING:
    from immoweb_scraper.db.DBConnection import DBConnection
    from immoweb_scraper.models import PurchaseProperty, RentalProperty


def insert_properties(
    db_conn: "DBConnection",
    properties: list[tp.Union["PurchaseProperty", "RentalProperty"]],
    table_class: tp.Type[Base],
):
    with db_conn.session_scope() as session:
        for prop in properties:
            db_property = table_class(**prop.model_dump())
            session.add(db_property)


def add_properties(
    db_conn: "DBConnection",
    rental_properties: list["RentalProperty"],
    purchase_properties: list["PurchaseProperty"],
):
    logger.info("Adding rental properties to database")
    insert_properties(db_conn, rental_properties, RentalPropertyTable)
    logger.info("Adding purchase properties to database")
    insert_properties(db_conn, purchase_properties, PurchasePropertyTable)

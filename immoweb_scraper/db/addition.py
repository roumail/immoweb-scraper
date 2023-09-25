import typing as tp
from collections import Counter

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
    # 1. Filter out duplicates in the properties list
    identifiers_list = [item.immoweb_identifier for item in properties]
    identifier_counts = Counter(identifiers_list)
    duplicates_in_list = {
        identifier: count
        for identifier, count in identifier_counts.items()
        if count > 1
    }
    if duplicates_in_list:
        logger.warning(
            f"Found duplicates in the list: {duplicates_in_list}. Keeping only one of each."
        )
        properties = list(
            {prop.immoweb_identifier: prop for prop in properties}.values()
        )

    # 2. Check against the database to ensure you're not inserting properties that already exist
    if table_class == RentalPropertyTable:
        existing_properties = get_all_rental_properties(db_conn)
    else:
        existing_properties = get_all_purchase_properties(db_conn)

    existing_identifiers = set(prop.immoweb_identifier for prop in existing_properties)
    new_properties = [
        prop
        for prop in properties
        if prop.immoweb_identifier not in existing_identifiers
    ]
    # add log for number of properties we're going to add

    with db_conn.session_scope() as session:
        for prop in new_properties:
            db_property = table_class(**prop.dict())
            session.add(db_property)
    return new_properties


def get_all_rental_properties(db_conn: "DBConnection"):
    with db_conn.session_scope() as session:
        return session.query(RentalPropertyTable).all()


def get_all_purchase_properties(db_conn: "DBConnection"):
    with db_conn.session_scope() as session:
        return session.query(PurchasePropertyTable).all()


def add_properties(
    db_conn: "DBConnection",
    rental_properties: list["RentalProperty"],
    purchase_properties: list["PurchaseProperty"],
):
    logger.info("Adding rental properties to database")
    rental_properties_added = insert_properties(
        db_conn, rental_properties, RentalPropertyTable
    )
    logger.info(
        f"Added {len(rental_properties_added)} rental properties to the database."
    )

    logger.info("Adding purchase properties to database")
    purchase_properties_added = insert_properties(
        db_conn, purchase_properties, PurchasePropertyTable
    )
    logger.info(
        f"Added {len(purchase_properties_added)} purchase properties to the database."
    )

    logger.info(
        f"Total new properties: {len(purchase_properties_added) + len(rental_properties_added)}."
    )

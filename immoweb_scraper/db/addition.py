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
    # 1. Verify that we only have unique identifiers in the properties list
    identifiers_list = [item.immoweb_identifier for item in properties]
    identifier_counts = Counter(identifiers_list)
    duplicates_in_list = {
        identifier: count
        for identifier, count in identifier_counts.items()
        if count > 1
    }
    assert not duplicates_in_list, f"Duplicates found in the list: {duplicates_in_list}"

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

    with db_conn.session_scope() as session:
        for prop in new_properties:
            db_property = table_class(**prop.model_dump())
            session.add(db_property)


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
    insert_properties(db_conn, rental_properties, RentalPropertyTable)
    logger.info("Adding purchase properties to database")
    insert_properties(db_conn, purchase_properties, PurchasePropertyTable)

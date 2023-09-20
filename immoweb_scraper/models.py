import typing as tp

import pandas as pd
from pydantic import BaseModel


class BaseProperty(BaseModel):
    immoweb_identifier: int
    build_type: str
    link: str
    price: int = None
    commune: int = None
    beds: int = None
    sq_meters: int = None


class RentalProperty(BaseProperty):
    charges: int = None


class PurchaseProperty(BaseProperty):
    pass


def to_property(
    data: pd.Series, property_type: tp.Type[tp.Union[RentalProperty, PurchaseProperty]]
) -> tp.Union[RentalProperty, PurchaseProperty]:
    price, charges = (data["price"] + (None, None))[:2]
    beds, sq_meters = (data["space"] + (None, None))[:2]

    property_data = {
        "immoweb_identifier": data["immoweb_identifier"],
        "build_type": data["build_type"],
        "link": data["link"],
        "price": price,
        "commune": data["commune"],
        "beds": beds,
        "sq_meters": sq_meters,
    }

    if issubclass(property_type, RentalProperty):
        property_data["charges"] = charges

    return property_type(**property_data)

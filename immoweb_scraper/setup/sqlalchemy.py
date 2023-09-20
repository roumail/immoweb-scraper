from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class RentalPropertyTable(Base):
    __tablename__ = "rental_properties"

    id = Column(Integer, primary_key=True)
    build_type = Column(String)
    link = Column(String, unique=True)
    price = Column(Float)
    charges = Column(Float)
    commune = Column(Integer)
    beds = Column(Integer)
    sq_meters = Column(Integer)


class PurchasePropertyTable(Base):
    __tablename__ = "purchase_properties"

    id = Column(Integer, primary_key=True)
    build_type = Column(String)
    link = Column(String, unique=True)
    price = Column(Float)
    commune = Column(Integer)
    beds = Column(Integer)
    sq_meters = Column(Integer)

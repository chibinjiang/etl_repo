from sqlalchemy import Column, VARCHAR, INTEGER, TIMESTAMP, UniqueConstraint, FLOAT
from configs.connector import BaseModel

from model import Mixin


class CountryGDPModel(Mixin, BaseModel):
    __tablename__ = 'country_gdp'
    __table_args__ = (
        UniqueConstraint("country", "year"),
    )
    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    year = Column(INTEGER, index=True, nullable=False)
    country = Column(VARCHAR(64), index=True, nullable=False)
    country_abbr = Column(VARCHAR(5), index=True)
    gdp = Column(FLOAT, index=True)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)

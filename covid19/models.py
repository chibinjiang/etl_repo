from sqlalchemy import Column, VARCHAR, INTEGER, TIMESTAMP, UniqueConstraint, FLOAT
from configs.connector import BaseModel

from model import Mixin


class CountryCovid19Model(Mixin, BaseModel):
    __tablename__ = 'country_covid19'
    __table_args__ = (
        UniqueConstraint("country", "date"),
    )
    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    date = Column(VARCHAR(16), index=True, nullable=False)
    country = Column(VARCHAR(64), index=True, nullable=False)
    country_abbr = Column(VARCHAR(5), index=True)
    confirmed = Column(INTEGER, index=True)
    deaths = Column(INTEGER, index=True)
    recovered = Column(INTEGER, index=True)
    daily_new = Column(INTEGER, index=True)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)

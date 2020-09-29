from sqlalchemy import Column, VARCHAR, INTEGER, TIMESTAMP, UniqueConstraint
from configs.connector import BaseModel

from model import Mixin


class CountryModel(Mixin, BaseModel):
    __tablename__ = 'country'
    __table_args__ = (
        UniqueConstraint("name"),
    )
    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(64), index=True)
    en_name = Column(VARCHAR(128), index=True, nullable=False)
    echart_name = Column(VARCHAR(64), index=True)
    iso_abbr = Column(VARCHAR(3), index=True)
    code = Column(VARCHAR(2), index=True)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)


class FreedomCountryScoreModel(Mixin, BaseModel):
    """
    虾仁猪心
    """
    __tablename__ = 'freedom_country_score'
    __table_args__ = (
        UniqueConstraint("country", "year"),
    )

    class Status(object):
        NotFree = "Not Free"
        Free = "Free"
        PartlyFree = "Partly Free"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    country = Column(VARCHAR(64), index=True, nullable=False)
    year = Column(INTEGER, index=True, nullable=False)
    country_abbr = Column(VARCHAR(5), index=True)
    pr_score = Column(INTEGER, index=True)   # Political Rights, 满分40
    cl_score = Column(INTEGER, index=True)  # Civil Liberties, 满分60
    total_score = Column(INTEGER, index=True)  # 满分100
    status = Column(VARCHAR(16), index=True)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)

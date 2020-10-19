from sqlalchemy import Column, VARCHAR, INTEGER, TIMESTAMP, FLOAT
from configs.connector import BaseModel

from model import Mixin


class USNuclearTargetModel(Mixin, BaseModel):
    __tablename__ = 'us_nuclear_target'
    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    point = Column(VARCHAR(64), index=True, nullable=False)
    country = Column(VARCHAR(64), index=True)
    longitude = Column(FLOAT, index=True)
    latitude = Column(FLOAT, index=True)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)

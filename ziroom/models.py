from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, JSON, TIMESTAMP, SMALLINT, FLOAT
from geoalchemy2 import Geometry
from configs.connector import BaseModel

from model import Mixin


class CommunityModel(Mixin, BaseModel):
    __tablename__ = 'ziroom_community'
    _id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(VARCHAR(24), index=True, nullable=False)
    name = Column(VARCHAR(64), index=True, nullable=False)
    community_name = Column(VARCHAR(32))
    city_name = Column(VARCHAR(32))
    district_name = Column(VARCHAR(32))
    bizcircle_name = Column(VARCHAR(32))
    # geo_location = GeometryColumn(Point(2))  # 维度: 2, srid defaults to 4326
    geo_location = Column(Geometry('POINT', srid=4326))
    sale_price = Column(FLOAT, index=True)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)


class ZiroomRentalModel(Mixin, BaseModel):
    """
    如何处理 多个 source_id
    """
    __tablename__ = 'ziroom_rental'
    _id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(VARCHAR(36), index=True, nullable=False)  # id(8)+house_id(8)+inv_id(6)+ind_no(9)
    community_id = Column(INTEGER, index=True)
    name = Column(VARCHAR(64))
    rent_type = Column(SMALLINT, index=True)  # 整租 or 合租
    is_first_signed = Column(SMALLINT, index=True, nullable=False)
    tags = Column(JSON)
    geo_location = Column(Geometry('POINT'))
    activity_list = Column(JSON)
    has_video = Column(SMALLINT)
    has_3d = Column(SMALLINT)
    is_turned = Column(SMALLINT)  # 是否转租
    sort_score = Column(FLOAT)
    bedroom_num = Column(SMALLINT)
    parlor_num = Column(SMALLINT)  # 客厅
    floor = Column(SMALLINT)
    floor_total = Column(SMALLINT)
    area_order = Column(FLOAT)  # 面积
    price = Column(INTEGER, index=True)
    price_unit = Column(VARCHAR(4))  # 租金的单位
    air_quality = Column(SMALLINT)
    face = Column(VARCHAR(4))  # 朝向
    sale_status = Column(SMALLINT)
    can_sign_date = Column(TIMESTAMP)
    can_sign_time = Column(TIMESTAMP)
    can_reserve_time = Column(TIMESTAMP)
    can_sign_long = Column(SMALLINT)
    can_sign_short = Column(SMALLINT)
    subway_station_info = Column(JSON)
    has_lift = Column(SMALLINT)
    build_year = Column(INTEGER)
    build_type = Column(VARCHAR(16))
    heating_type = Column(VARCHAR(16))
    greening_ratio = Column(FLOAT)
    bed_counter_size = Column(FLOAT)
    bed_width = Column(FLOAT)
    wardrobe_size = Column(SMALLINT)
    sofa_size = Column(SMALLINT)
    furniture_config = Column(JSON)
    cover_picture = Column(TEXT)  # 封面图
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)


GeometryDDL(CommunityModel.__table__)
GeometryDDL(ZiroomRentalModel.__tbale__)

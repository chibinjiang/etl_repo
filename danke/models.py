from sqlalchemy import Column, VARCHAR, INTEGER, TIMESTAMP, UniqueConstraint, SMALLINT, TEXT, FLOAT
from sqlalchemy.dialects.postgresql import ARRAY, JSON, DATE
from configs.connector import BaseModel

from model import Mixin


class DankeRentalModel(Mixin, BaseModel):

    class BedroomType(object):
        GD = '隔断'
        ZW = '主卧'
        CW = '次卧'

    class BuildingType(object):
        Loft = '民宅复式'
        Normal = '民宅平层'
        Department = '集中公寓'

    __tablename__ = 'danke_rental'
    __table_args__ = (
        UniqueConstraint("source_id"),
    )
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    city_id = Column(INTEGER, index=True)
    city_name = Column(VARCHAR(8), index=True)
    name = Column(VARCHAR(128), index=True)
    source_id = Column(INTEGER, index=True, nullable=False)
    room_code = Column(VARCHAR(16), index=True)
    room_number = Column(VARCHAR(4), index=True)
    block_name = Column(VARCHAR(32), index=True)
    district_name = Column(VARCHAR(8), index=True)
    area = Column(FLOAT, index=True)
    total_area = Column(FLOAT, index=True)
    address = Column(VARCHAR(128))
    source = Column(VARCHAR(8), index=True)
    status = Column(VARCHAR(4), index=True)
    style = Column(VARCHAR(8), index=True)
    living_room_count = Column(SMALLINT, index=True)  # parlor
    toilet_count = Column(SMALLINT, index=True)
    toilet_num = Column(SMALLINT, index=True)
    building_type = Column(VARCHAR(4), index=True)
    video_url = Column(TEXT)
    sublet_price = Column(INTEGER)  # 转租
    sublet_status = Column(SMALLINT)  # 转租
    sublet_mobile = Column(VARCHAR(16))
    bedroom_count = Column(SMALLINT, index=True)
    bedroom_type = Column(VARCHAR(16), index=True)
    built_year = Column(INTEGER, index=True)
    floor_count = Column(SMALLINT, index=True)
    floor_total_count = Column(SMALLINT, index=True)
    has_balcony = Column(SMALLINT, index=True)  # 阳台
    has_depot = Column(SMALLINT, index=True)
    has_lift = Column(SMALLINT, index=True)
    has_shower = Column(SMALLINT, index=True)
    has_terrace = Column(SMALLINT, index=True)
    has_toilet = Column(SMALLINT, index=True)
    has_tv = Column(SMALLINT, index=True)
    has_video = Column(SMALLINT, index=True)
    has_electronic_lock = Column(SMALLINT, index=True)  # 来自feature
    is_abs = Column(SMALLINT, index=True)
    is_month = Column(SMALLINT, index=True)
    is_near_subway = Column(SMALLINT, index=True)
    is_new_trend = Column(SMALLINT, index=True)
    is_rent_furniture = Column(SMALLINT, index=True)
    is_separated_room = Column(SMALLINT, index=True)
    price = Column(INTEGER, index=True)
    price_unit = Column(VARCHAR(4))
    month_price = Column(INTEGER, index=True)
    nearest_subway_title = Column(TEXT)
    subway_id = Column(VARCHAR(32))  # subway 表的id
    subway_distance = Column(INTEGER, index=True)
    subway_duration = Column(INTEGER, index=True)
    community_id = Column(INTEGER, index=True)  # community 表的 id
    community_name = Column(VARCHAR(64), index=True)
    public_space_num = Column(INTEGER, index=True)
    rent_end_date = Column(DATE, index=True)
    rent_ready_date = Column(DATE, index=True)
    rent_type = Column(SMALLINT, index=True)
    equip_end_date = Column(DATE, index=True)
    expect_check_in = Column(VARCHAR(32), index=True)
    waiting_rent_date = Column(DATE, index=True)
    # facility_list = Column(ARRAY(INTEGER))  # https://stackoverflow.com/questions/14219775/update-a-postgresql-array-using-sqlalchemy
    facility_config = Column(JSON)
    direction = Column(VARCHAR(4), index=True)
    heating = Column(VARCHAR(16), index=True)  # 来自feature
    weizhong_supply = Column(SMALLINT)
    search_text = Column(TEXT)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)


class DankeCommunityModel(Mixin, BaseModel):
    __tablename__ = 'danke_community'
    __table_args__ = (
        UniqueConstraint("source_id"),
    )
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(INTEGER, index=True, nullable=False)
    name = Column(VARCHAR(32), index=True, nullable=False)
    city_id = Column(INTEGER, index=True)
    city_name = Column(VARCHAR(8), index=True)
    block_id = Column(INTEGER, index=True)  # 街道
    block_name = Column(VARCHAR(16), index=True)
    district_id = Column(INTEGER, index=True)
    district_name = Column(VARCHAR(16), index=True)
    min_year = Column(INTEGER, index=True)
    max_year = Column(INTEGER, index=True)
    longitude = Column(FLOAT, index=True)
    latitude = Column(INTEGER, index=True)
    description = Column(TEXT)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)


class DankeRentalPicturesModel(Mixin, BaseModel):
    __tablename__ = 'danke_rental_pictures'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    rental_id = Column(INTEGER, index=True, nullable=False)  # rental 表的id
    order_no = Column(INTEGER, index=True, nullable=False)
    url = Column(VARCHAR(128), nullable=False, index=True)
    label = Column(VARCHAR(16), index=True)
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)


class DankeRentalRoommatesModel(Mixin, BaseModel):
    __tablename__ = 'danke_rental_roommates'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(INTEGER, index=True, nullable=False)
    name = Column(VARCHAR(8))
    gender = Column(VARCHAR(2))
    constellation = Column(VARCHAR(4))
    job = Column(VARCHAR(16))
    direction = Column(VARCHAR(4))
    has_toilet = Column(SMALLINT)
    check_in_time = Column(VARCHAR(16))
    area = Column(FLOAT)
    status = Column(VARCHAR(4))
    sublet_price = Column(INTEGER)  # 转租
    sublet_status = Column(VARCHAR(4))  # 转租
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)


class DankeSubwayModel(Mixin, BaseModel):
    __tablename__ = 'danke_subway'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(INTEGER, index=True, nullable=False)
    latitude = Column(FLOAT, index=True)
    longitude = Column(FLOAT, index=True)
    name = Column(VARCHAR(64))
    line = Column(VARCHAR(32))
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)


class DankeSuiteModel(Mixin, BaseModel):
    """
    房东房子的信息
    """
    __tablename__ = 'danke_suite'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    city_id = Column(INTEGER, index=True, nullable=False)
    city_name = Column(VARCHAR(8), index=True, nullable=False)
    source_id = Column(INTEGER, index=True, nullable=False)
    community_id = Column(INTEGER, index=True, nullable=False)  # community 的 id
    community_name = Column(VARCHAR(64), index=True)  # community 的 name
    address = Column(VARCHAR(128))
    area = Column(FLOAT, index=True)
    status = Column(VARCHAR(16), index=True)
    rent_end_date = Column(DATE, index=True)
    rent_ready_date = Column(DATE, index=True)
    equip_end_date = Column(DATE, index=True)
    bedroom_count = Column(SMALLINT, index=True)
    toilet_count = Column(SMALLINT, index=True)
    living_room_count = Column(SMALLINT, index=True)  # parlor
    floor_count = Column(SMALLINT, index=True)
    floor_total_count = Column(SMALLINT, index=True)
    heating = Column(VARCHAR(16), index=True)  # 来自feature
    updated = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)

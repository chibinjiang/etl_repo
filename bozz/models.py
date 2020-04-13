from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, JSON, TIMESTAMP, SMALLINT, FLOAT
from configs.connector import BaseModel

from model import Mixin
# 华为云的pg 不支持postgis, 除非提工单


class BozzCompanyModel(Mixin, BaseModel):
    __tablename__ = 'bozz_company'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(VARCHAR(32), index=True, nullable=False)
    name = Column(VARCHAR(64), index=True, nullable=False)
    logo = Column(VARCHAR(256))
    industry = Column(VARCHAR(16), index=True)
    scale = Column(VARCHAR(16), index=True)
    stage = Column(VARCHAR(16), index=True)
    welfare_list = Column(JSON)  # 福利
    work_days = Column(SMALLINT, index=True)  # 一周工作几天, 大小周算5.5
    start_work_time = Column(VARCHAR(10), index=True)  # 上班时间
    off_work_time = Column(VARCHAR(10), index=True)  # 下班时间
    tag_using_mac = Column(SMALLINT, index=True)  # 是否配mac
    tag_year_end_award = Column(SMALLINT, index=True)  # 年终奖
    # 股票期权
    tag_stock_inspire = Column(SMALLINT, index=True)
    # 餐补
    tag_meal_reward = Column(SMALLINT, index=True)
    # 住房补贴
    tag_rent_reward = Column(SMALLINT, index=True)
    # 弹性工作
    tag_elastic_work = Column(SMALLINT, index=True)
    # 偶尔加班
    tag_never_overtime = Column(SMALLINT, index=True)  # 不加班
    tag_often_overtime = Column(SMALLINT, index=True)  # 偶尔加班
    # 轮休
    tag_rotate_relax = Column(SMALLINT, index=True)  # 默认不
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

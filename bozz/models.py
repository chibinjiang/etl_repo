from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, JSON, TIMESTAMP, SMALLINT, PrimaryKeyConstraint, \
    UniqueConstraint, FLOAT
from configs.connector import BaseModel

from model import Mixin
# 华为云的pg 不支持postgis, 除非提工单


class BozzCompanyMapModel(Mixin, BaseModel):
    __tablename__ = 'bozz_company_map'
    __table_args__ = (
        PrimaryKeyConstraint("master_id", "replica_id"),
    )
    master_id = Column(INTEGER, index=True, nullable=False)
    replica_id = Column(VARCHAR(32), index=True, nullable=False)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)


class BozzCompanyModel(Mixin, BaseModel):
    __tablename__ = 'bozz_company'
    __table_args__ = (
        UniqueConstraint("source_id"),
    )

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(VARCHAR(32), index=True, nullable=False)
    name = Column(VARCHAR(64), index=True, nullable=False)
    logo = Column(VARCHAR(256))
    industry = Column(VARCHAR(16), index=True)
    scale = Column(VARCHAR(16), index=True)
    stage = Column(VARCHAR(16), index=True)
    welfare_list = Column(JSON)  # 福利
    work_days = Column(FLOAT, index=True)  # 一周工作几天, 大小周算5.5
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


class BozzRecruiterModel(Mixin, BaseModel):
    __tablename__ = "bozz_recruiter"
    __table_args__ = (
        UniqueConstraint("name", "title", "company_id"),
    )

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    # source_id = Column(VARCHAR(32), index=True, nullable=False)
    name = Column(VARCHAR(64), index=True, nullable=False)
    title = Column(VARCHAR(24))  # 头衔
    company_id = Column(INTEGER, index=True, nullable=False)
    avatar_url = Column(TEXT)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)


class BozzJobModel(Mixin, BaseModel):
    __tablename__ = "bozz_job"
    __table_args__ = (
        UniqueConstraint("source_id"),
    )

    class SalaryUnit(object):
        Date = 'per_date'
        Month = 'per_month'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    source_id = Column(VARCHAR(32), index=True, nullable=False)
    name = Column(VARCHAR(64), index=True, nullable=False)
    company_id = Column(INTEGER, index=True, nullable=False)
    recruiter_id = Column(INTEGER, index=True, nullable=False)
    degree_require = Column(VARCHAR(8))
    description = Column(TEXT)
    salary_text = Column(TEXT)
    total_salary_months = Column(INTEGER)
    salary_unit = Column(VARCHAR(16))
    min_experience = Column(INTEGER, index=True)
    max_experience = Column(INTEGER, index=True)
    min_salary = Column(INTEGER, index=True)
    max_salary = Column(INTEGER, index=True)
    labels = Column(JSON)
    valid_status = Column(INTEGER, index=True)
    city = Column(VARCHAR(16))
    district = Column(VARCHAR(16))
    business = Column(VARCHAR(16))  # 商圈
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

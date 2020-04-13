import traceback
from functools import wraps

import pandas as pd
from sqlalchemy.ext.declarative import declared_attr
from configs.connector import session


def catch_db_exc(default=None, rollback=False, logger=None):
    """
    捕获 db操作异常, 并返回默认值
    :param default: 在异常时返回的值
    :param rollback: 是否需要rollback
    :param logger:
    :return: default
    """
    def deco_func(func):
        @wraps(func)
        def catch_exc(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(traceback.format_exc())
                else:
                    traceback.print_exc()
            if rollback:
                session.rollback()
            return default
        return catch_exc
    return deco_func


class Mixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    @classmethod
    @catch_db_exc()
    def get(cls, _id):
        model = session.query(cls).filter(cls._id == _id).one_or_none()
        return model

    @classmethod
    @catch_db_exc()
    def get_by(cls, *conditions):
        model = session.query(cls).filter(*conditions).one_or_none()
        return model

    @classmethod
    @catch_db_exc(default=[])
    def query(cls, *conditions):
        models = session.query(cls).filter(*conditions).all()
        return models

    @classmethod
    @catch_db_exc()
    def query_dataframe(cls, *conditions):
        query = session.query(cls).filter(*conditions)
        df = pd.read_sql(query.statement, session.bind)
        return df

    @catch_db_exc(default=False, rollback=True)
    def save(self):
        session.add(self)
        session.commit()
        return True

    @catch_db_exc(default=False, rollback=True)
    def delete(self):
        session.delete(self)
        session.commit()
        return True

    @property
    def columns(self):
        columns = []
        for i in self.__table__.columns:
            columns.append(i.name)
        return columns

    @classmethod
    def dict2model(cls, d, model=None):
        model = model or cls()
        for attr in d:
            if not hasattr(model, attr):
                raise Exception("{} has no such attr: {}".format(cls.__tablename__, attr))
            setattr(model, attr, d[attr])
        return model

    def to_json(self):
        json_data = dict()
        for column in self.columns:
            json_data[column] = getattr(self, column)
        return json_data

@catch_db_exc(default=False, rollback=True)
def save_batch(model_list):
    session.add_all(model_list)
    session.commit()
    return True

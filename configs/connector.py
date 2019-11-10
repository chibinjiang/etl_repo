from redis import StrictRedis
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from private_configs import config

redis_client = StrictRedis(host=config.red_host, db=config.red_db, port=config.red_port)
mongo_client = MongoClient(config.mongo_uri)
mongo_db = mongo_client[config.mgd_db]
sql_engine = create_engine(config.db_uri)  # echo 表示是否打印详细SQL信息
# validate connection
assert mongo_client.server_info()['ok'] == 1.0
sql_engine.execute("select 1;")
BaseModel = declarative_base()
Session = sessionmaker()
Session.configure(bind=sql_engine)
session = Session()

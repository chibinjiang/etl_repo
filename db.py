from configs.connector import sql_engine
from zhihu.models import *
from anime.models import *
from github.models import *


def init_database():
    BaseModel.metadata.create_all(sql_engine)


if __name__ == '__main__':
    init_database()

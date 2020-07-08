from configs.connector import sql_engine
from zhihu.models import *
from anime.models import *
from github.models import GithubRepoModel, GithubTopicModel
from ziroom.models import ZiroomRentalModel, CommunityModel
from bozz.models import BozzCompanyModel, BozzJobModel


def init_database():
    BaseModel.metadata.create_all(sql_engine)


if __name__ == '__main__':
    init_database()

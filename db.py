from configs.connector import sql_engine, BaseModel
from freedom_house.model import FreedomCountryScoreModel
from gdp.models import CountryGDPModel
from nuclear.models import USNuclearTargetModel
from zhihu.models import ZhihuUserModel, ZhihuArticleModel, ZhihuQuestionModel, ZhihuAnswerModel, \
    ZhihuTopicBestAnswererMapModel, ZhihuTopicMapModel, ZhihuTopicModel
from anime.models import AnimeAuthorBangumiMapModel, AnimeAuthorModel, AnimeBangumiModel, AnimeEpisodeModel, \
    AnimeImageModel
from github.models import GithubRepoModel, GithubTopicModel
from ziroom.models import ZiroomRentalModel, CommunityModel
from bozz.models import BozzCompanyModel, BozzJobModel, BozzRecruiterModel, BozzCompanyMapModel
from covid19.models import CountryCovid19Model


def init_database():
    BaseModel.metadata.create_all(sql_engine)


if __name__ == '__main__':
    init_database()

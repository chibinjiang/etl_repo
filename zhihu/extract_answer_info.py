from datetime import datetime

from model import save_batch
from configs.connector import mongo_db
from utils import parse_html
from zhihu.models import ZhihuAnswerModel
collection = mongo_db['zhihu_answer']


def create_index():  # todo:  建索引
    collection.create_index("id")
    collection.create_index("voteup_count")
    collection.create_index("commaent_count")
    collection.create_index('user_id')


def extract_zhihu_answers():
    """
    todo: 可以模仿Flask的Form, 针对各个字段定义不同validate方法, 还能联合校验
    提取MongoDB 的 answer 信息
    :return:
    """
    unique_models = dict()
    for doc in collection.find({'id': '81972368'}):  # todo: 有效数据的条件
        # 无视匿名用户
        model = ZhihuAnswerModel()   # todo: 无效数据的过滤
        model.answer_id = doc['id']
        model.question_id = int(doc['question_id'])  # # todo:  mognod schema to mysql schame
        model.user_id = doc['user_id']
        if doc.get('is_labeled') is not None:  # todo: 处理缺失值
            model.is_labeled = doc['is_labeled']
        model.answer_url = doc['answer_url']
        if doc.get('content'):
            model.content = parse_html(doc['content'])
        if doc.get('thumbnail'):
            model.thumbnail = doc['thumbnail']
        model.comment_count = doc['comment_count']
        model.voteup_count = doc['voteup_count']
        model.created_time = datetime.fromtimestamp(int(doc['created_time']))  # convert 北京时间戳 to utc now
        model.updated_time = datetime.fromtimestamp(int(doc['updated_time']))
        model.created = datetime.utcnow()
        model.updated = datetime.utcnow()
        unique_models[model.answer_id] = model
    models = list()
    models.extend(unique_models.values())
    return save_batch(models)


if __name__ == '__main__':
    """
    python -m zhihu.extract_answer_info
    """
    create_index()
    extract_zhihu_answers()

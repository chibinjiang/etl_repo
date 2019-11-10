from datetime import timedelta, datetime

from configs.connector import mongo_client
from model import save_batch
from .models import ZhihuTopicModel


def extract_zhihu_topics():
    """
    提取MongoDB中的zhihu_topics到MySQL
    :return:
    """
    zhihu_topic = mongo_client['crawler']['zhihu_topic']
    docs = list(zhihu_topic.find({'crawl_time': {'$gt': datetime.utcnow() - timedelta(days=1)}}))
    models = list()
    for doc in docs:
        model = ZhihuTopicModel.get(int(doc['id']))
        if doc.get('questions_count') is not None:
            model.questions_count = doc['questions_count']
        if doc.get('unanswered_count') is not None:
            model.unanswered_count = doc['unanswered_count']
        if doc.get('followers_count') is not None:
            model.followers_count = doc['followers_count']
        if doc.get('father_count') is not None:
            model.father_count = doc['father_count']
        if doc.get('best_answers_count') is not None:
            model.best_answers_count = doc['best_answers_count']
        if doc.get('best_answerers_count'):
            model.best_answerers_count = doc['best_answerers_count']
        if doc.get('category'):
            model.category = doc['category']
        if doc.get('avatar_url'):
            model.avatar_url = doc['avatar_url']
        if doc.get('introduction'):
            model.description = doc['introduction']
        model.topic_url = doc['topic_url']
        models.append(model)
    return save_batch(models)


if __name__ == '__main__':
    """
    python -m etl.zhihu.extract_topic_info
    # 没有爬到的topic:
        20202320
        

    """
    extract_zhihu_topics()

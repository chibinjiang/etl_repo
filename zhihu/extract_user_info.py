from collections import Counter
from datetime import datetime

from configs.connector import mongo_client
from model import save_batch
from .models import ZhihuUserModel, GenderValue, ZhihuTopicBestAnswererMapModel


def extract_zhihu_users():
    """
    提取MongoDB 的user信息
    :return:
    """
    answerer_topic_maps = dict()
    unique_models = dict()
    for doc in mongo_client['crawler']['zhihu_user'].find({'id': {'$nin': [0, '0']}}):
        # 无视匿名用户
        model = ZhihuUserModel()
        model.user_id = doc['id']
        model.name = doc['name']
        if doc.get('user_url'):  # and doc['user_url'] != 'http://www.zhihu.com/api/v4/people/0'
            model.user_url = doc['user_url']
        if doc.get('user_type') is not None:
            model.user_type = doc['user_type']
        if doc.get('url_token'):
            model.url_token = doc['url_token']
        if doc.get('avatar_url') and doc['avatar_url'] != 'http://www.zhihu.com/api/v4/people/0':
            model.avatar_url = doc['avatar_url']
        edu_member_tag = doc.get('edu_member_tag')
        if edu_member_tag:
            if edu_member_tag['type'] == 'subject':
                model.subject = edu_member_tag.get('member_tag') or edu_member_tag.get('memberTag')
            elif edu_member_tag['type'] == 'master':
                model.master_area = edu_member_tag.get('member_tag') or edu_member_tag.get('memberTag')
        if doc.get('gender') in [1, 0] and doc['user_url'] != 'http://www.zhihu.com/api/v4/people/0':
            model.gender = GenderValue.male if doc['gender'] == 1 else GenderValue.female
        if doc.get('headline'):
            model.headline = doc['headline']
        if doc.get('is_org') is not None:
            model.is_org = doc['is_org']
        if doc.get('is_advertiser') is not None:
            model.is_advertiser = doc['is_advertiser']
        for badge in doc.get('badge', []):
            if badge['type'] == 'identity':
                model.identity = badge['description']
            elif badge['type'] == 'best_answerer':
                for topic in badge['topics']:
                    map_model = ZhihuTopicBestAnswererMapModel()
                    map_model.topic_id = int(topic['id'])
                    map_model.user_id = doc['id']
                    map_model.created = datetime.utcnow()
                    answerer_topic_maps[(map_model.user_id, map_model.topic_id)] = map_model
        model.created = datetime.utcnow()
        model.updated = datetime.utcnow()
        unique_models[model.user_id] = model
    models = []
    models.extend(answerer_topic_maps.values())
    models.extend(unique_models.values())
    return save_batch(models)


def get_all_badge():
    types = set()
    for doc in mongo_client['crawler']['zhihu_user'].find():
        for badge in doc['badge']:
            if not badge:
                continue
            types.add(badge['type'])
    print(types)


def get_all_edu():
    types = set()
    values = list()
    docs = list(mongo_client['crawler']['zhihu_user'].find({}, {'edu_member_tag': 1}))
    for doc in docs:
        edu_tag = doc.get('edu_member_tag')
        if edu_tag:
            if edu_tag.get('type') and edu_tag.get('member_tag'):
                types.add(edu_tag['type'])
                values.append(edu_tag['member_tag'])
    values_freq = Counter(values)
    print(types)
    print(values_freq.most_common(n=20))


if __name__ == '__main__':
    """
    python -m etl.zhihu.extract_user_info
    """
    extract_zhihu_users()

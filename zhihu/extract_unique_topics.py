from datetime import datetime
from pprint import pprint

from configs.connector import mongo_db
from model import save_batch
from zhihu.models import ZhihuTopicMapModel, ZhihuTopicModel


def main():
    zhihu_coll = mongo_db['zhihu_topic_node']
    # unique topic id
    pipeline = [
        {'$group': {'_id':
                        {'topic_id': '$id', 'topic_name': '$name',
                         'parent_id': '$parent_id', 'parent_name': '$parent_name'},
                    'count': {'$sum': 1}}},
    ]
    edges = list(zhihu_coll.aggregate(pipeline))
    print("一共有{}条边".format(len(edges)))
    models = list()
    unique_topic_ids = set()
    for edge in edges:
        info = edge['_id']
        now = datetime.utcnow()
        if not ZhihuTopicModel.get(info['topic_id']):
            topic_model = ZhihuTopicModel()
            topic_model.topic_id = int(info['topic_id'])
            topic_model.topic_name = info['topic_name']
            topic_model.created = now
            topic_model.updated = now
            if topic_model.topic_id not in unique_topic_ids:
                models.append(topic_model)
                unique_topic_ids.add(topic_model.topic_id)
        try:
            if not ZhihuTopicMapModel.query(
                    ZhihuTopicMapModel.topic_id == int(info['topic_id']),
                    ZhihuTopicMapModel.parent_id == int(info['parent_id'])):
                map_model = ZhihuTopicMapModel()
                map_model.topic_id = int(info['topic_id'])
                map_model.parent_id = int(info['parent_id'])
                map_model.created = now
                models.append(map_model)
        except KeyError as e:
            pprint(info)
    save_batch(models)


if __name__ == '__main__':
    """
    python -m etl.zhihu.extract_unique_topics
    """
    main()

from .models import ZhihuTopicModel


def run():
    hot_topics = list()
    for model in ZhihuTopicModel.query(ZhihuTopicModel.followers_count > 9999):
        hot_topics.append(model.topic_id)
    return hot_topics


if __name__ == '__main__':
    """
    python -m etl.zhihu.find_top20_hot_topics
    """
    run()

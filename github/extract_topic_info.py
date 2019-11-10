from datetime import datetime
from configs.connector import mongo_db
from github.models import GithubTopicModel
collection = mongo_db['github_topic']


def extract_github_topics():
    cond = {}
    for doc in collection.find(cond):
        model = GithubTopicModel.get_by(GithubTopicModel.topic_id == doc['topic_id']) or GithubTopicModel()
        if not model.created:
            model.created = datetime.utcnow()
        model.url = doc['url']
        model.name = doc['name']
        model.topic_id = doc['topic_id']
        if doc.get('avatar_url'):
            model.avatar_url = doc['avatar_url']
        if doc.get('description'):
            model.description = doc['description']
        model.updated = datetime.utcnow()
        model.save()


if __name__ == '__main__':
    """
    python -m github.extract_topic_info
    """
    extract_github_topics()


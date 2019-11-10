import sys
from datetime import datetime
from configs.connector import mongo_db
from github.models import GithubRepoModel

collection = mongo_db['github_repo']


def extract_github_repos():
    cond = {"name": {'$exists': True}}
    models = list()
    for i, doc in enumerate(collection.find(cond)):
        sys.stdout.write("\rETL: %d" % i)
        sys.stdout.flush()
        model = GithubRepoModel.get_by(GithubRepoModel.repo_id == doc['repo_id']) or GithubRepoModel()
        if not model.created:
            model.created = datetime.utcnow()
        model.url = doc['url']
        model.user_id = doc['user_id']
        model.resource = 'github'
        model.name = doc['name']
        model.repo_id = doc['repo_id']
        if 'stars' in doc:
            model.stars = doc['stars']
        if 'commits' in doc:
            model.commits = doc['commits']
        if 'issues' in doc:
            model.issues = doc['issues']
        if 'forks' in doc:
            model.forks = doc['forks']
        if 'watches' in doc:
            model.watches = doc['watches']
        if 'contributors' in doc:
            model.contributors = doc['contributors']
        if 'last_commit_id' in doc:
            model.last_commit_id = doc['last_commit_id']
        if 'first_commit_id' in doc:
            model.first_commit_id = doc['first_commit_id']
        if 'last_commit_time' in doc:
            model.last_commit_time = doc['last_commit_time']
        if 'first_commit_time' in doc:
            model.first_commit_time = doc['first_commit_time']
        desc = doc.get('description', '')
        model.description = desc
        topics = doc.get("topics", []) or []
        model.topics = topics
        major_languages = doc.get("major_languages", []) or []  # 默认是空list
        model.major_languages = major_languages
        model.updated = datetime.utcnow()
        models.append(model)
        model.save()
    # save_batch(models)


if __name__ == '__main__':
    """
    python -m github.extract_repo_info
    """
    extract_github_repos()


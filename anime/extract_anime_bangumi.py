"""
番剧表
"""
from datetime import datetime
from pymongo import DESCENDING
from configs.connector import mongo_db
from anime.models import AnimeBangumiModel, AnimeAuthorBangumiMapModel, AnimeAuthorModel
collection = mongo_db['anime_bangumi']


def extract_bangumi():
    for doc in collection.find().sort('crawl_time', DESCENDING):
        source_id = str(doc['bangumi_id'])
        model = AnimeBangumiModel.get_by_bangumi_id(source_id)
        if not model:
            model = AnimeBangumiModel()
            model.bangumi_id = source_id
            model.created = datetime.utcnow()
        model.name = doc['name']
        model.rank = doc['rank']
        model.cover = 'images/' + doc['save_file']
        model.last_updated = doc['last_updated']
        model.introduction = doc['introduction']
        model.source_url = doc['url']
        model.updated = datetime.utcnow()
        model.save()


def extract_author():
    for doc in collection.find().sort('crawl_time', DESCENDING):
        for name in doc['author']:
            # author
            model = AnimeAuthorModel.get_by_name(name)
            if not model:
                model = AnimeAuthorModel()
                model.name = name
                model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()


def extract_map():
    for doc in collection.find().sort('crawl_time', DESCENDING):
        for name in doc['author']:
            # author
            author = AnimeAuthorModel.get_by_name(name)
            bangumi = AnimeBangumiModel.get_by_bangumi_id(str(doc['bangumi_id']))
            if not author or not bangumi:
                print(author, bangumi)
                continue
            model = AnimeAuthorBangumiMapModel.get_by_author_and_bangumi(author._id, bangumi._id)
            if not model:
                model = AnimeAuthorBangumiMapModel()
                model.bangumi_id = bangumi._id
                model.author_id = author._id
                model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()


if __name__ == '__main__':
    """
    python -m etl.anime.extract_anime_bangumi
    """
    extract_bangumi()
    extract_author()
    extract_map()


from datetime import datetime
from pymongo import DESCENDING
from model import save_batch
from configs.connector import mongo_db
from anime.models import AnimeEpisodeModel, AnimeBangumiModel
collection = mongo_db['anime_episode']


def main():
    models = list()
    done_ids = set()
    for doc in collection.find().sort('crawl_time', DESCENDING):
        unique_id = str(doc['episode_id'])
        bangumi_source_id = str(doc['bangumi_id'])
        new_bangumi = AnimeBangumiModel.get_by_bangumi_id(bangumi_source_id)
        assert new_bangumi is not None
        model = AnimeEpisodeModel.get_by_episode_id(unique_id)
        if unique_id in done_ids:
            continue
        if not model:
            model = AnimeEpisodeModel()
            model.episode_id = unique_id
            model.created = datetime.utcnow()
        model.bangumi_id = new_bangumi._id
        model.title = doc['title']
        model.number = int(doc['number'])
        model.source_url = doc['first_page']
        model.updated = datetime.utcnow()
        models.append(model)
        done_ids.add(unique_id)
    print(len(models))
    save_batch(models)
    return models


if __name__ == '__main__':
    """
    python -m etl.anime.extract_anime_episode
    """
    main()


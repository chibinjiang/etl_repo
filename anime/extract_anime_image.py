from datetime import datetime
from pymongo import DESCENDING
from model import save_batch
from configs.connector import mongo_db
from anime.models import AnimeImageModel, AnimeEpisodeModel
collection = mongo_db['anime_image']


def main():
    models = list()
    for doc in collection.find().sort('crawl_time', DESCENDING):
        model = AnimeImageModel()
        episode_id = str(doc['episode_id'])
        episode_model = AnimeEpisodeModel.get_by_episode_id(episode_id)
        if not episode_model:
            print("NO Episode: ", doc)
            continue
        model.episode_id = doc['episode_id']
        if doc.get('number'):
            model.number = int(doc['number'])
        if doc.get('save_file'):
            # 保存相对路径
            model.image = 'images/' + doc['save_file']
        if doc.get('image'):
            model.source_image = doc['image']
        model.episode_id = episode_model._id
        model.source_url = doc['url']
        model.created = datetime.utcnow()
        model.updated = datetime.utcnow()
        models.append(model)
    return save_batch(models)


if __name__ == '__main__':
    """
    python -m etl.anime.extract_anime_image
    """
    main()


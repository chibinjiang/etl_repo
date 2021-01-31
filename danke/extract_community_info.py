from datetime import datetime
from configs.connector import mongo_db
from danke.models import DankeCommunityModel

rental_coll = mongo_db['fuck_danke_rental_detail']


def parse_community(doc):
    model = DankeCommunityModel()
    model.source_id = doc['communityId']
    model.name = doc['communityName']
    model.city_id = doc['cityId']
    model.city_name = doc['cityName']
    model.block_id = doc['blockId']
    model.block_name = doc['blockName']
    model.district_id = doc['districtId']
    model.district_name = doc['districtName']
    if doc['min_year']:
        model.min_year = doc['min_year']
    if doc['max_year']:
        model.max_year = doc['max_year']
    model.description = doc['summary'] or ''
    model.longitude = doc['communityLongitude']
    model.latitude = doc['communityLatitude']
    model.updated = datetime.utcnow()
    model.created = datetime.utcnow()
    return model


def main():
    fields = [
        'communityId', 'communityName', 'cityId', 'cityName', 'blockId',
        'blockName', 'districtId', 'districtName', 'communityLongitude',
        'communityLatitude'
    ]
    group_by = {
        '_id': {f: f'${f}' for f in fields},
        'min_year': {'$min': '$builtYears'},
        'max_year': {'$max': '$builtYears'},
        'summary': {'$last': '$communitySummary'}
    }
    pipeline = [
        {'$group': group_by}
    ]
    for doc in rental_coll.aggregate(pipeline):
        if not doc['_id']:
            continue
        doc.update(doc.pop('_id'))
        if not DankeCommunityModel.get_by(DankeCommunityModel.source_id == doc['communityId']):
            print("Saving ", doc['communityName'])
            model = parse_community(doc)
            model.save()


if __name__ == '__main__':
    """
    python -m danke.extract_community_info
    """
    main()

from datetime import datetime
from configs.connector import mongo_db
from danke.models import DankeSubwayModel

rental_coll = mongo_db['fuck_danke_rental_detail']


def parse_subway(doc):
    model = DankeSubwayModel.get_by(DankeSubwayModel.source_id == doc['id']) or DankeSubwayModel()
    model.source_id = doc['id']
    model.name = doc['name']
    model.latitude = doc['latitude']
    model.longitude = doc['longitude']
    model.line = doc['line']
    model.updated = datetime.utcnow()
    if not model.id:
        model.created = datetime.utcnow()
    return model


def main():
    group_by = {
        '_id': {
            'id': '$subwayId',
            'name': '$subway',
            'longitude': '$subwayLongitude',
            'latitude': '$subwayLatitude',
            'line': '$subwayLine',
        }
    }
    pipeline = [
        {'$match': {'subwayId': {'$nin': [None, '']}}},
        {'$group': group_by}
    ]
    for doc in rental_coll.aggregate(pipeline):
        doc.update(doc.pop('_id'))
        if not doc['name']:
            continue
        doc['name'] = doc['name'].split('.')[-1]
        print("[*] Saving: ", doc['name'])
        model = parse_subway(doc)
        model.save()


if __name__ == '__main__':
    main()

from datetime import datetime
from configs.connector import mongo_db
from danke.models import DankeSuiteModel, DankeCommunityModel

rental_coll = mongo_db['fuck_danke_rental_detail']


def parse_suite(doc):
    model = DankeSuiteModel.get_by(DankeSuiteModel.source_id == doc['suiteId']) or DankeSuiteModel()
    model.source_id = doc['suiteId']
    model.city_id = doc['cityId']
    model.city_name = doc['cityName']
    for field in [
        'rent_end_date', 'community_id', 'address', 'status', 'status', 'area', 'community_name',
        'rent_ready_date', 'equip_end_date', 'bedroom_count', 'living_room_count',
        'toilet_count', 'floor_count', 'floor_total_count', 'heating'
    ]:
        if doc[field] != '' and not str(doc[field]).startswith('000'):
            setattr(model, field, doc[field])
    model.updated = datetime.utcnow()
    if not model.id:
        model.created = datetime.utcnow()
    return model


def main():
    fields = [
        'suiteId', 'communityId', 'cityId', 'cityName',
    ]
    group_by = {
        '_id': {f: f'${f}' for f in fields},
        'status': {'$last': '$suiteStatus'},
        'address': {'$last': '$suiteAddress'},
        'area': {'$last': '$suiteArea'},
        'community_name': {'$last': '$communityName'},
        'rent_end_date': {'$last': '$rentEndDate'},
        'rent_ready_date': {'$last': '$rentReadyDate'},
        'equip_end_date': {'$last': '$equipEndDate'},
        'bedroom_count': {'$max': '$bedroomCount'},
        'living_room_count': {'$max': '$parlor'},
        'toilet_count': {'$max': '$toiletCount'},
        'floor_count': {'$max': '$floorCount'},
        'floor_total_count': {'$max': '$floorTotalCount'},
        'heating': {'$last': '$heating'},
    }
    pipeline = [
        {'$group': group_by}
    ]
    community_id_map = dict()
    for doc in rental_coll.aggregate(pipeline, allowDiskUse=True):
        if not doc['_id']:
            continue
        doc.update(doc.pop('_id'))
        community_source_id = int(doc['communityId'])
        if community_id_map.get(community_source_id):
            doc['community_id'] = community_id_map[community_source_id]
        else:
            community = DankeCommunityModel.get_by(DankeCommunityModel.source_id == community_source_id)
            if not community:
                print("Invalid Community ID: ", community_source_id, doc['address'])
                continue
            community_id_map[community_source_id] = community.id
            doc['community_id'] = community.id
        print("Saving ", doc['address'])
        model = parse_suite(doc)
        model.save()


if __name__ == '__main__':
    """
    python -m danke.extract_suite_info
    """
    main()

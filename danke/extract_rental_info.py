"""
顺序:
- 小区
- 地铁站
- 房子
- 租房
- 室友
- 图片
"""
import re
import traceback
from datetime import datetime
from configs.connector import mongo_db
from danke.models import DankeSuiteModel, DankeRentalModel, DankeRentalPicturesModel, DankeCommunityModel

rental_coll = mongo_db['fuck_danke_rental_detail']


def extract_number(value):
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        number = re.search(r'[\d\.]+', value)
        if number:
            return float(number.group(0))
    return None


def extract_boolean(value):
    if value in [True, 'true', 'True']:
        return 1
    elif value in [False, 'false', 'False']:
        return 0
    else:
        return value


def parse_picture(doc):
    for order_no, picture in enumerate(doc['detailPictures']):
        model = DankeRentalPicturesModel.get_by(
            DankeRentalPicturesModel.rental_id == doc['rental_id'], DankeRentalPicturesModel.url == picture['url']) \
                or DankeRentalPicturesModel()
        model.rental_id = doc['rental_id']
        model.url = picture['url']
        model.label = picture['labelName']
        model.order_no = order_no
        if not model.id:
            model.created = datetime.utcnow()
        model.updated = datetime.utcnow()
        model.save()


def check_valid_date(doc, field):
    if doc.get(field) and not doc[field].startswith('000') and not doc[field].startswith('1970'):
        return True
    return False


def parse_rental(doc):
    model = DankeRentalModel.get_by(DankeRentalModel.source_id == int(doc['roomId'])) or DankeRentalModel()
    model.city_id = int(doc['cityId'])
    model.city_name = doc['cityName']
    model.source_id = int(doc['roomId'])
    model.name = doc['name']
    model.suite_id = doc['suite_id']
    model.block_name = doc['blockName']
    model.district_name = doc.get('districtName')
    model.address = doc.get('suiteAddress')
    model.community_id = doc['community_id']
    model.community_name = doc.get('communityName')
    model.room_code = doc.get('roomCode')
    model.area = extract_number(doc.get('roomArea'))
    model.total_area = extract_number(doc.get('suiteArea'))
    model.room_number = doc.get('roomNumber')
    model.style = doc.get('style')
    model.status = doc.get('roomStatus')
    model.source = doc.get('roomSource')
    model.search_text = doc.get('searchText', '')
    model.living_room_count = doc.get('parlor')
    model.bedroom_count = doc.get('bedroomCount')
    model.toilet_count = doc.get('toiletCount')
    model.toilet_num = doc.get('toiletNum')
    model.bedroom_type = doc.get('bedroomType')
    model.built_year = extract_number(doc.get('builtYears'))
    model.building_type = doc.get('buildingType')
    model.video_url = doc.get('videoUrl')
    model.sublet_price = doc.get('subletPrice')
    model.sublet_status = extract_boolean(doc.get('subletStatus'))
    model.sublet_mobile = doc.get('subletMobile')
    model.floor_count = doc.get('floorCount')
    model.floor_total_count = doc.get('floorTotalCount')
    model.has_balcony = extract_boolean(doc.get('hasBalcony'))  # 阳台
    model.has_depot = extract_boolean(doc.get('hasDepot'))
    model.has_shower = extract_boolean(doc.get('hasShower'))
    model.has_toilet = extract_boolean(doc.get('hasToilet'))
    model.has_tv = extract_boolean(doc.get('hasTv'))
    model.has_lift = extract_boolean(doc.get('hasLift'))
    model.has_terrace = extract_boolean(doc.get('hasTerrace'))  # 阳台
    model.has_video = extract_boolean(doc.get('hasVideo'))
    model.facility_config = [item['title'] for config in doc['facilityConfig']
                             if config['label'] == '卧室配置' for item in config['items']]
    model.has_electronic_lock = extract_boolean('智能锁' in model.facility_config)
    model.is_abs = extract_boolean(doc.get('isAbs'))
    model.is_month = extract_boolean(doc.get('isMonth'))
    model.is_near_subway = extract_boolean(doc.get('isNearSuway'))
    model.is_new_trend = extract_boolean(doc.get('isNewTrend'))
    model.is_separated_room = extract_boolean(doc.get('isSeparatedRoom'))
    model.is_rent_furniture = extract_boolean(doc.get('isRentFurniture'))
    model.price = extract_number(doc.get('price'))
    model.month_price = int(doc['monthPrice'])
    model.price_unit = doc.get('priceUnit')
    model.nearest_subway_title = doc.get('nearestSubwayTitle')
    model.subway_id = doc.get('subwayId')
    model.subway_distance = doc.get('subwayDistance')
    model.subway_duration = doc.get('subwayDuration')
    if check_valid_date(doc, 'rentEndDate'):
        model.rent_end_date = doc['rentEndDate']
    model.public_space_num = doc.get('publicSpaceNum')
    if check_valid_date(doc, 'rentReadyDate'):
        model.rent_ready_date = doc['rentReadyDate']
    model.rent_type = doc['rentType']
    model.heating = doc['heating']
    model.direction = doc['facing']
    model.search_text = doc['searchText']
    model.expect_check_in = doc.get('expectCheckIn', {}).get('checkInTitle')
    if check_valid_date(doc, 'equipEndDate'):
        model.equip_end_date = doc['equipEndDate']
    # model.weizhong_supply = doc.get('weizhongSupply')
    if check_valid_date(doc, 'waitingRentDate'):
        model.waiting_rent_date = doc['waitingRentDate']
    model.updated = datetime.utcnow()
    model.created = datetime.utcnow()
    return model


def main():
    for doc in rental_coll.find({}):
        if not doc.get('suiteId'):
            continue
        try:
            suite = DankeSuiteModel.get_by(DankeSuiteModel.source_id == doc['suiteId'])
            community = DankeCommunityModel.get_by(DankeCommunityModel.source_id == doc['communityId'])
            if suite and community:
                doc['suite_id'] = suite.id
                doc['community_id'] = community.id
                model = parse_rental(doc)
                model.save()
            else:
                print(f"No such community or suite id: {doc['communityId']} and {doc['suiteId']}")
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    """
    python -m danke.extract_rental_info
    """
    main()

"""
步骤:
1. 提取rental 信息
2. 用不同价格新增rental
3. 提取rental 详情页的信息
4. 删除过去7天的原数据
"""
from datetime import datetime

from configs.connector import mongo_db
from .models import ZiroomRentalModel, CommunityModel


def process_each_rental(doc: dict, community: CommunityModel, rental: ZiroomRentalModel):
    print("处理: ", str(doc['_id']))
    tags = [tag['title'] for tag in doc.get('tags', [])]
    rental.is_first_signed = 1 if '首次出租' in tags else 0
    rental.name = doc['name']
    rental.has_3d = doc['has_3d']
    rental.rent_type = doc['type']
    # rental.has_lift = doc['have_lift']
    rental.has_video = doc['has_video']
    rental.is_turned = doc['turn']
    rental.tags = [tag['title'] for tag in doc.get('tags', [])]
    rental.sort_score = doc['sort_score']
    rental.bedroom_num = doc['bedroom']
    rental.parlor_num = doc['parlor']
    rental.face = doc['face']
    rental.area_order = doc['area_order']
    rental.floor = doc['floor']
    rental.floor_total = doc['floor_total']
    rental.air_quality = doc['air_quality']
    rental.can_sign_date = datetime.fromtimestamp(doc['can_sign_date']) if doc.get('can_sign_date') else None
    rental.can_sign_time = datetime.fromtimestamp(doc['can_sign_time']) if doc.get('can_sign_time') else None
    rental.can_reserve_time = doc['can_reserve_time']
    rental.can_sign_long = doc['can_sign_long']
    rental.can_sign_short = doc['can_sign_short']
    # 房间配套
    # rental.bed_counter_size =
    # rental.price = int(doc['sale_price'])
    rental.floor_total = int(doc['floor_total']) if doc.get('floor_total') else None
    community.source_id = doc['resblock_id']
    community.name = doc['resblock_name']
    if 'lng' in doc:
        community.longitude = doc['lng']
        rental.longitude = doc['lng']
    if 'lat' in doc:
        community.latitude = doc['lat']
        rental.latitude = doc['lat']
    community.bizcircle_name = doc['bizcircle_name'].strip()
    community.district_name = doc['district_name'].strip()
    community.updated = datetime.utcnow()
    community.created = datetime.utcnow()
    rental.updated = datetime.utcnow()
    rental.created = datetime.utcnow()
    return True
    # detail = doc['detail_info']
    # if not detail:
    #     continue
    # resblock = detail['resblock']
    # # 处理tags
    # try:
    #     tags = [tag['title'] for tag in detail.get('tags', [])]
    #     tags.extend([tag['title'] for tag in doc.get('tags', [])])
    #     if '首次出租' in tags:
    #         rental['is_first_signed'] = 1
    #     else:
    #         rental['is_first_signed'] = 0
    #     for tag in tags:
    #         if tag in ignore_tags:
    #             continue
    #         tag = tag.strip()
    #         rental['tag_' + tag] = 1
    #     rental['id'] = doc['inv_no']
    #     rental['has_video'] = doc['has_video']
    #     rental['has_3d'] = doc['has_3d']
    #     rental['turn'] = doc['turn']
    #     rental['sort_score'] = doc['sort_score']
    #     rental['bedroom'] = doc['bedroom']
    #     rental['floor_total'] = int(doc['floor_total'])
    #     rental['sale_price'] = int(doc['sale_price'])
    #     # sample['district'] = doc['district_name'].strip()
    #     bizcircle =
    #     rental['bizcircle_{}'.format(bizcircle)] = 1
    #     # sample['bizcircle'] = doc['bizcircle_name'].strip()
    #     rental['parlor'] = doc['parlor']
    #     rental['air_quality'] = doc['air_quality']
    #     for face in doc.get('face', ''):
    #         if face in '东南西北':
    #             rental['face_' + face] = 1
    #     rental['sale_status_{}'.format(doc['sale_status'])] = 1
    #     rental['area_order'] = doc['area_order']
    #     rental['floor'] = doc['floor']
    #     rental['floor_ratio'] = int(doc['floor']) / int(doc['floor_total'])
    #     meter = re.search('\d+米', doc.get('subway_station_info', ''))
    #     # if meter:
    #     rental['to_station'] = int(meter.group(0).strip('米'))
    #     rental['have_lift'] = detail['have_lift']
    #     rental['price'] = math.log(doc['real_price'])
    #     # 小区信息
    #     if resblock.get('build_year'):
    #         rental['build_year'] = 2020 - int(resblock['build_year'])
    #     if resblock.get('build_type'):
    #         rental['build_type_{}'.format(resblock['build_type'])] = 1
    #     if resblock.get('heating_type'):
    #         rental['heating_type_{}'.format(resblock['heating_type'])] = 1
    #     if resblock.get('house_num'):
    #         rental['total_houses'] = int(resblock.get('house_num'))
    #     # sample['sale_price'] = resblock
    #     green_ratio = re.search('\d+', resblock.get('greening_ratio', ''))
    #     if green_ratio:
    #         rental['green_ratio'] = int(green_ratio.group(0))
    #     # 房间配套
    #     for space in detail.get('space', []):
    #         for config in space.get('config', []):
    #             thing = config['name']
    #             if '床下柜' in thing:
    #                 if re.search(r'[\d\.]+', thing):
    #                     rental['bed_counter'] = float(re.search(r'[\d\.]+', thing).group(0))
    #                 else:
    #                     rental['bed_counter'] = 1.5  # 假设是1.5的床下柜
    #             elif thing.endswith('床'):
    #                 if re.search(r'[\d\.]+', thing):
    #                     rental['bed_width'] = float(re.search(r'[\d\.]+', thing).group(0))
    #                 else:
    #                     rental['bed_width'] = 1.5  # 假设是1.5的床下柜
    #             elif '衣柜' in thing:
    #                 if '双' in thing:
    #                     rental['wardrobe'] = 2
    #                 elif '三' in thing:
    #                     rental['wardrobe'] = 3
    #                 elif '四' in thing:
    #                     rental['wardrobe'] = 4
    #                 else:
    #                     rental['wardrobe'] = 2  # default
    #             elif '沙发' in thing:
    #                 if '双人' in thing:
    #                     rental['sofa_size'] = 2
    #                 elif '单人' in thing:
    #                     rental['sofa_size'] = 1
    #                 else:
    #                     rental['sofa_size'] = 1
    #             else:
    #                 rental['config_{}'.format(thing)] = int(config['num'])
    #         break
    #     # 优惠活动
    #     for activity in detail.get('activity_list', []):
    #         rental['activity_{}'.format(activity['name'])] = 1


def extract_rental():
    valid_cond = {}
    ziroom_rental = mongo_db['ziroom_rental_raw']
    rentals = ziroom_rental.find(valid_cond)
    for doc in rentals:
        rental_id = "_".join([doc['id'], doc['house_id'], doc['inv_id'], doc['inv_no']])
        rental = ZiroomRentalModel.get_by(ZiroomRentalModel.source_id == rental_id) or ZiroomRentalModel()
        rental.source_id = rental_id
        community = CommunityModel.get_by(CommunityModel.name == doc['resblock_name'],
                                          CommunityModel.bizcircle_name == doc['bizcircle_name']) or CommunityModel()
        process_each_rental(doc, community, rental)
        if community.save():
            rental.community_id = community.id
            rental.save()


def deepcopy_db_object(model):
    new_model = model.__class__()
    for column in model.columns:
        if column not in ['id', '_id']:
            setattr(new_model, column, getattr(model, column))
    return new_model


def extract_price():
    ziroom_price = mongo_db['ziroom_rental_price']
    prices = ziroom_price.find({})
    for doc in prices:
        rental = ZiroomRentalModel.get_by(ZiroomRentalModel.source_id.like('%{}%'.format(doc['inv_no'])))
        if not rental:
            print("No such rental: {}".format(doc['inv_no']))
            continue
        if rental.price is None:
            print("{}: {} -> {}".format(doc['inv_no'], rental.price, doc['price']))
            rental.price = doc['price']
            rental.save()
        elif doc['price'] != rental.price:
            print("{}: {} -> {}".format(doc['inv_no'], rental.price, doc['price']))
            new_rental = deepcopy_db_object(rental)
            new_rental.price = doc['price']
            new_rental.created = datetime.utcnow()
            new_rental.updated = datetime.utcnow()
            rental.expiration_time = doc['crawl_time']
            rental.updated = datetime.utcnow()
            rental.save()
            new_rental.save()


def split_list(lst, size):
    """
    将lst 分成 等份, 每份size 个
    :param lst:
    :param size:
    :return:
    """
    results = list()
    for i in range(0, len(lst), size):
        results.append(lst[i: i+size])
    return results


def delete_done_docs():
    ids = list()
    ziroom_rental = mongo_db['ziroom_rental_raw']
    for model in ZiroomRentalModel.query():
        ids.append(model.source_id.split('_')[-1])
    for i, batch_ids in enumerate(split_list(ids, 1000)):
        print(i, " deleted: ", len(batch_ids))
        result = ziroom_rental.delete_many({'inv_no': {'$in': batch_ids}})


def extract_detail():
    pass


def delete_1_week_ago():
    pass


if __name__ == '__main__':
    """
    python -m ziroom.extract_ziroom_rental
    """
    # extract_rental()
    delete_done_docs()
    # extract_detail()
    # delete_1_week_ago()

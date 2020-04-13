import re
import sys
from configs.connector import mongo_db
from .models import BozzCompanyModel


class TagValue(object):
    Yes = 1
    No = 0


def parse_welfare_list(doc, welfares):
    for tag in welfares:
        # 是否双休
        if '双休' in tag:
            doc['work_days'] = 5
        elif '单休' in tag:
            doc['work_days'] = 6
        elif '大小周' in tag:
            doc['work_days'] = 5.5
        if '排班轮休' in tag:
            doc['tag_rotate_relax'] = TagValue.Yes
        else:
            doc['tag_rotate_relax'] = TagValue.No
        if '股票期权' in tag:
            doc['tag_stock_inspire'] = TagValue.Yes
        if '年终奖' in tag:
            doc['tag_year_end_award'] = TagValue.Yes
        # 上下班时间
        work_time = re.search('上午(\d+:\d+)-下午(\d+:\d+)', tag)
        if work_time:
            doc['start_work_time'] = work_time.group(1)
            doc['off_work_time'] = work_time.group(2)
        if '餐补' in tag:
            doc['tag_meal_reward'] = TagValue.Yes
        if '住房补贴' in tag:
            doc['tag_rent_reward'] = TagValue.Yes
        if '弹性工作' in tag:
            doc['tag_elastic_work'] = TagValue.Yes
        if '偶尔加班' in tag:
            doc['tag_often_overtime'] = TagValue.Yes
        if '不加班' in tag:
            doc['tag_never_overtime'] = TagValue.Yes
    # 是否配mac
    # using_mac = Column(SMALLINT, index=True)
    return doc


def dict2model(d, Model, model=None):
    model = model or Model()
    for attr in d:
        if not hasattr(model, attr):
            raise Exception("{} has no such attr: {}".format(Model.__tablename__, attr))
        setattr(model, attr, d[attr])
    return model


def process_each_company(doc):
    data = dict()
    if doc.get('welfareList'):
        parse_welfare_list(data, doc['welfareList'])
    data['welfare_list'] = doc['welfareList'] or []
    data['source_id'] = doc['encryptBrandId']
    data['name'] = doc['name']
    data['scale'] = doc['scaleName']
    data['stage'] = doc['stageName']
    data['industry'] = doc['industryName']
    data['logo'] = doc['logo']
    data['updated'] = doc['crawl_time']
    # data['created'] = datetime.utcnow()
    return data


def extract_company():
    valid_cond = {}
    bozz_company = mongo_db['bozz_company']
    company_list = bozz_company.find(valid_cond)
    for i, doc in enumerate(company_list):
        sys.stdout.write("\r{}".format(i+1))
        sys.stdout.flush()
        model = BozzCompanyModel.get_by(BozzCompanyModel.source_id==doc['encryptBrandId'])
        parse_doc = process_each_company(doc)
        if not model:
            parse_doc['created'] = doc['crawl_time']
        model = dict2model(parse_doc, BozzCompanyModel, model)
        if not model.save():
            raise Exception("Stop")


if __name__ == '__main__':
    """
    python -m bozz.extract_company_info
    """
    extract_company()

import sys
from datetime import datetime
from pymongo import MongoClient
from private_configs import config
from freestyle_utils.decorators.toolbox import timeit, cache_by_redis
from configs.connector import mongo_db
from .models import BozzRecruiterModel, BozzCompanyModel


def parse_each_recruiter(doc):
    data = dict()
    data['name'] = doc['bossName']
    data['title'] = doc['bossTitle']
    data['avatar_url'] = doc['bossAvatar']
    data['created'] = doc['crawl_time']
    data['updated'] = datetime.utcnow()
    return data


@cache_by_redis(3600)
def match_company(source_id=None, name=None, logo=None):
    company = None
    if source_id:
        company = BozzCompanyModel.get_by(BozzCompanyModel.source_id == source_id)
    if not company and name and logo:
        company = BozzCompanyModel.get_by(BozzCompanyModel.name == name, BozzCompanyModel.logo == logo)
    if not company and name:
        company = BozzCompanyModel.get_by(BozzCompanyModel.name == name)
    if not company:
        print("No such company: {}".format(name))
    return company.id


@timeit
def extract_recruiter(brand_name):
    """
    预处理的速度奇慢
    """
    print(f"处理{brand_name}的招聘者")
    client = MongoClient(config.mongo_uri)
    mongo_db = client[config.mgd_db]
    bozz_job = mongo_db['bozz_job']
    recruiter_list = bozz_job.aggregate([
        {'$match': {'brandName': brand_name}},
        {'$group': {'_id': {
            'bossName': '$bossName', 'bossTitle': '$bossTitle', 'encryptBrandId': '$encryptBrandId',
            'brandName': '$brandName', 'brandLogo': '$brandLogo'
        }, 'bossAvatar': {'$last': '$bossAvatar'}, 'crawl_time': {'$last': '$crawl_time'}}}
    ], allowDiskUse=True)
    for i, doc in enumerate(recruiter_list):
        sys.stdout.write("\r{}".format(i+1))
        sys.stdout.flush()
        doc.update(doc.pop('_id'))
        company_id = match_company(doc.get('encryptBrandId'), doc.get('brandName'), doc.get('brandLogo'))
        if not company_id:
            continue
        # recruiter
        recruiter = BozzRecruiterModel.get_by(
            BozzRecruiterModel.name == doc['bossName'],
            BozzRecruiterModel.title == doc['bossTitle'],
            BozzRecruiterModel.company_id == company_id
        )
        parsed_recruiter = parse_each_recruiter(doc)
        parsed_recruiter['company_id'] = company_id
        recruiter_model = BozzRecruiterModel.dict2model(parsed_recruiter, recruiter)
        recruiter_model.save()


if __name__ == '__main__':
    """
    python -m bozz.extract_recruiter_info
    怎么把 ETL的速度提升呢: 如何 并发呢 ?
    """
    bozz_company = mongo_db['bozz_company']
    names = list(bozz_company.distinct('name'))[:16]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=4) as exe:
        exe.map(extract_recruiter, names)

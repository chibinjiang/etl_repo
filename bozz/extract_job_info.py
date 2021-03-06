import re
import sys
from datetime import datetime

from freestyle_utils.decorators.toolbox import timeit, cache_by_redis
from pymongo import DESCENDING

from configs.connector import mongo_db, redis_client
from model import save_batch
from .models import BozzJobModel, BozzRecruiterModel, BozzCompanyModel


class TagValue(object):
    Yes = 1
    No = 0


def parse_each_job(doc):
    data = dict()
    data['source_id'] = doc['encryptJobId']
    data['name'] = doc['jobName']
    data['degree_require'] = doc['jobDegree']
    data['labels'] = doc['jobLabels']
    data['valid_status'] = doc['jobValidStatus']
    data['city'] = doc['cityName']
    data['district'] = doc['districtName']
    data['business'] = doc['businessName']
    nums = re.search("(\d+)-(\d+)", doc.get('jobExperience') or '')
    if nums:
        data['min_experience'] = int(nums.group(1))
        data['max_experience'] = int(nums.group(2))
    if '1年以内' == doc.get('jobExperience'):
        data['min_experience'], data['max_experience'] = 0, 1
    if '应届生' == doc.get('jobExperience'):
        data['min_experience'], data['max_experience'] = 0, 0
    salary_desc = doc.get('salaryDesc') or ''
    by_date = '天' in salary_desc
    data['salary_text'] = salary_desc
    data['salary_unit'] = BozzJobModel.SalaryUnit.Date if by_date else BozzJobModel.SalaryUnit.Month
    nums = re.search("(\d+)-(\d+)", salary_desc)
    if nums:
        data['min_salary'] = int(nums.group(1)) if by_date else int(nums.group(1)) * 1000
        data['max_salary'] = int(nums.group(2)) if by_date else int(nums.group(2)) * 1000
    total_salary_months = re.search('(\d+)薪', salary_desc)
    if total_salary_months:
        data['total_salary_months'] = int(total_salary_months.group(1))
    data['created'] = doc['crawl_time']
    data['updated'] = datetime.utcnow()
    return data


def parse_each_recruiter(doc):
    data = dict()
    data['name'] = doc['bossName']
    data['title'] = doc['bossTitle']
    data['avatar_url'] = doc['bossAvatar']
    data['created'] = doc['crawl_time']
    data['updated'] = datetime.utcnow()
    return data


@cache_by_redis(redis_client, 3600)
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


def match_recruiter(name, title, company):
    pass


@timeit
def extract_job(skip, size):
    """
    预处理的速度奇慢
    """
    valid_cond = {}
    models = list()
    batch_size = 5000
    unique_ids = list()
    bozz_job = mongo_db['bozz_job']
    job_list = bozz_job.find(valid_cond).sort([('crawl_time', DESCENDING)]).skip(skip).limit(size)
    for i, doc in enumerate(job_list):
        sys.stdout.write("\r{}".format(i+1))
        sys.stdout.flush()
        jid = doc['encryptJobId']
        if jid in unique_ids:
            continue
        unique_ids.append(jid)
        company_id = match_company(doc.get('encryptBrandId'), doc.get('brandName'), doc.get('brandLogo'))
        if not company_id:
            continue
        # job, MongoDB 中已经去重了
        job = BozzJobModel.get_by(BozzJobModel.source_id == jid)
        parsed_job = parse_each_job(doc)
        parsed_job['company_id'] = company_id
        # parsed_job['recruiter_id'] = recruiter_model.id
        job_model = BozzJobModel.dict2model(parsed_job, job)
        models.append(job_model)
        if len(models) == batch_size:
            save_batch(models, chunk_size=batch_size)
            models = list()
    if models:
        save_batch(models, chunk_size=batch_size)
    return i+1


def update_company_id():
    pass

def update_recruiter_id():
    pass


if __name__ == '__main__':
    """
    python -m bozz.extract_job_info
    怎么把 ETL的速度提升呢
    """
    offset = 0
    limit = 100000
    while True:
        print(f"Offset: {offset}; Limit: {limit}")
        l = extract_job(offset, limit)
        if l < limit:
            print(f"Stop on: {l}")
            break
        offset += limit

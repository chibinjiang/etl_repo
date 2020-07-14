import re
import sys
from datetime import datetime

from pymongo import DESCENDING

from configs.connector import mongo_db
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
    nums = re.search("(\d+)-(\d+)", salary_desc)
    if nums:
        data['min_salary'] = int(nums.group(1)) if '天' in salary_desc else int(nums.group(1)) * 1000
        data['max_salary'] = int(nums.group(2)) if '天' in salary_desc else int(nums.group(2)) * 1000
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


def extract_job(skip, size):
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
        company = None
        if 'encryptBrandId' in doc:
            company = BozzCompanyModel.get_by(BozzCompanyModel.source_id == doc.get('encryptBrandId'))
        if not company:
            company = BozzCompanyModel.get_by(BozzCompanyModel.name == doc['brandName'], BozzCompanyModel.logo == doc['brandLogo'])
        if not company:
            company = BozzCompanyModel.get_by(BozzCompanyModel.name == doc['brandName'])
        if not company:
            print("No such company: {}".format(doc['brandName']))
            continue
        # recruiter
        recruiter = BozzRecruiterModel.get_by(
            BozzRecruiterModel.name == doc['bossName'],
            BozzRecruiterModel.title == doc['bossTitle'],
            BozzRecruiterModel.company_id == company.id
        )
        parsed_recruiter = parse_each_recruiter(doc)
        parsed_recruiter['company_id'] = company.id
        recruiter_model = BozzRecruiterModel.dict2model(parsed_recruiter, recruiter)
        recruiter_model.save()
        # job, MongoDB 中已经去重了
        job = BozzJobModel.get_by(BozzJobModel.source_id == jid)
        parsed_job = parse_each_job(doc)
        parsed_job['company_id'] = company.id
        parsed_job['recruiter_id'] = recruiter_model.id
        job_model = BozzJobModel.dict2model(parsed_job, job)
        models.append(job_model)
        if len(models) == batch_size:
            save_batch(models, chunk_size=batch_size)
            models = list()
    if models:
        save_batch(models, chunk_size=batch_size)
    return models


if __name__ == '__main__':
    """
    python -m bozz.extract_job_info
    """
    offset = 0
    limit = 100000
    while True:
        print(f"Offset: {offset}; Limit: {limit}")
        models = extract_job(offset, limit)
        if len(models) < limit:
            print(f"Stop on: {len(models)}")
            break
        offset += limit

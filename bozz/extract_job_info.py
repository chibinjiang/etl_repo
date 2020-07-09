import re
import sys
import traceback
from datetime import datetime

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
    nums = re.search("(\d+)-(\d+)", doc.get('salaryDesc') or '')
    if nums:
        data['min_salary'] = int(nums.group(1)) * 1000
        data['max_salary'] = int(nums.group(2)) * 1000
    data['updated'] = doc['crawl_time']
    return data


def parse_each_recruiter(doc):
    data = dict()
    data['name'] = doc['bossName']
    data['title'] = doc['bossTitle']
    data['avatar_url'] = doc['bossAvatar']
    data['created'] = doc['crawl_time']
    data['updated'] = datetime.utcnow()
    return data


def extract_job():
    valid_cond = {}
    models = list()
    batch_size = 1000
    unique_ids = list()
    bozz_company = mongo_db['bozz_job']
    company_list = bozz_company.find(valid_cond)
    for i, doc in enumerate(company_list):
        try:
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
                raise Exception("No such company: {}".format(doc['brandName']))
            # recruiter
            recruiter = BozzRecruiterModel.get_by(
                BozzRecruiterModel.name == doc['bossName'],
                BozzRecruiterModel.title == doc['bossTitle'], BozzRecruiterModel.company_id == company.id)
            parsed_recruiter = parse_each_recruiter(doc)
            parsed_recruiter['company_id'] = company.id
            if not recruiter:
                parsed_recruiter['created'] = doc['crawl_time']
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
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    """
    python -m bozz.extract_job_info
    """
    extract_job()

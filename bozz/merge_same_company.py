from datetime import datetime
import time
import requests
from scrapy import Selector
from collections import defaultdict
from bozz.models import BozzCompanyMapModel, BozzCompanyModel


def load_duplicate_tuple():
    name2source_ids = defaultdict(list)
    for model in BozzCompanyModel.query():
        name2source_ids[model.name].append(model.source_id)
    ret = dict()
    for name in name2source_ids:
        source_ids = name2source_ids[name]
        if len(source_ids) > 1:
            ret[name] = source_ids
    return ret


def query_bozz(name):
    headers = {
        'authority': 'www.zhipin.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.zhipin.com/job_detail/?query=%E5%8C%BB%E6%B8%A1%E4%BA%91&city=100010000&industry=&position=',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7',
        'cookie': '__zp__pub__=; __c=1594053777; __g=-; t=uhIdpv3QMnz843s; wt=uhIdpv3QMnz843s; __l=l=%2Flogin.zhipin.com%2F&r=https%3A%2F%2Fwww.zhipin.com%2Fgongsir%2F4dc79c7ad647bbac0XN409m-Fg~~.html%3Fka%3Dcompany-jobs&friend_source=0&friend_source=0; _bl_uid=XIkRXchea3kqnhh6pcyjnsUe9I2I; __zp__pub__=; __zp_seo_uuid__=540cae3e-52e2-4fac-a7dd-55de60e9753c; lastCity=100010000; __a=68411834.1590144204.1590144204.1594053777.58.2.52.58; __zp_stoken__=58b9aAH5fRE8VGlIqAiZUUF0EegdzI09mWhB3A1BPeExiZFFZcVFUf0NPUSYCO1RdAkcSGCsUf3QJBllVNFRTM1McNxgvUhRDDAJmMHNqJktMICFZQWoeAyYtc2Y%2BHAMWQH5XZyQ8VH5LRyU%3D',
    }
    params = (
        ('query', name),
        ('city', '100010000'),
        ('industry', ''),
        ('position', ''),
    )
    response = requests.get('https://www.zhipin.com/job_detail/', headers=headers, params=params)
    selector = Selector(response)
    html = selector.xpath('.//div[@id="wrap"]//div[@class="company-item"]//a/@href').extract_first()
    if html:
        source_id = html.split('/')[-1].split('.')[0]
        print(f"Target id: {source_id}")
        model = BozzCompanyModel.get_by(BozzCompanyModel.source_id == source_id)
        return model.id


def main():
    name2source_ids = load_duplicate_tuple()
    print(name2source_ids)
    for name in name2source_ids:
        print(f"Query {name}....")
        source_ids = name2source_ids[name]
        master_id = query_bozz(name)
        if not master_id:
            print(f"No such master id: {name}")
            continue
        for source_id in source_ids:
            model = BozzCompanyMapModel()
            model.master_id = master_id
            model.replica_id = source_id
            model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()
        time.sleep(1)


if __name__ == '__main__':
    """
    python -m bozz.merge_same_company
    """
    main()




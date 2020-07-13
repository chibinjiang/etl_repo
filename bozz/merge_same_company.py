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
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.zhipin.com/job_detail/?query=huawei&city=100010000&industry=&position=',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7',
        'cookie': '__zp__pub__=; __c=1594642411; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1594642412; lastCity=100010000; __l=l=%2Fwww.zhipin.com%2Fgongsir%2F4dc79c7ad647bbac0XN409m-Fg~~.html%3Fka%3Dcompany-jobs&r=&friend_source=0&friend_source=0; __a=58798900.1594642411..1594642411.8.1.8.8; __zp_stoken__=4f4faPC5UeCopAnoRXV1hAWJiBVhtL3FFUlgQNRVLKXtScT5IHlgiUiBeAGAScFoAD39CJHRKN0hEH2RVAwZUGXltd3Q0SQB5ZkIlOjJsWF9NGCd0VUREJTdOKQwJLBwdTUYHW3tDSE0JBWE%3D; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1594642821',
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
            raise Exception(f"No such master id: {name}")
        for source_id in source_ids:
            model = BozzCompanyMapModel()
            model.master_id = master_id
            model.replica_id = source_id
            model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()
        time.sleep(5)


if __name__ == '__main__':
    """
    python -m bozz.merge_same_company
    """
    main()




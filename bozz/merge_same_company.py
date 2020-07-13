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
    cookies = {
        '__zp__pub__': '',
        'Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a': '1594644343',
        'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a': '1594644343',
        '__zp_stoken__': '4f4faPC5UeCopNwgfajxhAWJiBVhiem9MUyEQNRVLKR05Yh1FFFgiUiBeAGRmMnUXD39CJHRKNzoXF2BVGn0SOA8Xc3M6XXgUfksvRDJsWF9NGDBbFzBAJTdOKQwJJhwdTUYHW3tDSE0JBWE%3D',
        '__a': '1077175.1594644340..1594644340.1.1.1.1',
        '__c': '1594644340',
        '__g': '-',
        '__l': 'l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D%25E4%25B9%2590%25E4%25BF%25A1%25E5%259C%25A3%25E6%2596%2587%26city%3D100010000%26industry%3D%26position%3D&r=&friend_source=0',
    }

    headers = {
        'Host': 'www.zhipin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e24) NetType/WIFI Language/en',
        'accept-language': 'en-us',
    }

    params = (
        ('query', name),
        ('city', '100010000'),
        ('industry', ''),
        ('position', ''),
    )
    response = requests.get('https://www.zhipin.com/job_detail/', headers=headers, params=params, cookies=cookies)
    if len(response.text) < 51402:
        raise Exception("被发现了!")
    selector = Selector(response)
    html = selector.xpath('.//div[@id="wrap"]//div[@class="company-item"]//a/@href').extract_first()
    if html:
        source_id = html.split('/')[-1].split('.')[0]
        print(f"Target id: {source_id}")
        model = BozzCompanyModel.get_by(BozzCompanyModel.source_id == source_id)
        return model.id


def main():
    name2source_ids = load_duplicate_tuple()
    for name in name2source_ids:
        print(f"Query {name}....")
        source_ids = name2source_ids[name]
        master_id = query_bozz(name)
        if not master_id:
            print(f"No such master id: {name}")
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




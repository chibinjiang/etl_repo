import json
import requests
from datetime import datetime
from freedom_house.model import FreedomCountryScoreModel


def main():
    status_map = {
        'not-free': FreedomCountryScoreModel.Status.NotFree,
        'free': FreedomCountryScoreModel.Status.Free,
        'partly-free': FreedomCountryScoreModel.Status.PartlyFree,
    }
    # template = "https://freedomhouse.org/api/map/fiw/{year}/json"
    for year in range(2017, 2021):
        print("Get Year: ", year)
        data = json.load(open(f'freedom_house/{year}.json', 'r'))
        for code, item in data['countries'].items():
            item['name'] = item['name'].strip()
            model = FreedomCountryScoreModel.get_by(
                FreedomCountryScoreModel.country == item['name'], FreedomCountryScoreModel.year == year)
            model = model or FreedomCountryScoreModel()
            model.country_abbr = code
            model.year = year
            model.country = item['name']
            if 'current' not in item:
                print("Ignore: ", item['name'])
                continue
            model.pr_score = item['current']['pr']
            model.cl_score = item['current']['cl']
            model.total_score = item['current']['total']
            model.status = status_map[item['current']['status']]
            model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()


def read_others():
    # 来自另一个repo
    import csv
    status_map = {
        'PF': FreedomCountryScoreModel.Status.PartlyFree,
        'NF': FreedomCountryScoreModel.Status.NotFree,
        'F': FreedomCountryScoreModel.Status.Free,
    }
    name_map = {
        'Bahamas': 'The Bahamas',
        'Cape Verde': 'Cabo Verde',
        'Macedonia': 'North Macedonia',
        'Congo (Kinshasa)': 'Democratic Republic of the Congo',
        'Congo (Brazzaville)': 'Republic of the Congo',
        'Swaziland': 'Eswatini',
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Cote dIvoire": "Côte d'Ivoire",
        "Serbia and Montenegro": "Serbia",
        "Sao Tome and Principe": "São Tomé and Príncipe",
    }
    file_name = 'freedom_house/AggregateScores{year}.csv'
    country_map = {m.country: m.country_abbr for m in FreedomCountryScoreModel.query()}
    for year in range(2006, 2019):
        for row in csv.DictReader(open(file_name.format(year=year), 'r', encoding='latin-1')):  # utf8无法编码
            country, status, total, pr, cl = row['Country/Territory'], row['Status'], row['Total Aggr'], row['PR Aggr'], row['CL Aggr']
            country = country.strip().strip('*')
            country = name_map[country] if country in name_map else country
            if not country:
                print(row)
                continue
            if country not in country_map:
                print("Unknown country: ", country)
            model = FreedomCountryScoreModel.get_by(
                FreedomCountryScoreModel.country == country, FreedomCountryScoreModel.year == year)
            model = model or FreedomCountryScoreModel()
            model.country = country
            model.year = year
            model.country_abbr = country_map.get(country)
            model.status = status_map[status]
            model.pr_score = pr
            model.cl_score = cl
            model.total_score = total if total else (pr + cl)
            model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()


def update_country_abbr():
    country_map = {m.country: m.country_abbr for m in FreedomCountryScoreModel.query() if m.country_abbr}
    for country in country_map:
        print(country)
        FreedomCountryScoreModel.update_many(
            FreedomCountryScoreModel.country == country, country_abbr=country_map[country])


def test():
    # 没用
    headers = {
        'authority': 'freedomhouse.org',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7',
    }
    response = requests.get('https://freedomhouse.org/api/map/fiw/2017/json', headers=headers)
    print(response.json())


if __name__ == '__main__':
    """
    python -m freedom_house.extract_freedom_score
    """
    read_others()
    main()

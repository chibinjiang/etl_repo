"""
世界人口数据: https://www.google.com/publicdata/explore

"""
import csv
from datetime import datetime

from freedom_house.models import CountryModel


def main():
    country_mapping = {
        'Somalia': 'Somaliland',
        "West Bank and Gaza": "Palestine",
    }
    name_cache = set()
    with open("freedom_house/CountryData.csv") as fr:
        for row in csv.DictReader(fr):
            if row['Province_State']:
                continue
            country, country_code, iso_code, population = row['Country_Region'], row['iso2'], row['iso3'], row['Population']
            country = country_mapping[country] if country in country_mapping else country
            name_cache.add(country)
            model = CountryModel.get_by(CountryModel.en_name == country) or CountryModel.get_by(CountryModel.iso_abbr == iso_code)
            if model:
                model.population = population
                model.updated = datetime.utcnow()
                model.save()
            else:
                print(country, country_code, iso_code)


if __name__ == '__main__':
    """
    python -m freedom_house.extract_coutry_info
    """
    main()

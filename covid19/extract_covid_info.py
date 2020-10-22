from datetime import datetime
from glob import glob
import pandas as pd
import re
from covid19.models import CountryCovid19Model
from freedom_house.model import CountryModel


def load_country_map():
    abbr_name_map = dict()
    for model in CountryModel.query():
        abbr_name_map[model.en_name] = model.iso_abbr
    return abbr_name_map


def main():
    """
    todo: 使用web data 更新最近的数据
    Incidence Rate = cases per 100,000 persons, 每十万人感染
    Case-Fatality Ratio (%) = Number recorded deaths / Number cases
    Active cases = total cases - total recovered - total deaths
    """
    name_mapping = {
        'US': 'United States',
        'UK': 'United Kingdom',
        'Bahamas': 'The Bahamas',
        'Congo (Brazzaville)': 'Republic of the Congo',
        'Congo (Kinshasa)': 'Democratic Republic of the Congo',
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Gambia": "The Gambia",
        "Korea, South": "South Korea",
        "Taiwan*": "Taiwan",
        "Saint Kitts and Nevis": "St. Kitts and Nevis",
        "Saint Lucia": "St. Lucia",
        "West Bank and Gaza": "Palestine",
        "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
        # "West Bank and Gaza": "Gaza Strip",
        "Czechia": "Czech Republic",
        "Sao Tome and Principe": "São Tomé and Príncipe",
        "Burma": "Myanmar",
        "Mainland China": "China",
    }
    country_mapping = load_country_map()
    agg_func = {
        'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum'
    }
    files = "COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/10-*.csv"
    files = sorted(glob(files))
    for file in files:
        rexp = re.search("(\d{2})-(\d{2})-(\d{4})\.csv$", file)
        year, month, day = rexp.group(3), rexp.group(1), rexp.group(2)
        df = pd.read_csv(file)
        if 'Country/Region' in df.columns:
            df['Country_Region'] = df['Country/Region']
        # 转换 要在 聚合之前
        df['Country_Region'] = df['Country_Region'].apply(lambda c: name_mapping[c] if c in name_mapping else c)
        for country, row in df.groupby('Country_Region').agg(agg_func).iterrows():
            confirmed, deaths, recovered = int(row['Confirmed']), int(row['Deaths']), int(row['Recovered'])
            if country not in country_mapping:
                print(country, confirmed, deaths, recovered)
                continue
            date = f"{year}-{month}-{day}"
            model = CountryCovid19Model.get_by(CountryCovid19Model.date == date, CountryCovid19Model.country == country) \
                    or CountryCovid19Model()
            model.country = country
            model.date = date
            model.country_abbr = country_mapping[country]
            model.confirmed = confirmed
            model.deaths = deaths
            model.recovered = recovered
            if not model.id:
                model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()


def save_daily_new():
    """
    这里假设所有国家地区都是从2020-01-22 开始的
    更新国家第一天的 daily new
    """
    sql = """
        update country_covid19 as t set daily_new = first_day.confirmed
        from (select country, date, confirmed from country_covid19 where date = '2020-01-22') as first_day
        where t.country = first_day.country and t.date = first_day.date;
    """
    CountryCovid19Model.execute_sql(sql)
    print("SQL1 done")
    sql = """
        update country_covid19 as c set daily_new = t.daily_new
        from (
             select now.country, now.date, (now.confirmed - ago.confirmed) as daily_new
             from country_covid19 as now join country_covid19 as ago
                on ago.date = TO_CHAR(TO_DATE(now.date, 'YYYY-MM-DD') - INTERVAL '1  day', 'YYYY-MM-DD')
                and now.country = ago.country
         ) as t where c.country = t.country and c.date = t.date;
    """
    CountryCovid19Model.execute_sql(sql)
    print("SQL2 done")


if __name__ == '__main__':
    """
    python -m covid19.extract_covid_info
    """
    main()
    save_daily_new()

import pandas as pd
from datetime import datetime
from freedom_house.models import CountryModel
from gdp.models import CountryGDPModel


def load_country_map():
    abbr_name_map = dict()
    for model in CountryModel.query():
        # abbr_name_map[model.iso_abbr] = model.en_name
        abbr_name_map[model.en_name] = model.iso_abbr
    return abbr_name_map


def main():
    mappings = {
        'Bahamas, The': 'The Bahamas',
        "Cote d'Ivoire": "Côte d'Ivoire",
        'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
        'Congo, Rep.': 'Republic of the Congo',
        'Egypt, Arab Rep.': 'Egypt',
        'Gambia, The': 'The Gambia',
        'Korea, Rep.': 'South Korea',
        'Korea, Dem. People’s Rep.': 'North Korea',
        'Hong Kong SAR, China': 'Hong Kong',
        'Lao PDR': 'Laos',
        'Macao SAR, China': 'Macao',
        'West Bank and Gaza': 'Palestine',
        'Russian Federation': 'Russia',
        "Sao Tome and Principe": "São Tomé and Príncipe",
        "Yemen, Rep.": 'Yemen',
        'Iran, Islamic Rep.': 'Iran',
        'Kyrgyz Republic': 'Kyrgyzstan',
    }
    country_map = load_country_map()
    df = pd.read_csv('./gdp/世界银行GDP_20200916_en.csv')
    for i, row in df.iterrows():
        country_name, country_code = row['Country Name'], row['Country Code']
        country_name = mappings[country_name] if country_name in mappings else country_name
        if country_name not in country_map:
            print("No country name: ", country_name, country_code)
            continue
        for year in range(1960, 2020):
            if not row.get(str(year)) or pd.isna(row[str(year)]):
                continue
            if CountryGDPModel.get_by(CountryGDPModel.year == year, CountryGDPModel.country == country_name):
                continue
            model = CountryGDPModel()
            model.country = country_name
            model.country_abbr = country_map[country_name]
            model.year = year
            model.gdp = row[str(year)]
            model.created = datetime.utcnow()
            model.updated = datetime.utcnow()
            model.save()


if __name__ == '__main__':
    """
    python -m gdp.extract_gdp_info
    """
    main()

"""
No country code:  ABW 阿拉伯联盟国家
No country code:  ARB
No country code:  ASM
No country code:  BMU
No country code:  CEB
No country code:  CHI
No country code:  CSS
No country code:  CUW
No country code:  CYM
No country code:  EAP
No country code:  EAR
No country code:  EAS
No country code:  ECA
No country code:  ECS
No country code:  EMU
No country code:  EUU
No country code:  FCS
No country code:  FRO
No country code:  GIB
No country code:  GRL
No country code:  GUM
No country code:  HIC
No country code:  HPC
No country code:  IBD
No country code:  IBT
No country code:  IDA
No country code:  IDB
No country code:  IDX
No country code:  IMN
No country code:  LAC
No country code:  LCN
No country code:  LDC
No country code:  LIC
No country code:  LMC
No country code:  LMY
No country code:  LTE
No country code:  MAC
No country code:  MAF
No country code:  MEA
No country code:  MIC
No country code:  MNA
No country code:  MNP
No country code:  NAC
No country code:  NCL
No country code:  OED
No country code:  OSS
No country code:  PRE
No country code:  PRI
No country code:  PSE
No country code:  PSS
No country code:  PST
No country code:  PYF
No country code:  SAS
No country code:  SSA
No country code:  SSF
No country code:  SST
No country code:  SXM
No country code:  TCA
No country code:  TEA
No country code:  TEC
No country code:  TLA
No country code:  TMN
No country code:  TSA
No country code:  TSS
No country code:  UMC
No country code:  VGB
No country code:  VIR
No country code:  WLD
No country code:  XKX
"""

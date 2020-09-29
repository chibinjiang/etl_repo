from datetime import datetime

from .model import CountryModel, FreedomCountryScoreModel

country2echart = {
    'South Korea': 'Dem. Rep. Korea',
    'North Korea': 'Korea',
    'Central African Republic': 'Central African Rep.',
    'Eswatini': 'Swaziland',
    'Czech Republic': 'Czech Rep.',
    'Democratic Republic of the Congo': 'Dem. Rep. Congo',
    'Dominican Republic': 'Dominican Rep.',
    'Laos': 'Lao PDR',
    'South Sudan': 'S. Sudan',
    'The Gambia': 'Gambia',
    'The Bahamas': 'Bahamas',
    'North Macedonia': 'Macedonia',
}

CountryNameMap = {
    "Afghanistan": "阿富汗",
    "Angola": "安哥拉",
    "Albania": "阿尔巴尼亚",
    "Algeria": "阿尔及利亚",
    "Argentina": "阿根廷",
    "Armenia": "亚美尼亚",
    "Australia": "澳大利亚",
    "Austria": "奥地利",
    "Azerbaijan": "阿塞拜疆",
    "Bahamas": "巴哈马",
    "Bangladesh": "孟加拉国",
    "Belgium": "比利时",
    "Benin": "贝宁",
    "Burkina Faso": "布基纳法索",
    "Burundi": "布隆迪",
    "Bulgaria": "保加利亚",
    "Bosnia and Herz.": "波斯尼亚和黑塞哥维那",
    "Belarus": "白俄罗斯",
    "Belize": "伯利兹",
    "Bermuda": "百慕大群岛",
    "Bolivia": "玻利维亚",
    "Brazil": "巴西",
    "Brunei": "文莱",
    "Bhutan": "不丹",
    "Botswana": "博茨瓦纳",
    "Cambodia": "柬埔寨",
    "Cameroon": "喀麦隆",
    "Canada": "加拿大",
    "Central African Rep.": "中非共和国",
    "Chad": "乍得",
    "Chile": "智利",
    "China": "中国",
    "Colombia": "哥伦比亚",
    "Congo": "刚果（布）",
    "Costa Rica": "哥斯达黎加",
    "Côte d'Ivoire": "科特迪瓦",
    "Croatia": "克罗地亚",
    "Cuba": "古巴",
    "Cyprus": "塞浦路斯",
    "Czech Rep.": "捷克",
    "Dem. Rep. Korea": "韩国",
    "Dem. Rep. Congo": "刚果（金）",
    "Denmark": "丹麦",
    "Djibouti": "吉布提",
    "Dominican Rep.": "多米尼加",
    "Ecuador": "厄瓜多尔",
    "Egypt": "埃及",
    "El Salvador": "萨尔瓦多",
    "Eq. Guinea": "赤道几内亚",
    "Eritrea": "厄立特里亚",
    "Estonia": "爱沙尼亚",
    "Ethiopia": "埃塞俄比亚",
    "Falkland Is.": "福克兰群岛",
    "Fiji": "斐济",
    "Finland": "芬兰",
    "France": "法国",
    "French Guiana": "法属圭亚那",
    "Fr. S. Antarctic Lands": "法属南部领地",
    "Gabon": "加蓬",
    "Gambia": "冈比亚",
    "Germany": "德国",
    "Georgia": "格鲁吉亚",
    "Ghana": "加纳",
    "Greece": "希腊",
    "Greenland": "格陵兰",
    "Guatemala": "危地马拉",
    "Guinea": "几内亚",
    "Guinea-Bissau": "几内亚比绍",
    "Guyana": "圭亚那",
    "Haiti": "海地",
    "Heard I. and McDonald Is.": "赫德岛和麦克唐纳群岛",
    "Honduras": "洪都拉斯",
    "Hungary": "匈牙利",
    "Iceland": "冰岛",
    "India": "印度",
    "Indonesia": "印度尼西亚",
    "Iran": "伊朗",
    "Iraq": "伊拉克",
    "Ireland": "爱尔兰",
    "Israel": "以色列",
    "Italy": "意大利",
    "Ivory Coast": "象牙海岸",
    "Jamaica": "牙买加",
    "Japan": "日本",
    "Jordan": "约旦",
    "Kashmir": "克什米尔",
    "Kazakhstan": "哈萨克斯坦",
    "Kenya": "肯尼亚",
    "Kosovo": "科索沃",
    "Kuwait": "科威特",
    "Kyrgyzstan": "吉尔吉斯斯坦",
    "Lao PDR": "老挝",
    "Latvia": "拉脱维亚",
    "Lebanon": "黎巴嫩",
    "Lesotho": "莱索托",
    "Liberia": "利比里亚",
    "Libya": "利比亚",
    "Lithuania": "立陶宛",
    "Luxembourg": "卢森堡",
    "Madagascar": "马达加斯加",
    "Macedonia": "马其顿",
    "Malawi": "马拉维",
    "Malaysia": "马来西亚",
    "Mali": "马里",
    "Mauritania": "毛里塔尼亚",
    "Mexico": "墨西哥",
    "Moldova": "摩尔多瓦",
    "Mongolia": "蒙古",
    "Montenegro": "黑山",
    "Morocco": "摩洛哥",
    "Mozambique": "莫桑比克",
    "Myanmar": "缅甸",
    "Namibia": "纳米比亚",
    "Netherlands": "荷兰",
    "New Caledonia": "新喀里多尼亚",
    "New Zealand": "新西兰",
    "Nepal": "尼泊尔",
    "Nicaragua": "尼加拉瓜",
    "Niger": "尼日尔",
    "Nigeria": "尼日利亚",
    "Korea": "朝鲜",
    "Northern Cyprus": "北塞浦路斯",
    "Norway": "挪威",
    "Oman": "阿曼",
    "Pakistan": "巴基斯坦",
    "Panama": "巴拿马",
    "Papua New Guinea": "巴布亚新几内亚",
    "Paraguay": "巴拉圭",
    "Peru": "秘鲁",
    "Republic of the Congo": "刚果共和国",
    "Philippines": "菲律宾",
    "Poland": "波兰",
    "Portugal": "葡萄牙",
    "Puerto Rico": "波多黎各",
    "Qatar": "卡塔尔",
    "Republic of Serbia": "塞尔维亚共和国",
    "Romania": "罗马尼亚",
    "Russia": "俄罗斯",
    "Rwanda": "卢旺达",
    "Samoa": "萨摩亚",
    "Saudi Arabia": "沙特阿拉伯",
    "Senegal": "塞内加尔",
    "Serbia": "塞尔维亚",
    "Sierra Leone": "塞拉利昂",
    "Slovakia": "斯洛伐克",
    "Slovenia": "斯洛文尼亚",
    "Solomon Is.": "所罗门群岛",
    "Somaliland": "索马里兰",
    "Somalia": "索马里",
    "South Africa": "南非",
    "S. Geo. and S. Sandw. Is.": "南乔治亚和南桑德威奇群岛",
    "S. Sudan": "南苏丹",
    "Spain": "西班牙",
    "Sri Lanka": "斯里兰卡",
    "Sudan": "苏丹",
    "Suriname": "苏里南",
    "Swaziland": "斯威士兰",
    "Sweden": "瑞典",
    "Switzerland": "瑞士",
    "Syria": "叙利亚",
    "Tajikistan": "塔吉克斯坦",
    "Tanzania": "坦桑尼亚",
    "Thailand": "泰国",
    "Timor-Leste": "东帝汶",
    "Togo": "多哥",
    "Trinidad and Tobago": "特立尼达和多巴哥",
    "Tunisia": "突尼斯",
    "Turkey": "土耳其",
    "Turkmenistan": "土库曼斯坦",
    "Uganda": "乌干达",
    "Ukraine": "乌克兰",
    "United Arab Emirates": "阿联酋",
    "United Kingdom": "英国",
    "United Republic of Tanzania": "坦桑尼亚联合共和国",
    "United States": "美国",
    "United States of America": "美利坚合众国",
    "Uruguay": "乌拉圭",
    "Uzbekistan": "乌兹别克斯坦",
    "Vanuatu": "瓦努阿图",
    "Venezuela": "委内瑞拉",
    "Vietnam": "越南",
    "West Bank": "西岸",
    "W. Sahara": "阿拉伯撒哈拉民主共和国",
    "Yemen": "也门",
    "Zambia": "赞比亚",
    "Zimbabwe": "津巴布韦"
}


def main():
    for i, model in enumerate(FreedomCountryScoreModel.distinct(['country', 'country_abbr'])):
        en_name = model.country
        echart_en_name = en_name if en_name in CountryNameMap else country2echart.get(en_name)
        if not echart_en_name:
            print(i, en_name, model.country_abbr)
        country_model = CountryModel()
        country_model.name = CountryNameMap.get(echart_en_name)
        country_model.en_name = en_name
        country_model.echart_name = echart_en_name
        country_model.iso_abbr = model.country_abbr
        country_model.code = ''
        country_model.created = datetime.utcnow()
        country_model.updated = datetime.utcnow()
        country_model.save()


if __name__ == '__main__':
    """
    python -m freedom_house.init_country
    """
    main()
"""
# 0 Abkhazia GEG None
# 4 Andorra AND None
6 Antigua and Barbuda ATG None
12 Bahrain BHR None
14 Barbados BRB None
21 Bosnia and Herzegovina BIH None
28 Cabo Verde CPV None
34 Chechnya None None
38 Comoros COM None
41 Crimea CRM None
49 Dominica DMA None
50 Dominican Republic DOM None
51 Eastern Donbas EDO None
55 Equatorial Guinea GNQ None
58 Eswatini SWZ None
64 Gaza Strip GAZ None
69 Grenada GRD None
80 Indian Kashmir INX None
86 Israeli Occupied Territories None None
93 Kiribati KIR None
103 Liechtenstein LIE None
109 Maldives MDV None
111 Malta MLT None
112 Marshall Islands MHL None
114 Mauritius MUS None
116 Micronesia FSM None
118 Monaco MCO None
124 Nagorno-Karabakh AZK None
126 Nauru NRU None
139 Pakistani Kashmir PKA None
140 Palau PLW None
141 Palestinian Authority Administered Territories None None
156 San Marino SMR None
157 São Tomé and Príncipe STP None
161 Seychelles SYC None
163 Singapore SGP None
166 Solomon Islands SLB None
171 South Ossetia GSO None
175 St. Kitts and Nevis KNA None
176 St. Lucia LCA None
177 St. Vincent and the Grenadines VCT None
192 Tonga TON None
193 Transnistria MDT None
198 Tuvalu TUV None
210 Western Sahara ESH None
"""

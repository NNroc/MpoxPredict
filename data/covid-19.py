import pandas as pd
from datetime import datetime

city_list = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建',
             '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '陕西',
             '甘肃', '新疆']
data_covid_19_filename = '../data_original/省级COVID-19逐日统计（境外输入）.csv'
covid_19_input_df = pd.read_csv(data_covid_19_filename, keep_default_na=False, encoding='gbk')
data = covid_19_input_df.values
all_city_covid_19_input_data = dict()

start_time = datetime.strptime('2022/12/6', '%Y/%m/%d')
for city_name in city_list:
    all_city_covid_19_input_data[city_name] = 0

for row in data:
    if row[1] in city_list:
        if row[8] == '':
            continue
        all_city_covid_19_input_data[row[1]] += int(row[8])

date_covid_19_input_save_filename = 'date_covid_19_input.csv'

with open(date_covid_19_input_save_filename, 'w', encoding='gbk') as f:
    for city_name in city_list:
        f.writelines(city_name + ',' + str(all_city_covid_19_input_data[city_name]) + '\n')

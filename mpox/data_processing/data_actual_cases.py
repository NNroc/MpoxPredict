'''实时患病人数'''

import pandas as pd
import datetime as dt
import csv
import os
from mpox.entity.entity import Records, Country


# 猴痘实时患病人数(具有传染性) =  (n 周 total_cases - n 周 new_deaths - (n - 2) 周 new_cases + (n + 1) 周 new_cases) * 0.935

def read_csv(filepath: str, encoding='GBK'):
    file_data = {}
    with open(filepath, 'r', encoding=encoding) as fp:
        reader = csv.DictReader(fp)
        for country_name in reader.fieldnames:
            all_country_name.append(country_name)
            file_data[country_name] = []
        for row in reader:
            for col in row:
                file_data[col].append(row[col])
    return file_data


def get_actual_case(total_cases, total_deaths, new_cases, new_deaths):
    actual_cases_data = {}
    for country in all_country_name:
        actual_cases_data[country] = []
        # 数据使用的总范围
        rg = len(total_cases[''])
        if country == '':
            continue
        for i in range(rg):
            if i == 0 or i == 1 or i == (rg - 1):
                continue
            # 这里要省略三条的数据
            if len(actual_cases_data['']) < rg - 3:
                actual_cases_data[''].append(total_cases[''][i])
            # 猴痘实时患病人数(具有传染性)
            # (n 周 total_cases - n 周 new_deaths - (n - 2) 周 new_cases + (n + 1) 周 new_cases) * 0.935
            # todo 公式存在问题
            actual_cases_week_num = (float(total_cases[country][i])
                                     - float(new_deaths[country][i])
                                     - float(new_cases[country][i - 2])
                                     + float(new_cases[country][i + 1])) * 0.935
            actual_cases_week_num = int(actual_cases_week_num)
            actual_cases_week_num = str(actual_cases_week_num)
            actual_cases_data[country].append(actual_cases_week_num)
    return actual_cases_data


dir_name = '../mpox_data'
# 所有的国家名字
all_country_name = []

mpox_global_total_cases_week = dir_name + '/mpox_global_total_cases_week.csv'
mpox_global_total_deaths_week = dir_name + '/mpox_global_total_deaths_week.csv'
mpox_global_new_cases_week = dir_name + '/mpox_global_new_cases_week.csv'
mpox_global_new_deaths_week = dir_name + '/mpox_global_new_deaths_week.csv'

mpox_global_actual_cases_week = dir_name + '/mpox_global_actual_cases_week.csv'

total_cases_week = read_csv(mpox_global_total_cases_week)
total_deaths_week = read_csv(mpox_global_total_deaths_week)
new_cases_week = read_csv(mpox_global_new_cases_week)
new_deaths_week = read_csv(mpox_global_new_cases_week)

actual_cases_week = get_actual_case(total_cases_week, total_deaths_week, new_cases_week, new_deaths_week)

# 保存为csv文件
with open(mpox_global_actual_cases_week, 'w', encoding='utf-8') as f:
    country_str = ''
    for country_name in all_country_name:
        if country_name == '':
            continue
        country_str = country_str + ',' + country_name
    f.writelines('date' + country_str + '\n')
    for row in range(len(actual_cases_week[''])):
        data_str = str(actual_cases_week[''][row])
        for country_name in all_country_name:
            if country_name == '':
                continue
            data_str = data_str + ',' + actual_cases_week[country_name][row]
        f.writelines(data_str + '\n')

'''实时患病人数'''

import pandas as pd
import datetime as dt
import csv
import os
from mpox.entity.entity import Records, Country


# 猴痘实时患病人数(具有传染性) =  n 周 total_cases - n 周 new_deaths - (n - 2) 周 new_cases + (n + 1) 周 new_cases

def read_csv(filepath: str, encoding='GBK'):
    file_data = []
    with open(filepath, 'r', encoding=encoding) as fp:
        reader = csv.DictReader(fp)
        use = None
        for x in reader:
            print(x)

    return file_data


dir_name = '../mpox_data'
# 所有的国家名字
all_country_name = []

mpox_global_total_cases_week = dir_name + '/mpox_global_total_cases_week.csv'
mpox_global_total_deaths_week = dir_name + '/mpox_global_total_deaths_week.csv'
mpox_global_new_cases_week = dir_name + '/mpox_global_new_cases_week.csv'
mpox_global_new_deaths_week = dir_name + '/mpox_global_new_deaths_week.csv'

total_cases_week = read_csv(mpox_global_total_cases_week)
total_deaths_week = read_csv(mpox_global_total_deaths_week)
new_cases_week = read_csv(mpox_global_new_cases_week)
new_deaths_week = read_csv(mpox_global_new_cases_week)
actual_cases_week = read_csv(mpox_global_new_deaths_week)

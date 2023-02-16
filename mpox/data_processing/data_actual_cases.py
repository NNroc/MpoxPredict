'''实时患病人数'''

import pandas as pd
import datetime as dt
import csv
import os


# 猴痘实时患病人数(具有传染性) =  n 周 total_cases - n 周 new_deaths - (n - 2) 周 new_cases + (n + 1) 周 new_cases

def read_csv(filepath: str, encoding='GBK'):
    with open(filepath, 'r', encoding=encoding) as fp:
        reader = csv.DictReader(fp)
        use = None
        for x in reader:
            if x['location'] not in all_country_name:
                if use is not None:
                    all_country[use.country_name] = use
                all_country_name.append(x['location'])
                use = Country(x['location'])
            use.records[x['date']] = Records(x['date'],
                                             x['total_cases'], x['total_deaths'],
                                             x['new_cases'], x['new_deaths'])
        return 1


dir_name = '../mpox_data'

mpox_global_total_cases_week = dir_name + '/mpox_global_total_cases_week.csv'
mpox_global_total_deaths_week = dir_name + '/mpox_global_total_deaths_week.csv'
mpox_global_new_cases_week = dir_name + '/mpox_global_new_cases_week.csv'
mpox_global_new_deaths_week = dir_name + '/mpox_global_new_deaths_week.csv'

total_cases_week = read_csv(mpox_global_total_cases_week)
total_deaths_week = read_csv(mpox_global_total_deaths_week)
new_cases_week = read_csv(mpox_global_new_cases_week)
new_deaths_week = read_csv(mpox_global_new_cases_week)
actual_cases_week = read_csv(mpox_global_new_deaths_week)

import math

import pandas as pd
import datetime

data_mpox_global_actual_cases_week_path = 'mpox/mpox_data/mpox_global_actual_cases_week.csv'
data_flight_global_week_path = 'data_original/20230221 数据整理(军事医学研究院)英文版.xlsx'
data_departures_path = 'data_original/出入境人数.xlsx'

# departures
data_departures_df = pd.read_excel(data_departures_path, sheet_name=0)
data_departures_df = data_departures_df.values

# mpox 实际新增患病
data_mpox_actual_cases_week_df = pd.read_csv(data_mpox_global_actual_cases_week_path, header=None)
data_mpox_actual_cases_week_df = data_mpox_actual_cases_week_df.values

# 出入境航司
data_flight_global_week_df = pd.read_excel(data_flight_global_week_path, sheet_name=0, header=None)
data_flight_global_week_df = data_flight_global_week_df.values

# 风险矩阵（以 出入境航司 为基准）
data_risk_matrix = dict()
# 时间序列
data_date = []
# mpox 实际新增患病
data_mpox_actual_cases_week = dict()
# mpox 所涉及的国外城市
data_all_city_external = [i for i in data_mpox_actual_cases_week_df[0]]
data_all_city_external = data_all_city_external[1:]
# 出入境航司
data_flight_global_week = dict()
# 出入境航司 所涉及的国内城市
data_all_city_internal = [i for i in data_flight_global_week_df[0]]
data_all_city_internal = data_all_city_internal[5:]
# 各国家出境人次
data_departures = dict()
for country, departures, x1, x2, x3, x4, x5, x6, x7, x8, x9 in data_departures_df:
    data_departures[country] = float(departures)

for city_name in data_all_city_external:
    data_mpox_actual_cases_week[city_name] = dict()

for row in range(1, len(data_mpox_actual_cases_week_df)):
    for idx in range(1, len(data_all_city_external) + 1):
        date = data_mpox_actual_cases_week_df[row][0]
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime('%Y-%m-%d')
        # 加入时间序列
        if date not in data_date:
            data_date.append(date)
        # 对应 (时间, 人数)
        data_mpox_actual_cases_week[data_all_city_external[idx - 1]][date] = \
            data_mpox_actual_cases_week_df[row][idx]

for row in range(1, len(data_flight_global_week_df)):
    for idx in range(5, len(data_all_city_internal) + 5):
        # 中国的城市名称
        city_name = data_flight_global_week_df[row][1]
        if city_name not in data_flight_global_week:
            data_flight_global_week[city_name] = dict()
            data_risk_matrix[city_name] = dict()
        date = data_flight_global_week_df[row][0]
        date = date.split(' ')[2]
        date = date.replace('/', '-')
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime('%Y-%m-%d')
        if date not in data_flight_global_week[city_name]:
            data_flight_global_week[city_name][date] = dict()
            data_risk_matrix[city_name][date] = dict()
        # 对应 (时间, 人数)
        data_flight_global_week[city_name][date][data_all_city_internal[idx - 5]] = \
            data_flight_global_week_df[row][idx]

# 遍历中国航班中涉及的城市
for flight_idx in data_flight_global_week:
    # 城市的日期
    for date in data_date:
        sum = 0
        # 城市的日期 外来国家的航班数
        if date not in data_flight_global_week[flight_idx]:
            continue
        for country in data_flight_global_week[flight_idx][date]:
            if country in data_mpox_actual_cases_week:
                flight_num = float(data_flight_global_week[flight_idx][date][country])
                actual_num = float(data_mpox_actual_cases_week[country][date])
                departure_num = data_departures[country]
                # departure_num = 1
                sum += flight_num * actual_num / departure_num
        data_risk_matrix[flight_idx][date] = sum

# 风险矩阵保存位置
data_risk_matrix_save_filename = 'risk_matrix.csv'
with open(data_risk_matrix_save_filename, 'w', encoding='gbk') as f:
    row_str = '风险矩阵'
    for city in data_risk_matrix:
        row_str = row_str + ',' + city
    f.writelines(row_str + '\n')
    for date in data_date:
        date_str = str(date)
        for city in data_risk_matrix:
            if date in data_risk_matrix[city] and data_risk_matrix[city][date] != 0.0 and math.log10(
                    data_risk_matrix[city][date] * 10000) > 0:
                date_str = date_str + ',' + str(math.log10(data_risk_matrix[city][date] * 10000))
            else:
                date_str = date_str + ',0'
        f.writelines(date_str + '\n')

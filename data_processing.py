import pandas as pd

data_mpox_global_actual_cases_week_path = 'mpox/mpox_data/mpox_global_actual_cases_week.csv'
data_flight_global_week_path = 'data_original/20230221 数据整理(军事医学研究院).xlsx'

# mpox 实际新增患病
data_mpox_actual_cases_week_df = pd.read_csv(data_mpox_global_actual_cases_week_path, header=None)
data_mpox_actual_cases_week_df = data_mpox_actual_cases_week_df.values

# 出入境航司
data_flight_global_week_df = pd.read_excel(data_flight_global_week_path, sheet_name=0, header=None)
data_flight_global_week_df = data_flight_global_week_df.values

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

for city_name in data_all_city_external:
    data_mpox_actual_cases_week[city_name] = dict()

for city_name in data_all_city_internal:
    data_flight_global_week[city_name] = dict()

for row in range(1, len(data_mpox_actual_cases_week_df)):
    for idx in range(1, len(data_all_city_external) + 1):
        # 对应 (时间, 人数)
        data_mpox_actual_cases_week[data_all_city_external[idx - 1]][data_mpox_actual_cases_week_df[row][0]] = \
            data_mpox_actual_cases_week_df[row][idx]

for row in range(1, len(data_flight_global_week_df)):
    for idx in range(5, len(data_all_city_internal) + 5):
        # 对应 (时间, 人数)
        data_flight_global_week[data_all_city_internal[idx - 5]][data_flight_global_week_df[row][0]] = \
            data_flight_global_week_df[row][idx]

print()

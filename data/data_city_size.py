import pandas as pd
import datetime as dt
import csv
import os
import pandas as pd
import datetime as dt
import xlrd

from mpox.entity.entity import Records, Country

data_flight_filename = '20230221 数据整理(军事医学研究院).xlsx'
data_flight_save_filename = 'data_flight.csv'

# 出现的所有城市名字
all_city_name = []
# 出现的所有时间序列名字
all_date_series = []
# 合并的航班数据
data_flight = dict()

# 获取 xlsx
df = pd.read_excel(data_flight_filename)
data = df.values
for row in data:
    if row[0] not in all_date_series:
        all_date_series.append(row[0])
        data_flight[row[0]] = [row[2], row[3]]
    else:
        data_flight[row[0]] = [data_flight[row[0]][0] + row[2], data_flight[row[0]][1] + row[3]]
    if row[1] not in all_city_name:
        all_city_name.append(row[1])

# 根据城市名排序
all_city_name.sort()

# 保存航班文件
with open(data_flight_save_filename, 'w', encoding='utf-8') as f:
    f.writelines('date,到达国家,国内航司,境外航司''\n')
    for row in data_flight:
        f.writelines(row + ',中国,' + str(data_flight[row][0]) + ',' + str(data_flight[row][1]) + '\n')

# 筛选城市规模信息
data_city_size_filename = '城市规模参数.xlsx'
# 保存文件
data_city_size_save_filename = 'city_size.csv'
# 最终的筛选结果
data_city_size = dict()
# 未筛查到的城市
city_not_have = list.copy(all_city_name)

df = pd.read_excel(data_city_size_filename)
data = df.values
for row in data:
    if row[1][-1] == '市':
        row[1] = row[1][:-1]
    if row[1] in all_city_name:
        # [Proportion of high school and above, age60]
        data_city_size[row[1]] = [row[19], row[31]]
        city_not_have.remove(row[1])

# 保存筛选过的城市规模参数文件
with open(data_city_size_save_filename, 'w', encoding='utf-8') as f:
    f.writelines('city,Proportion of high school and above,age60''\n')
    for row in data_city_size:
        f.writelines(row + ',' + str(data_city_size[row][0]) + ',' + str(data_city_size[row][1]) + '\n')

print(len(all_city_name))
print(all_city_name)
print(city_not_have)

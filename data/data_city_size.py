import pandas as pd
import datetime as dt
import csv
import os
import xlrd

data_flight_filename = '20230221 数据整理(军事医学研究院).xlsx'
# data_flight_save_filename = 'data_flight.csv'

# 出现的所有城市名字
all_city_name = []
# 出现的所有时间序列名字
all_date_series = []
# 合并的航班数据
data_flight = dict()

# 获取 xlsx
df1 = pd.read_excel(data_flight_filename, sheet_name='Sheet1')
data = df1.values
# df2 = pd.read_excel(data_flight_filename, sheet_name='Sheet3')
for row in data:
    if row[0] not in all_date_series:
        all_date_series.append(row[0])
    if row[1] not in all_city_name:
        all_city_name.append(row[1])
    data_flight[row[0]] = row[2] + row[3]

# 根据城市名排序
all_city_name.sort()

# 筛选城市规模信息
data_city_size_filename = '城市规模参数.xlsx'
# 保存文件
data_city_size_save_filename = 'city_size.csv'
# 最终的筛选结果
data_city_size = dict()
# 未筛查到的城市
city_not_have = list.copy(all_city_name)

# 读取sheet列表的元素
df = pd.read_excel(data_city_size_filename, sheet_name='all')
data = df.values
for row in data:
    if row[1][-1] == '市':
        row[1] = row[1][:-1]
    if row[1] in all_city_name:
        # [Proportion of high school and above, age60]
        data_city_size[row[1]] = [row[19], row[31]]
        city_not_have.remove(row[1])

# 保存航班文件,xlsx操作更方便......
# with open(data_flight_save_filename, 'w', encoding='gbk') as f:
#     other_city=''
#     f.writelines('date,到达国家,国内外航司'+other_city+'\n')
#     for row in data_flight:
#         f.writelines(row + ',中国,' + str(data_flight[row][0]) + ',' + str(data_flight[row][1]) + '\n')

# 保存筛选过的城市规模参数文件
with open(data_city_size_save_filename, 'w', encoding='gbk') as f:
    f.writelines('city,Proportion of high school and above,age60''\n')
    for row in data_city_size:
        f.writelines(row + ',' + str(data_city_size[row][0]) + ',' + str(data_city_size[row][1]) + '\n')

print(len(all_city_name))
print(all_city_name)
print(city_not_have)

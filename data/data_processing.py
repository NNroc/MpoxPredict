import pandas as pd
import datetime as dt
import csv
import os
import xlrd
from data.entity.entity import Statistical

data_flight_filename = '20230221 数据整理(军事医学研究院).xlsx'
data_flight_save_filename = 'data_flight.csv'

# 出现的所有城市名字
all_city_name = []
# 出现的所有时间序列名字
all_date_series = []
# 合并的航班数据
data_flight = dict()

# 获取 xlsx
df1 = pd.read_excel(data_flight_filename, sheet_name='Sheet1')
data = df1.values
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
# 城市规模参数保存文件
data_city_size_save_filename = 'data_city_size.csv'
# 最终的筛选结果
data_city_size = dict()
# 未筛查到的城市
city_not_have = list.copy(all_city_name)
# 航班信息
data_flight_filename = ''
# 航班信息保存文件
data_flight_save_filename = 'data_flight.csv'

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
    f.writelines('city,Proportion of high school and above,age60\n')
    for row in data_city_size:
        f.writelines(row + ',' + str(data_city_size[row][0]) + ',' + str(data_city_size[row][1]) + '\n')

print(len(all_city_name))
print(all_city_name)
print(city_not_have)

# 筛选出的城市统计数据
all_statistical_data = []
# 筛选出的城市统计数据保存地址
statistical_data_save_filename = 'city_statistical.csv'
# 城市统计数据
for year in range(2001, 2022):
    statistical_data_path = '中国城市统计年鉴2001—2021年/中国城市统计年鉴_' + str(year) + '年/中国城市统计年鉴_' + str(
        year) + '年(Excel版本)/地级市（及以上城市）统计资料（' + str(year) + '年）.xlsx'
    print(statistical_data_path)
    statistical_data_df = pd.read_excel(statistical_data_path, sheet_name='Sheet1')
    statistical_data = statistical_data_df.values
    for row in range(4, len(statistical_data)):
        if statistical_data[row][0] == '市':
            statistical_data[row][0] = statistical_data[row][0][:-1]
        if statistical_data[row][0] not in all_city_name:
            continue
        # 2001~2017的数据格式与2018~2021的数据格式不一样
        statistical = None
        if year < 2018:
            statistical = Statistical(year, statistical_data[row][0], statistical_data[row][4],
                                      statistical_data[row][9], statistical_data[row][11], statistical_data[row][12],
                                      statistical_data[row][13], statistical_data[row][14], statistical_data[row][15],
                                      statistical_data[row][16], statistical_data[row][21], statistical_data[row][96],
                                      statistical_data[row][97], statistical_data[row][98], statistical_data[row][99],
                                      statistical_data[row][100], statistical_data[row][101],
                                      statistical_data[row][104], statistical_data[row][110],
                                      statistical_data[row][113], statistical_data[row][115])
        else:
            statistical = Statistical(year, statistical_data[row][0], statistical_data[row][5],
                                      statistical_data[row][9], statistical_data[row][11], statistical_data[row][12],
                                      statistical_data[row][13], statistical_data[row][14], statistical_data[row][15],
                                      statistical_data[row][16], statistical_data[row][21], statistical_data[row][96],
                                      statistical_data[row][97], statistical_data[row][98], statistical_data[row][99],
                                      statistical_data[row][100], statistical_data[row][101],
                                      statistical_data[row][104], statistical_data[row][110],
                                      statistical_data[row][113], statistical_data[row][115])
        all_statistical_data.append(statistical)

with open(statistical_data_save_filename, 'w', encoding='gbk') as f:
    f.writelines(
        '年份,城市,城镇常住人口(市辖区),居住用地面积,公园绿地面积,建成区绿化覆盖率(%),工业颗粒物排放量(吨),工业二氧化硫排放量(吨),工业氮氧化物排放量(吨),细颗粒物年平均浓度(微克/立方米),'
        '人均地区生产总值(元)全市,医院数(个)全市,医院数(个)市辖区,医院床位数(张)全市,医院床位数(张)市辖区,执业(助理)医师数(人)全市,执业(助理)医师数(人)市辖区,职工基本医疗保险参保人数全市,'
        '境内公路总里程(公里)全市,全年公共汽(电)车客运总量(万人次),公路客运量(万人)\n')
    for statistical_data in all_statistical_data:
        f.writelines(
            str(statistical_data.year) + str(statistical_data.city) + str(statistical_data.population_total_city) + str(
                statistical_data.area_living) + str(statistical_data.area_parks_green) +
            str(statistical_data.green_covered_area) + str(statistical_data.industrial_particulate_emission) + str(
                statistical_data.sulphur_dioxide_emission) +
            str(statistical_data.nitrogen_dioxide_emission) + str(statistical_data.pm25) + str(
                statistical_data.capita_grp_total_city) + str(statistical_data.hospitals_total_city) + str(
                statistical_data.hospitals_districts_city) + str(statistical_data.hospitals_beds_total_city) + str(
                statistical_data.hospitals_beds_districts_city) + str(statistical_data.doctors_total_city) + str(
                statistical_data.doctors_districts_city) + str(
                statistical_data.basic_medical_care_system_total_city) + str(statistical_data.mileage_total_city) + str(
                statistical_data.bus_passenger) + str(statistical_data.highway_passenger) + '\n')

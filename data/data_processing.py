import pandas as pd
import os
from data.entity.Statistical import Statistical
from data.entity.Homosexuality import Homosexuality


# os.listdir()方法获取文件夹名字，返回数组
def getAllFiles(targetDir):
    listFiles = os.listdir(targetDir)
    return listFiles


# 出现的所有城市名字
all_city_name = []
# 出现的所有时间序列名字
all_date_series = []
# 合并的航班数据
data_flight = dict()

# 根据城市名排序
all_city_name.sort()

# 筛选城市规模信息
data_city_size_filename = '../data_original/城市规模参数.xlsx'
# 城市规模参数保存文件
data_city_size_save_filename = 'data_city_size.csv'
# 最终的筛选结果
data_city_size = dict()
# 未筛查到的城市
city_not_have = list.copy(all_city_name)

# # 航班信息
# data_flight_filename = ''
# # 航班信息保存文件
# data_flight_save_filename = 'data_flight.csv'

# 获取航班数据 xlsx
# df1 = pd.read_excel(data_flight_filename, sheet_name='Sheet1', keep_default_na=False)
# data = df1.values
# for row in data:
#     if row[0] not in all_date_series:
#         all_date_series.append(row[0])
#     if row[1] not in all_city_name:
#         all_city_name.append(row[1])
#     data_flight[row[0]] = row[2] + row[3]

# 读取sheet列表的元素
df = pd.read_excel(data_city_size_filename, sheet_name='all', keep_default_na=False)
data = df.values
for row in data:
    if row[1][-1] == '市':
        row[1] = row[1][:-1]
    if row[1] in all_city_name:
        # [Proportion of high school and above, age0_19, age20_39, age60]
        data_city_size[row[1]] = [row[19], row[28], row[29], row[31]]
        city_not_have.remove(row[1])

# 保存航班文件
# with open(data_flight_save_filename, 'w', encoding='gbk') as f:
#     other_city = ''
#     f.writelines('date,到达国家,国内外航司'+other_city+'\n')
#     for row in data_flight:
#         f.writelines(row + ',中国,' + str(data_flight[row][0]) + ',' + str(data_flight[row][1]) + '\n')

# 保存筛选过的城市规模参数文件
with open(data_city_size_save_filename, 'w', encoding='gbk') as f:
    f.writelines('city,Proportion of high school and above,age0_19,age20_39,age60\n')
    for row in data_city_size:
        f.writelines(row + ',' + str(data_city_size[row][0]) + ',' + str(data_city_size[row][1]) + ',' + str(
            data_city_size[row][2]) + ',' + str(data_city_size[row][3]) + '\n')

# 去除特殊城市
for i in city_not_have:
    all_city_name.remove(i)
print(len(all_city_name))
print(all_city_name)

# 筛选出的城市统计数据
all_statistical_data = []
# 筛选出的城市统计数据保存地址
statistical_data_save_filename = 'data_city_statistical.csv'
# 城市统计数据
statistical_data_path = '../data_original/地级市（及以上城市）统计资料（2021年）.xlsx'
statistical_data_df = pd.read_excel(statistical_data_path, sheet_name='Sheet1', keep_default_na=False)
# 将空值赋值为，这个有问题用不了
# statistical_data_df.fillna('暂无')
statistical_data = statistical_data_df.values
for row in range(5, len(statistical_data)):
    statistical_data[row][0] = statistical_data[row][0].strip()
    if statistical_data[row][0][-1] == '市':
        statistical_data[row][0] = statistical_data[row][0][:-1]
    if statistical_data[row][0] not in all_city_name:
        # print(statistical_data[row][0])
        continue
    # 各年的数据格式不一样，暂用2021年发布的
    statistical = Statistical(2021, statistical_data[row][0], statistical_data[row][5], statistical_data[row][6],
                              statistical_data[row][9], statistical_data[row][11], statistical_data[row][12],
                              statistical_data[row][13], statistical_data[row][14], statistical_data[row][15],
                              statistical_data[row][16], statistical_data[row][21], statistical_data[row][100],
                              statistical_data[row][101], statistical_data[row][102], statistical_data[row][103],
                              statistical_data[row][104], statistical_data[row][105], statistical_data[row][108],
                              statistical_data[row][114], statistical_data[row][116], statistical_data[row][117],
                              statistical_data[row][118], statistical_data[row][119])
    all_statistical_data.append(statistical)

# 预测同性恋数据，已有2007到2011，预测到2021
homosexuality_filename = '../data_original/中国城市同性恋数据.xlsx'
homosexuality_df = pd.read_excel(homosexuality_filename, sheet_name=0, keep_default_na=False, header=None)
homosexuality_df = homosexuality_df.values
# 完整的数据
all_homosexuality_data = dict()
# 年数，索引从1开始
year_num = len(homosexuality_df)
# 城市数，索引从1开始
city_num = len(homosexuality_df[0])
# 往后预测的年数
predict_num = 8
# 将所有城市初始化
for i in range(1, city_num):
    # 除去不要的城市
    if homosexuality_df[0][i] not in all_city_name:
        continue
    all_homosexuality_data[homosexuality_df[0][i]] = Homosexuality(homosexuality_df[0][i],
                                                                   homosexuality_df[1][0], year_num - 1, predict_num)
for i in range(1, year_num):
    for j in range(1, city_num):
        # 除去不要的城市
        if homosexuality_df[0][j] not in all_city_name:
            continue
        all_homosexuality_data[homosexuality_df[0][j]].add(homosexuality_df[i][j], int(homosexuality_df[i][0]))

for city in all_homosexuality_data:
    all_homosexuality_data[city].predict()

# 保存目录
data_homosexuality_save_filename = 'data_homosexuality.csv'
# 保存预测结果
with open(data_homosexuality_save_filename, 'w', encoding='gbk') as f:
    city_str = ''
    for city in all_homosexuality_data:
        city_str = city_str + ',' + city
    f.writelines('date' + city_str + '' + '\n')
    for i in range(1, year_num + predict_num):
        year = i + int(homosexuality_df[1][0]) - 1
        f.writelines(str(year))
        for city in all_homosexuality_data:
            f.writelines(',' + str(int(all_homosexuality_data[city].data[i - 1])))
        f.writelines('\n')

# 数据汇总
data_save_filename = 'data.csv'
for s in all_statistical_data:
    s.merge_people_message(data_city_size[s.city][0], data_city_size[s.city][1], data_city_size[s.city][2],
                           data_city_size[s.city][3])
    for city in all_homosexuality_data:
        if city == s.city:
            s.merge_homosexuality(all_homosexuality_data[city], 2022)
            break

# 增加气温数据
data_temperature_filename = '../data_original/2000-2020年分市逐年气温'
files = getAllFiles(data_temperature_filename)
for file in files:
    # 年份 省份 城市 城市代码 平均气温
    data_temperature_df = pd.read_excel(data_temperature_filename + '/' + file, sheet_name=0, keep_default_na=False)
    data_temperature_df = data_temperature_df.values
    for year, province, city, city_code, temperature in data_temperature_df:
        if year != 2020:
            continue
        if city[-1] == '市':
            city = city[:-1]
        for sta in all_statistical_data:
            if sta.city == city:
                sta.merge_temperature(temperature)
                break

# 增加降水量数据
data_water_filename = '../data_original/1980年～2020年中国各城市降水量数据.xlsx'
data_water_df = pd.read_excel(data_water_filename, sheet_name=0, keep_default_na=False)
data_water_df = data_water_df.values
for year, province, province_code, city, city_code, water in data_water_df:
    if year != 2020:
        continue
    if city[-1] == '市':
        city = city[:-1]
    for sta in all_statistical_data:
        if sta.city == city:
            sta.merge_water(water)
            break

# 增加日照数据
data_sun_filename = '../data_original/2000-2020年372个城市年度日照时数.xlsx'
data_sun_df = pd.read_excel(data_sun_filename, sheet_name=0, keep_default_na=False)
data_sun_df = data_sun_df.values
for year, province_code, province, city_code, city, sun in data_sun_df:
    if year != 2020:
        continue
    if city[-1] == '市':
        city = city[:-1]
    for sta in all_statistical_data:
        if sta.city == city:
            sta.merge_sun(sun)
            break

# 增加COVID-19数据
data_covid_filename = '../data_original/COVID-19逐日统计.csv'
data_covid_df = pd.read_csv(data_covid_filename, encoding='gbk')
data_covid_df = data_covid_df.values
for idx, province, city, city_code, date, x1, x2, x3, x4, x5, x6, case, cure, die in data_covid_df:
    if date != '2022.12.06':
        continue
    for sta in all_statistical_data:
        if sta.city == city:
            sta.merge_covid(case, cure, die)
            break

# covid-19 经查询修整的数据
# data_covid19_save_filename = 'data_covid19.csv'
# with open(data_covid19_save_filename, 'w', encoding='gbk') as f:
#     f.writelines('年份,城市,累计确诊,累计治愈,累计死亡\n')
#     for statistical_data in all_statistical_data:
#         f.writelines(
#             str(statistical_data.year) + ','
#             + str(statistical_data.city) + ','
#             + str(statistical_data.case) + ','
#             + str(statistical_data.cure) + ','
#             + str(statistical_data.die)
#             + '\n')

with open(data_save_filename, 'w', encoding='gbk') as f:
    f.writelines(
        '年份,城市,城镇常住人口(市辖区),建成区面积（平方公里）市辖区,居住用地面积,公园绿地面积,建成区绿化覆盖率(%),工业颗粒物排放量(吨),工业二氧化硫排放量(吨),工业氮氧化物排放量(吨),细颗粒物年平均浓度(微克/立方米),人均地区生产总值(元)全市,医院数(个)全市,医院数(个)市辖区,医院床位数(张)全市,医院床位数(张)市辖区,执业(助理)医师数(人)全市,执业(助理)医师数(人)市辖区,职工基本医疗保险参保人数全市,境内公路总里程(公里)全市,年末实有公共汽（电）车营运车辆数（辆）,全年公共汽(电)车客运总量(万人次),年末实有巡游出租汽车营运车数（辆）,公路客运量(万人),高中及以上比例(%),年龄0到19比例(%),年龄20到39比例(%),年龄60以上比例(%),同性恋人数,城市降水量数据,城市年度日照时数,城市逐年气温,covid-19 累计确诊,covid-19 累计治愈,covid-19 累计死亡\n')
    for statistical_data in all_statistical_data:
        f.writelines(
            str(statistical_data.year) + ','
            + str(statistical_data.city) + ','
            + str(statistical_data.population_total_city) + ','
            + str(statistical_data.built_up_total_city) + ','
            + str(statistical_data.area_living) + ','
            + str(statistical_data.area_parks_green) + ','
            + str(statistical_data.green_covered_area) + ','
            + str(statistical_data.industrial_particulate_emission) + ','
            + str(statistical_data.sulphur_dioxide_emission) + ','
            + str(statistical_data.nitrogen_dioxide_emission) + ','
            + str(statistical_data.pm25) + ','
            + str(statistical_data.capita_grp_total_city) + ','
            + str(statistical_data.hospitals_total_city) + ','
            + str(statistical_data.hospitals_districts_city) + ','
            + str(statistical_data.hospitals_beds_total_city) + ','
            + str(statistical_data.hospitals_beds_districts_city) + ','
            + str(statistical_data.doctors_total_city) + ','
            + str(statistical_data.doctors_districts_city) + ','
            + str(statistical_data.basic_medical_care_system_total_city) + ','
            + str(statistical_data.mileage_total_city) + ','
            + str(statistical_data.bus_num) + ','
            + str(statistical_data.bus_passenger) + ','
            + str(statistical_data.taxi_num) + ','
            + str(statistical_data.highway_passenger) + ','
            + str(statistical_data.high_school_above) + ','
            + str(statistical_data.age0_19) + ','
            + str(statistical_data.age20_39) + ','
            + str(statistical_data.age60) + ','
            + str(int(statistical_data.homosexuality)) + ','
            + str(statistical_data.water) + ','
            + str(statistical_data.sun) + ','
            + str(statistical_data.temperature) + ','
            + str(statistical_data.case) + ','
            + str(statistical_data.cure) + ','
            + str(statistical_data.die)
            + '\n')

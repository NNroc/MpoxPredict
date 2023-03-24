import pandas as pd
import os
from data.entity.WorldEconomy import WorldEconomy


# os.listdir()方法获取文件夹名字，返回数组
def getAllFiles(targetDir):
    listFiles = os.listdir(targetDir)
    return listFiles


# 所有的城市情况
country_dict = dict()
# 各城市所拥有的元素
value_name_list = []

data_world_economy_dir = '../data_original/世界各国社经'
files = getAllFiles(data_world_economy_dir)
for file in files:
    sheet = pd.read_excel(data_world_economy_dir + '/' + file, sheet_name=None)
    sheet_list = list(sheet.keys())
    for sheet_name in sheet_list:
        data_world_economy_df = pd.read_excel(data_world_economy_dir + '/' + file, sheet_name=sheet_name,
                                              keep_default_na=False, header=None, usecols='A,B')
        data_world_economy_df = data_world_economy_df.values
        value_name = data_world_economy_df[0][1]
        value_name_list.append(value_name)
        for country_name, value in data_world_economy_df:
            if country_name == '国家':
                continue
            if country_name not in country_dict:
                country_dict[country_name] = WorldEconomy(country_name)
            country_dict[country_name].sheet_list_name.append(value_name)
            country_dict[country_name].sheet_list_value.append(value)

# 保存目录
data_world_economy_save_filename = 'data_world_economy.csv'
# 保存预测结果
with open(data_world_economy_save_filename, 'w', encoding='gbk') as f:
    country_str = '国家'
    for value_name in value_name_list:
        country_str = country_str + ',' + value_name
    f.writelines(country_str + '\n')
    for country_name in country_dict:
        country_str = country_name
        country_value_num = 0
        for value_name in value_name_list:
            if value_name == country_dict[country_name].sheet_list_name[country_value_num]:
                country_str = country_str + ',' + str(country_dict[country_name].sheet_list_value[country_value_num])
                country_value_num = country_value_num + 1
                if country_value_num >= len(country_dict[country_name].sheet_list_name):
                    break
            else:
                country_str = country_str + ',' + 'NULL'
        # print(country_str)
        f.writelines(country_str + '\n')

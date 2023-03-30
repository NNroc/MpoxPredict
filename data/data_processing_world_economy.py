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
    data_world_economy_df = pd.read_csv(data_world_economy_dir + '/' + file, keep_default_na=False, header=None)
    data_world_economy_df = data_world_economy_df.values
    row_num = data_world_economy_df.shape[0]
    col_num = data_world_economy_df.shape[1]
    value_name_list_this = []
    need_to_append = WorldEconomy()
    for i in range(2, col_num):
        value_name_list.append(data_world_economy_df[0][i])
        value_name_list_this.append(data_world_economy_df[0][i])
        need_to_append.sheet_list_name.append(data_world_economy_df[0][i])
    for indx in range(1, row_num):
        use_flag = True
        for i in range(2, col_num):
            if data_world_economy_df[indx][i] is None:
                use_flag = False
                break
        # 如果相等就更新，反之写入country_dict中
        if (need_to_append.country_name == None or need_to_append.country_name == data_world_economy_df[indx][0]) \
                and use_flag:
            need_to_append.country_name = data_world_economy_df[indx][0]
            need_to_append.year = data_world_economy_df[indx][1]
            need_to_append.sheet_list_value = []
            for i in range(2, col_num):
                need_to_append.sheet_list_value.append(data_world_economy_df[indx][i])
        elif need_to_append.country_name != None and need_to_append.country_name != data_world_economy_df[indx][0]:
            country_name = need_to_append.country_name
            if country_name not in country_dict:
                country_dict[country_name] = WorldEconomy(country_name)
            for i in range(2, col_num):
                country_dict[country_name].sheet_list_name.append(value_name_list_this[i - 2])
                country_dict[country_name].sheet_list_value.append(need_to_append.sheet_list_value[i - 2])
            # 初始化
            need_to_append = WorldEconomy()
            indx = indx - 1
    if need_to_append.country_name != None:
        country_name = need_to_append.country_name
        if country_name not in country_dict:
            country_dict[country_name] = WorldEconomy(country_name)
        for i in range(2, col_num):
            country_dict[country_name].sheet_list_name.append(value_name_list_this[i - 2])
            country_dict[country_name].sheet_list_value.append(need_to_append.sheet_list_value[i - 2])
        # 初始化
        need_to_append = WorldEconomy()

# 保存目录
data_world_economy_save_filename = 'data_world_economy.csv'
# 设置填充符
fill_str = ''
# 保存预测结果
with open(data_world_economy_save_filename, 'w', encoding='gbk') as f:
    world_economy_str = 'Country'
    for value_name in value_name_list:
        world_economy_str = world_economy_str + ',' + "\"" + value_name + "\""
    f.writelines(world_economy_str + '\n')
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
                country_str = country_str + ',' + fill_str
        f.writelines(country_str + '\n')

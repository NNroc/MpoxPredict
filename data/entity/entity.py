from data.utils.grey import grey_predict


class Statistical:
    def __init__(self, year, city, population_total_city, area_living, area_parks_green, green_covered_area,
                 industrial_particulate_emission, sulphur_dioxide_emission, nitrogen_dioxide_emission, pm25,
                 capita_grp_total_city, hospitals_total_city, hospitals_districts_city,
                 hospitals_beds_total_city, hospitals_beds_districts_city, doctors_total_city, doctors_districts_city,
                 basic_medical_care_system_total_city, mileage_total_city, bus_passenger, highway_passenger):
        # 年份
        self.year = year
        # 城市
        self.city = city
        # 城镇常住人口(市辖区)
        self.population_total_city = population_total_city
        # 居住用地面积
        self.area_living = area_living
        # 公园绿地面积
        self.area_parks_green = area_parks_green
        # 建成区绿化覆盖率 (%)
        self.green_covered_area = green_covered_area
        # 工业颗粒物排放量(吨)
        self.industrial_particulate_emission = industrial_particulate_emission
        # 工业二氧化硫排放量(吨)
        self.sulphur_dioxide_emission = sulphur_dioxide_emission
        # 工业氮氧化物排放量(吨)
        self.nitrogen_dioxide_emission = nitrogen_dioxide_emission
        # 细颗粒物年平均浓度 (微克/立方米)
        self.pm25 = pm25
        # 人均地区生产总值 (元)	全市
        self.capita_grp_total_city = capita_grp_total_city
        # 医院数 (个) 全市
        self.hospitals_total_city = hospitals_total_city
        # 医院数 (个) 市辖区
        self.hospitals_districts_city = hospitals_districts_city
        # 医院床位数 (张) 全市
        self.hospitals_beds_total_city = hospitals_beds_total_city
        # 医院床位数 (张) 市辖区
        self.hospitals_beds_districts_city = hospitals_beds_districts_city
        # 执业(助理)医师数 (人) 全市
        self.doctors_total_city = doctors_total_city
        # 执业(助理)医师数 (人) 市辖区
        self.doctors_districts_city = doctors_districts_city
        # 职工基本医疗保险参保人数 全市
        self.basic_medical_care_system_total_city = basic_medical_care_system_total_city
        # 境内公路总里程 (公里) 全市
        self.mileage_total_city = mileage_total_city
        # 全年公共汽(电)车客运总量 (万人次)
        self.bus_passenger = bus_passenger
        # 公路客运量 (万人)
        self.highway_passenger = highway_passenger

        # 下列数据需进行合并
        # 学历高中及以上比例
        self.high_school_above = ''
        # 年龄60以上比例
        self.age60 = ''

    def merge(self, high_school_above, age60):
        self.high_school_above = high_school_above
        self.age60 = age60


class Homosexuality:
    def __init__(self, city, year_start, year_num, predict_num):
        self.city = city
        self.year_start = int(year_start)
        self.year_num = int(year_num)
        self.data = [-1 for _ in range(year_num)]
        self.predict_num = int(predict_num)

    def add(self, data, year):
        self.data[year - self.year_start] = data

    def predict(self):
        data_predict = grey_predict(self.data, self.predict_num)
        self.data.extend(data_predict)

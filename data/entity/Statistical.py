from data.entity.Homosexuality import Homosexuality


class Statistical:
    def __init__(self, year, city, population_total_city, built_up_total_city, area_living, area_parks_green,
                 green_covered_area, industrial_particulate_emission, sulphur_dioxide_emission,
                 nitrogen_dioxide_emission, pm25, capita_grp_total_city, hospitals_total_city, hospitals_districts_city,
                 hospitals_beds_total_city, hospitals_beds_districts_city, doctors_total_city, doctors_districts_city,
                 basic_medical_care_system_total_city, mileage_total_city, bus_num, bus_passenger, taxi_num,
                 highway_passenger):
        # 年份
        self.year = year
        # 城市
        self.city = city
        # 城镇常住人口(市辖区)
        self.population_total_city = population_total_city
        # 建成区面积（平方公里）市辖区
        self.built_up_total_city = built_up_total_city
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
        # 年末实有公共汽（电）车营运车辆数（辆）
        self.bus_num = bus_num
        # 全年公共汽(电)车客运总量 (万人次)
        self.bus_passenger = bus_passenger
        # 年末实有巡游出租汽车营运车数（辆）
        self.taxi_num = taxi_num
        # 公路客运量 (万人)
        self.highway_passenger = highway_passenger

        # 下列数据需进行合并
        # 学历高中及以上比例
        self.high_school_above = ''
        # 年龄60以上比例
        self.age60 = ''
        # 同性恋人数
        self.homosexuality = -1

    def merge_people_message(self, high_school_above, age0_19, age20_39, age60):
        self.high_school_above = high_school_above
        self.age0_19 = age0_19
        self.age20_39 = age20_39
        self.age60 = age60

    def merge_homosexuality(self, homosexuality: Homosexuality, year: int):
        self.homosexuality = homosexuality.data[year - homosexuality.year_start]

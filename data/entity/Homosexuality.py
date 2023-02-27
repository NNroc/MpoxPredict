import pandas as pd
from data.utils.gm11 import gm11
from data.utils.gm1n import gm1n


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
        data = pd.DataFrame(self.data)
        data_predict = gm11(data, predstep=self.predict_num)
        data_predict.fit()
        data_predict.predict()
        data_predict.loss()
        data_predict.errors()
        # print('GM(1,1)的拟合值是： ', data_predict.fit())
        # print(f'GM(1,1)的{data_predict.predstep}步预测值是： ', data_predict.predict())
        # print('GM(1,1)的预测误差是： ', data_predict.loss())
        # print(data_predict.errors())
        self.data.extend(list(data_predict.pred_values))

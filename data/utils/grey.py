import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from decimal import Decimal


def grey_predict(history_data: list, predict_num: int):
    '''
    :param history_data: 原始序列
    :param predict_num: 需要预测的长度
    :return:
    '''
    n = len(history_data)
    X0 = np.array(history_data)

    # 累加生成
    history_data_agg = [sum(history_data[0:i + 1]) for i in range(n)]
    X1 = np.array(history_data_agg)

    # 计算数据矩阵B和数据向量Y
    B = np.zeros([n - 1, 2])
    Y = np.zeros([n - 1, 1])
    for i in range(0, n - 1):
        B[i][0] = -0.5 * (X1[i] + X1[i + 1])
        B[i][1] = 1
        Y[i][0] = X0[i + 1]

    # 计算GM(1,1)微分方程的参数a和u
    # A = np.zeros([2,1])
    A = np.linalg.inv(B.T.dot(B)).dot(B.T).dot(Y)
    a = A[0][0]
    u = A[1][0]

    # 建立灰色预测模型
    XX0 = np.zeros(n)
    XX0[0] = X0[0]
    for i in range(1, n):
        XX0[i] = (X0[0] - u / a) * (1 - math.exp(a)) * math.exp(-a * (i))

    # 模型精度的后验差检验
    e = 0  # 求残差平均值
    for i in range(0, n):
        e += (X0[i] - XX0[i])
    e /= n

    # 求历史数据平均值
    aver = 0
    for i in range(0, n):
        aver += X0[i]
    aver /= n

    # 求历史数据方差
    s12 = 0
    for i in range(0, n):
        s12 += (X0[i] - aver) ** 2
    s12 /= n

    # 求残差方差
    s22 = 0
    for i in range(0, n):
        s22 += ((X0[i] - XX0[i]) - e) ** 2
    s22 /= n

    # 求后验差比值
    C = s22 / s12

    # 求小误差概率
    cout = 0
    for i in range(0, n):
        if abs((X0[i] - XX0[i]) - e) < 0.6754 * math.sqrt(s12):
            cout = cout + 1
        else:
            cout = cout
    P = cout / n
    # 返回的预测序列
    f = np.zeros(predict_num)

    for i in range(0, predict_num):
        f[i] = (X0[0] - u / a) * (1 - math.exp(a)) * math.exp(-a * (i + n))
    # if (C < 0.35 and P > 0.75):
    #     # 预测精度为一级
    #     # print('往后predict_num各年负荷为：')
    #     f = np.zeros(predict_num)
    #     for i in range(0, predict_num):
    #         f[i] = (X0[0] - u / a) * (1 - math.exp(a)) * math.exp(-a * (i + n))
    # else:
    #     print('灰色预测法不适用')
    return f


class GM11:
    def __init__(self):
        self.f = None

    def isUsable(self, X0):
        '''判断是否通过光滑检验'''
        X1 = X0.cumsum()
        rho = [X0[i] / X1[i - 1] for i in range(1, len(X0))]
        rho_ratio = [rho[i + 1] / rho[i] for i in range(len(rho) - 1)]
        print("rho:", rho)
        print("rho_ratio:", rho_ratio)
        flag = True
        for i in range(2, len(rho) - 1):
            if rho[i] > 0.5 or rho[i + 1] / rho[i] >= 1:
                flag = False
            if rho[-1] > 0.5:
                flag = False
        if flag:
            print("数据通过光滑校验")
        else:
            print("该数据未通过光滑校验")
            '''判断是否通过级比检验'''
            lambds = [X0[i - 1] / X0[i] for i in range(1, len(X0))]
            X_min = np.e ** (-2 / (len(X0) + 1))
            X_max = np.e ** (2 / (len(X0) + 1))
            for lambd in lambds:
                if lambd < X_min or lambd > X_max:
                    print('该数据未通过级比检验')
                    return
                print('该数据通过级比检验')

    def train(self, X0):
        X1 = X0.cumsum()
        Z = (np.array([-0.5 * (X1[k - 1] + X1[k]) for k in range(1, len(X1))])).reshape(len(X1) - 1, 1)
        # 数据矩阵A、B
        A = (X0[1:]).reshape(len(Z), 1)
        B = np.hstack((Z, np.ones(len(Z)).reshape(len(Z), 1)))
        # 求灰参数
        a, u = np.linalg.inv(np.matmul(B.T, B)).dot(B.T).dot(A)
        u = Decimal(u[0])
        a = Decimal(a[0])
        print("灰参数a：", a, "，灰参数u：", u)
        self.f = lambda k: (Decimal(X0[0]) - u / a) * np.exp(-a * k) + u / a

    def predict(self, k):
        X1_hat = [float(self.f(k)) for k in range(k)]
        X0_hat = np.diff(X1_hat)
        X0_hat = np.hstack((X1_hat[0], X0_hat))
        return X0_hat

    def evaluate(self, X0_hat, X0):
        '''
        根据后验差比及小误差概率判断预测结果
        :param X0_hat: 预测结果
        :param X0:
        :return:
        '''
        S1 = np.std(X0, ddof=1)
        # 原始数据样本标准差
        S2 = np.std(X0 - X0_hat, ddof=1)
        # 残差数据样本标准差
        C = S2 / S1
        # 后验差比
        Pe = np.mean(X0 - X0_hat)
        temp = np.abs((X0 - X0_hat - Pe)) < 0.6745 * S1
        p = np.count_nonzero(temp) / len(X0)
        # 计算小误差概率
        print("原数据样本标准差：", S1)
        print("残差样本标准差：", S2)
        print("后验差比：", C)
        print("小误差概率p：", p)


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False
    # 步骤二（解决坐标轴负数的负号显示问题）
    # 原始数据X
    data = pd.read_excel('./siwei_day_traffic.xlsx')
    X = data[data['week_day'] == '周五'].jam_num[:5].astype(float).values
    print(X)
    # 训练集
    X_train = X[:int(len(X) * 0.7)]
    # 测试集
    X_test = X[int(len(X) * 0.7):]
    model = GM11()
    model.isUsable(X_train)
    # 判断模型可行性
    model.train(X_train)
    # 训练
    Y_pred = model.predict(len(X))
    # 预测
    Y_train_pred = Y_pred[:len(X_train)]
    Y_test_pred = Y_pred[len(X_train):]
    score_test = model.evaluate(Y_test_pred, X_test)
    # 评估
    # 可视化
    plt.grid()
    plt.plot(np.arange(len(X_train)), X_train, '->')
    plt.plot(np.arange(len(X_train)), Y_train_pred, '-o')
    plt.legend(['负荷实际值', '灰色预测模型预测值'])
    plt.title('训练集')
    plt.show()
    plt.grid()
    plt.plot(np.arange(len(X_test)), X_test, '->')
    plt.plot(np.arange(len(X_test)), Y_test_pred, '-o')
    plt.legend(['负荷实际值', '灰色预测模型预测值'])
    plt.title('测试集')
    plt.show()

import numpy as np
import math


def grey_predict(history_data: list, predict_num: int):
    n = len(history_data)
    X0 = np.array(history_data)

    # �ۼ�����
    history_data_agg = [sum(history_data[0:i + 1]) for i in range(n)]
    X1 = np.array(history_data_agg)

    # �������ݾ���B����������Y
    B = np.zeros([n - 1, 2])
    Y = np.zeros([n - 1, 1])
    for i in range(0, n - 1):
        B[i][0] = -0.5 * (X1[i] + X1[i + 1])
        B[i][1] = 1
        Y[i][0] = X0[i + 1]

    # ����GM(1,1)΢�ַ��̵Ĳ���a��u
    # A = np.zeros([2,1])
    A = np.linalg.inv(B.T.dot(B)).dot(B.T).dot(Y)
    a = A[0][0]
    u = A[1][0]

    # ������ɫԤ��ģ��
    XX0 = np.zeros(n)
    XX0[0] = X0[0]
    for i in range(1, n):
        XX0[i] = (X0[0] - u / a) * (1 - math.exp(a)) * math.exp(-a * (i))

    # ģ�;��ȵĺ�������
    e = 0  # ��в�ƽ��ֵ
    for i in range(0, n):
        e += (X0[i] - XX0[i])
    e /= n

    # ����ʷ����ƽ��ֵ
    aver = 0
    for i in range(0, n):
        aver += X0[i]
    aver /= n

    # ����ʷ���ݷ���
    s12 = 0
    for i in range(0, n):
        s12 += (X0[i] - aver) ** 2
    s12 /= n

    # ��в��
    s22 = 0
    for i in range(0, n):
        s22 += ((X0[i] - XX0[i]) - e) ** 2
    s22 /= n

    # �������ֵ
    C = s22 / s12

    # ��С������
    cout = 0
    for i in range(0, n):
        if abs((X0[i] - XX0[i]) - e) < 0.6754 * math.sqrt(s12):
            cout = cout + 1
        else:
            cout = cout
    P = cout / n
    # ���ص�Ԥ������
    f = np.zeros(predict_num)
    if (C < 0.35 and P > 0.95):
        # Ԥ�⾫��Ϊһ��
        # print('����predict_num���긺��Ϊ��')
        f = np.zeros(predict_num)
        for i in range(0, predict_num):
            f[i] = (X0[0] - u / a) * (1 - math.exp(a)) * math.exp(-a * (i + n))
    else:
        print('��ɫԤ�ⷨ������')
    return f

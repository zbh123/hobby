# coding：utf-8

import numpy as np
from mf import load_data, save_file, prediction, top_k


def train(V, r, maxCycles, e):
    """ 非负矩阵分解
    :param V: 评分矩阵
    :param r:分解后矩阵的维数
    :param maxCycles:最大迭代次数
    :param e:最小误差
    :return:
    """
    m, n = np.shape(V)
    # 1、初始化矩阵
    P = np.mat(np.random.random((m, r)))
    Q = np.mat(np.random.random((r, n)))
    # 2、非负矩阵分解
    for step in range(maxCycles):
        # 计算预测值
        V_pre = P * Q
        # 计算预测值与真实值的误差
        E = V - V_pre
        err = 0.0
        for i in range(m):
            for j in range(n):
                # 平方损失函数
                err += E[i, j] * E[i, j]
        if err < e:
            break
        if step % 1000 == 0:
            print('\titeration is {}, loss is: {}'.format(step, err))

        a = P.T * V
        b = P.T * P * Q
        for i_1 in range(r):
            for j_1 in range(n):
                if b[i_1, j_1] != 0:
                    # 更新矩阵Q
                    Q[i_1, j_1] = Q[i_1, j_1] * a[i_1, j_1] / b[i_1, j_1]
        c = V * Q.T
        d = P * Q * Q.T
        for i_2 in range(m):
            for j_2 in range(r):
                if d[i_2, j_2] != 0:
                    # 更新矩阵P
                    P[i_2, j_2] = P[i_2, j_2] * c[i_2, j_2] / d[i_2, j_2]
    return P, Q


if __name__ == '__main__':
    # 1、导入用户商品数据
    print("------------ 1. load data ------------")
    data = load_data("data.txt")
    # 2、计算商品之间的相似性
    print("------------ 2. training -------------")
    p, q = train(data, 5, 10000, 1e-5)
    # 3、保存分解后的结果
    print("------------ 3. save decompose ------------")
    save_file('W', p)
    save_file('H', q)
    # 4.预测
    print('--------4. prediction ----------')
    predict = prediction(data, p, q, 0)
    # 5.进行top-K推荐
    print("------------ 5. top_k recommendation ------------")
    top_recom = top_k(predict, 2)
    print(top_recom)

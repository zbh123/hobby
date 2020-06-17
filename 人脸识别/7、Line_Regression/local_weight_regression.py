# coding:utf-8
import numpy as np
from linear_regression_train import load_data
import matplotlib.pyplot as plt


def lwlr(feature, label, k):
    ''' 局部加权线性回归
    :param feature: 特征
    :param label: 标签
    :param k: 核函数的系数
    :return:
    '''
    m = np.shape(feature)[0]
    predict = np.zeros(m)
    weights = np.mat(np.eye(m))    # 生成对角矩阵
    for i in range(m):
        for j in range(m):
            diff = feature[i, ] - feature[j, ]
            weights[j, j] = np.exp(diff * diff.T / (-2.0 * k ** 2))
        xTx = feature.T * (weights * feature)
        ws = xTx.I * (feature.T * (weights * label))
        predict[i] = feature[i, ] * ws
    return predict


if __name__ == "__main__":
    # 1、导入数据集
    feature, label = load_data("data.txt")
    predict = lwlr(feature, label, 0.01)
    m = np.shape(predict)[0]
    x1List = []
    y1List = []
    for i in range(m):
        x1List.append(feature[i, 1])
        y1List.append(label[i])
        # print(feature[i, 1], predict[i])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x1List, predict, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='green')
    plt.show()

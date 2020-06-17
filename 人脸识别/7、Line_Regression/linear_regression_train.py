# coding:utf-8
import numpy as np
from math import pow
import matplotlib.pyplot as plt


def least_square(feature, label):
    ''' 最小二乘法
    :param feature:特征
    :param label: 标签
    :return:
    '''
    w = (feature.T * feature).I * feature.T * label
    return w


def newton(feature, label, iterMax, sigma, delta):
    ''' 牛顿迭代法
    :param feature:特征
    :param label: 标签
    :param iterMax: 最大迭代次数
    :param sigma: 牛顿法参数
    :param delta: 牛顿法参数
    :return:
    '''
    n = np.shape(feature)[1]
    w = np.mat(np.zeros((n, 1)))
    it = 0
    while it <= iterMax:
        # print(it)
        g = first_derivative(feature, label, w)   # 一阶导
        G = second_derivative(feature)            # 二阶导
        d = -G.I * g        # G.I矩阵的逆
        m = get_min_m(feature, label, sigma, delta, d, w, g)     # 得到最小的m
        w = w + pow(sigma, m) * d
        if it % 10 == 0:
            print('\t-----iteration:{}, error:{}----'.format(it, get_error(feature, label, w)[0, 0]))
        it += 1
    return w


def get_min_m(feature, label, sigma, delta, d, w, g):
    ''' 计算步长中最小的值m,基于Armijo搜索，使得f(x + param) <= f(x) + param
    :param feature: 特征
    :param label: 标签
    :param sigma: 全局牛顿参数
    :param delta: 全局牛顿参数
    :param d: 负的一阶导数除以二阶导数值
    :param w:
    :param g: 一阶导数值
    :return:
    '''
    m = 0
    while True:
        w_new = w + pow(sigma, m) * d
        left = get_error(feature, label, w_new)
        right = get_error(feature, label, w) + delta * pow(sigma, m) * g.T * d
        if left <= right:
            break
        else:
            m += 1
    return m


def get_error(feature, label, w):
    ''' 计算误差，线性回归的损失函数: (y - y1) ** 2 / 2
    :param feature:特征
    :param label: 标签
    :param w: 线性回归的参数w
    :return:
    '''
    return (label - feature * w).T * (label - feature * w) / 2


def first_derivative(feature, label, w):
    ''' 一阶导 = （label - feature*w） * feature
    :param feature: 特征
    :param label:  标签
    :param w: 线性回归参数w
    :return:
    '''
    m, n = np.shape(feature)
    g = np.mat(np.zeros((n, 1)))
    for i in range(m):
        err = label[i, 0] - feature[i, ] * w
        for j in range(n):
            g[j, ] -= err * feature[i, j]
    return g


def second_derivative(feature):
    ''' 计算二阶导数
    :param feature:
    :return:
    '''
    m, n = np.shape(feature)
    G = np.mat(np.zeros((n, n)))
    for i in range(m):
        x_left = feature[i, ].T
        x_right = feature[i, ]
        G += x_left * x_right
    return G


def load_data(file_path):
    f = open(file_path)
    feature = []
    label = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split('\t')
        feature_tmp.append(1)
        for i in range(len(lines) - 1):
            feature_tmp.append(float(lines[i]))
        feature.append(feature_tmp)
        label.append(float(lines[-1]))
    f.close()
    return np.mat(feature), np.mat(label).T


def save_model(file_name, w):
    f = open(file_name, 'w')
    m, n = np.shape(w)
    for i in range(m):
        w_tmp = []
        for j in range(n):
            w_tmp.append(str(w[i, j]))
        f.write('\t'.join(w_tmp))
        f.write('\n')
    f.close()


def draw(file_name, feature, w):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    predict = feature * w
    m = np.shape(predict)[0]
    for i in range(m):
        y1List.append(predict[i, 0])
    f = open(file_name, 'r')
    for line in f.readlines():
        lines = line.strip().split('\t')

        x0List.append(float(lines[0]))
        y0List.append(float(lines[1]))
        x1List.append(float(lines[0]))

    f.close()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='black')
    plt.show()


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    feature, label = load_data("data.txt")
    # 2、最下二乘求解
    print("--------- 2.training ------------")
    w = least_square(feature, label)
    # 3、牛顿迭代
    print("--------- 3.save model ------------")
    # w = newton(feature, label, 50, 0.1, 0.5)
    # 4、保存结果
    print("--------- 4.save result ------------")
    save_model('weights', w)
    draw("data.txt", feature, w)

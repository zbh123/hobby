# coding:utf-8
import numpy as np
import math
import matplotlib.pyplot as plt

MinPts = 5


def dbscan(data, eps, MinPts):
    """ DBSCAN算法
    :param data: 需要聚类的数据集
    :param eps: 半径
    :param MinPts: 半径内的最少的数据点的个数
    :return:types(mat)每个样本的类型：核心点，边界点，噪音点
            sub_class(mat)每个样本所属的类别
    """
    m = np.shape(data)[0]
    # 区分核心点1，边界0和噪音点-1
    types = np.mat(np.zeros((1, m)))
    sub_class = np.mat(np.zeros((1, m)))
    # 用于判断该点是否被处理过,0表示未处理过
    dealed = np.mat(np.zeros((m, 1)))
    # 计算每个数据点之间的距离
    dis = distance(data)
    # 用于标记类别
    number = 1
    # 对于每一个点进行处理
    for i in range(m):
        # 找到未处理的点
        if dealed[i, 0] == 0:
            # 找到第i个点到其他所有点的距离
            D = dis[i, ]
            # 找到半径eps内的所有点
            ind = find_eps(D, eps)
            # 区分点的类型
            # 边界点
            if 1 < len(ind) < MinPts + 1:
                types[0, i] = 0
                sub_class[0, i] = 0
            # 噪音点
            if len(ind) == 1:
                types[0, i] = -1
                sub_class[0, i] = -1
            # 核心点
            if len(ind) >= MinPts + 1:
                types[0, i] = 1
                for x in ind:
                    sub_class[0, x] = number
                # 判断核心点是否密度可达
                while len(ind) > 0:
                    dealed[ind[0], 0] = 1
                    D = dis[ind[0], ]
                    tmp = ind[0]
                    del ind[0]
                    ind_1 = find_eps(D, eps)
                    if len(ind_1) > 1:
                        # 处理非噪音点
                        for x1 in ind_1:
                            sub_class[0, x1] = number
                        if len(ind_1) >= MinPts + 1:
                            types[0, tmp] = 1
                        else:
                            types[0, tmp] = 0
                        for j in range(len(ind_1)):
                            if dealed[ind_1[j], 0] == 0:
                                dealed[ind_1[j], 0] = 1
                                ind.append(ind_1[j])
                                sub_class[0, ind_1[j]] = number
                number += 1
    # 最后处理所有未分类点为噪音点
    ind_2 = ((sub_class == 0).nonzero())[1]
    for x in ind_2:
        sub_class[0, x] = -1
        types[0, x] = -1
    return types, sub_class


def find_eps(distance_D, eps):
    """ 找到距离小于、等于eps的样本的下标
    :param distance_D: 样本i和其他样本之间的距离
    :param eps: 半径的大小
    :return:
    """
    ind = []
    n = np.shape(distance_D)[1]
    for j in range(n):
        if distance_D[0, j] <= eps:
            ind.append(j)
    return ind


def distance(data):
    """ 计算样本点之间的距离
    :param data: 样本
    :return: 返回的是轴对称矩阵，符合每个点到相邻点的距离
    """
    m, n = np.shape(data)
    dis = np.mat(np.zeros((m, m)))
    for i in range(m):
        for j in range(i, m):
            # 计算i和j之间的距离
            tmp = 0
            for k in range(n):
                tmp += (data[i, k] - data[j, k]) * (data[i, k] - data[j, k])
            dis[i, j] = np.sqrt(tmp)
            dis[j, i] = dis[i, j]
    print(dis)
    return dis


def load_data(file_path):
    f = open(file_path)
    data = []
    for line in f.readlines():
        data_tmp = []
        lines = line.strip().split("\t")
        for x in lines:
            data_tmp.append(float(x.strip()))
        data.append(data_tmp)
    f.close()
    return np.mat(data)


def epsilon(data, MinPts):
    """ 计算半径
    :param data:
    :param MinPts:
    :return:
    """
    m, n = np.shape(data)
    xMax = np.max(data, 0)      # np.max(data, axis) 沿纵轴查找最大、最小值
    xMin = np.min(data, 0)
    # np.prod计算矩阵所有元素的乘积，可以指定axis，输出的结果个数就是另一个轴的大小
    eps = ((np.prod(xMax - xMin) * MinPts * math.gamma(0.5 * n + 1)) / (m * math.sqrt(math.pi ** n))) ** (1.0 / n)
    return eps


def save_result(file_name, data):
    f = open(file_name, 'w')
    n = np.shape(data)[1]
    tmp = []
    for i in range(n):
        tmp.append(str(data[0, i]))
    f.write("\n".join(tmp))
    f.close()


def draw(data, sub_class):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    x2List = []
    y2List = []
    x3List = []
    y3List = []
    m = np.shape(data)[0]
    for i in range(m):
        if sub_class[0, i] == 1.0:
            x0List.append(data[i, 0])
            y0List.append(data[i, 1])
        if sub_class[0, i] == 2.0:
            x1List.append(data[i, 0])
            y1List.append(data[i, 1])
        if sub_class[0, i] == 3.0:
            x2List.append(data[i, 0])
            y2List.append(data[i, 1])
        if sub_class[0, i] == -1.0:
            x3List.append(data[i, 0])
            y3List.append(data[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='green')
    ax.scatter(x2List, y2List, s=10, c='blue')
    ax.scatter(x3List, y3List, s=10, c='black')
    plt.show()


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    testData = load_data("data.txt")
    # 2、计算半径
    print("--------- 2.calculate eps ------------")
    eps = epsilon(testData, MinPts)
    # 3、通过DBSCAN算法进行训练
    print("--------- 3.DBSCAN ------------")
    types, sub_class = dbscan(testData, eps, MinPts)
    # 4、保存结果
    print("--------- 4.save result ------------")
    save_result('types', types)
    save_result('sub_class', sub_class)

    draw(testData, sub_class)




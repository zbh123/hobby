# ---coding:utf-8---
import numpy as np
from random import random
import matplotlib.pyplot as plt
from k_means_train import load_data, kmeans, distance, save_result

FLOAT_MAX = 1e100


def get_centroids(points, k):
    """ KMeans++的初始化聚类中心的方法
    :param points: 样本
    :param k: 聚类中心个数
    :return:
    """
    m, n = np.shape(points)
    cluster_centers = np.mat(np.zeros((k, n)))
    # 1.随机选择一个样本点为第一个聚类中心
    index = np.random.randint(0, m)
    cluster_centers[0, ] = np.copy(points[index, ])
    # 2.初始化一个距离的序列
    d = [0.0 for _ in range(m)]
    for i in range(1, k):
        sum_all = 0
        for j in range(m):
            # 3.对每一个样本找到最近的聚类中心点。与每个聚类中心计算距离，距离最小的那个确认分类
            d[j] = nearest(points[j, ], cluster_centers[0:i, ])
            # 4.将所有最短距离相加
            sum_all += d[j]
        # 5.取得sum_all之间的随机数(0-1之间)
        sum_all *= random()
        # 6.以概率获得距离最远的样本点作为聚类中心点
        for j, di in enumerate(d):
            sum_all -= di
            if sum_all > 0:
                continue
            cluster_centers[i] = np.copy(points[j, ])
            break
    return cluster_centers


def nearest(point, cluster_centers):
    """ 计算point和cluster_centers之间的最小距离
    :param point: 当前的样本点
    :param cluster_centers: 当前的已经初始化的聚类中心
    :return:
    """
    min_dist = FLOAT_MAX
    m = np.shape(cluster_centers)[0]  # 当前已经初始化的聚类中心的个数
    for i in range(m):
        # 计算point与每个聚类中心的距离
        d = distance(point, cluster_centers[i,])
        # 选择最短的距离
        if min_dist > d:
            min_dist = d
    return min_dist


def draw(data, sub, centroids):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    x2List = []
    y2List = []
    x3List = []
    y3List = []
    x4List = []
    y4List = []
    m = np.shape(data)[0]
    for i in range(m):
        if float(sub[i, 0]) == 0.0:
            x0List.append(data[i, 0])
            y0List.append(data[i, 1])
        elif float(sub[i, 0]) == 1.0:
            x1List.append(data[i, 0])
            y1List.append(data[i, 1])
        elif float(sub[i, 0]) == 2.0:
            x2List.append(data[i, 0])
            y2List.append(data[i, 1])
        elif float(sub[i, 0]) == 3.0:
            x3List.append(data[i, 0])
            y3List.append(data[i, 1])
    m, n = np.shape(centroids)
    for i in range(m):
        x4List.append(centroids[i, 0])
        y4List.append(centroids[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='yellow')
    ax.scatter(x2List, y2List, s=10, c='green')
    ax.scatter(x3List, y3List, s=10, c='blue')
    ax.scatter(x4List, y4List, s=10, c='black')
    plt.show()


if __name__ == "__main__":
    k = 4  # 聚类中心的个数
    file_path = "data.txt"
    # 1、导入数据
    print("---------- 1.load data ------------")
    data = load_data(file_path)
    # 2、KMeans++的聚类中心初始化方法
    print("---------- 2.K-Means++ generate centers ------------")
    centroids = get_centroids(data, k)
    # 3、聚类计算
    print("---------- 3.kmeans ------------")
    subCenter = kmeans(data, k, centroids)
    # 4、保存所属的类别文件
    print("---------- 4.save subCenter ------------")
    save_result("sub_pp", subCenter)
    # 5、保存聚类中心
    print("---------- 5.save centroids ------------")
    save_result("center_pp", centroids)
    draw(data, subCenter, centroids)

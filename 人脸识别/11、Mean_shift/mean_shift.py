# coding:UTF-8
import numpy as np
import math
import matplotlib.pyplot as plt

MIN_DISTANCE = 0.000001     # 最小误差


def gaussian_kernel(distance, bandwidth):
    """ 高斯核函数
    :param distance:(mat)欧式距离
    :param bandwidth: (int)核函数的带宽
    :return:
    """
    m = np.shape(distance)[0]    # 样本个数
    right = np.mat(np.zeros((m, 1)))    # mx1矩阵
    for i in range(m):
        right[i, 0] = (-0.5 * distance[i] * distance[i].T) / (bandwidth * bandwidth)
        right[i, 0] = np.exp(right[i, 0])
    left = 1 / (bandwidth * math.sqrt(2 * math.pi))
    gaussian_val = left * right
    return gaussian_val


def train_mean_shift(points, kernel_bandwidth=2):
    """ 训练Mean_shift模型
    :param points: 特征数据
    :param kernel_bandwidth:核函数的带宽
    :return:
    """
    mean_shift_points = np.mat(points)
    max_min_dist = 1
    iteration = 0     # 训练的迭代次数
    m = np.shape(mean_shift_points)[0]   # 样本个数
    need_shift = [True] * m
    while max_min_dist > MIN_DISTANCE:
        # 循环计算每个数据的最佳漂移值，直到满足条件。循环过程中若某个点不再需要漂移则跳过
        max_min_dist = 0
        iteration += 1
        print("\t iteration:{}".format(iteration))
        for i in range(0, m):
            # 判断每一个样本点是否需要计算偏移均值,循环计算每个数据对应的漂移点，知道每个数据的漂移点不需要再改动need_shift[i]=False
            if not need_shift[i]:
                continue
            p_new = mean_shift_points[i]
            p_new_start = p_new
            p_new = shift_point(p_new, points, kernel_bandwidth)    # 对样本点进行漂移,计算出每个样本点的mean_shift值
            dist = euclidean_dist(p_new, p_new_start)    # 计算原漂移点与漂移后的点之间的距离
            if dist > max_min_dist:
                max_min_dist = dist
            if dist < MIN_DISTANCE:    # 不需要改动，当该样本点满足条件时，不再参与循环计算。可以保证最终每个样本点都能满足条件
                need_shift[i] = False
            mean_shift_points[i] = p_new    # 给每个数据重新赋值其满足条件的漂移点
        print(max_min_dist)
    # 计算最终的group
    group = group_points(mean_shift_points)   # 计算所属的类别
    return np.mat(points), mean_shift_points, group


def shift_point(point, points, kernel_bandwidth):
    """ 计算均值漂移，Mean_shift向量的计算公式
    :param point: (mat)需要计算的点
    :param points: (array) 所有的样本点
    :param kernel_bandwidth: 核函数的带宽
    :return:
    """
    points = np.mat(points)
    m = np.shape(points)[0]    # 样本的个数
    # 计算距离
    point_distances = np.mat(np.zeros((m, 1)))
    for i in range(m):
        point_distances[i, 0] = euclidean_dist(point, points[i])

    # 计算高斯核
    point_weights = gaussian_kernel(point_distances, kernel_bandwidth)     # mx1的矩阵
    # 计算分母
    all_sum = 0.0
    for i in range(m):
        all_sum += point_weights[i, 0]
    # 均值偏移，计算的结果是Mean_shift向量的值
    point_shifted = point_weights.T * points / all_sum
    return point_shifted


def euclidean_dist(pointA, pointB):
    """ 计算欧式距离
    :param pointA: A点坐标
    :param pointB: B点坐标
    :return:
    """
    # 计算pointA和pointB之间的欧式距离
    total = (pointA - pointB) * (pointA - pointB).T
    return math.sqrt(total)


def group_points(mean_shift_points):
    """ 计算所属的类别
    :param mean_shift_points:漂移向量
    :return:
    """
    group_assignment = []
    m, n = np.shape(mean_shift_points)
    index = 0
    index_dict = {}
    for i in range(m):
        item = []
        for j in range(n):
            item.append(str(('%5.2f' % mean_shift_points[i, j])))
        item_1 = "_".join(item)
        if item_1 not in index_dict:
            index_dict[item_1] = index
            index += 1
    for key in index_dict.keys():
        print(key, index_dict[key])
    for i in range(m):
        item = []
        for j in range(n):
            item.append(str(('%5.2f' % mean_shift_points[i, j])))
        item_1 = "_".join(item)
        group_assignment.append(index_dict[item_1])
    return group_assignment


def load_data(path, feature_num=2):
    f = open(path)    # 打开文件
    data = []
    for line in f.readlines():
        lines = line.strip().split('\t')
        data_tmp = []
        if len(lines) != feature_num:        # 判断特征个数是否正确
            continue
        for i in range(feature_num):
            data_tmp.append(float(lines[i]))
        data.append(data_tmp)
    f.close()
    return data


def save_result(file_name, data):
    '''保存最终的计算结果
    input:  file_name(string):存储的文件名
            data(mat):需要保存的文件
    '''
    f = open(file_name, "w")
    m, n = np.shape(data)
    for i in range(m):
        tmp = []
        for j in range(n):
            tmp.append(str(data[i, j]))
        f.write("\t".join(tmp) + "\n")
    f.close()


def draw(data, sub, centroids):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    x2List = []
    y2List = []
    x4List = []
    y4List = []
    m = np.shape(data)[0]
    for i in range(m):
        if int(sub[i]) == 0:
            x0List.append(data[i][0])
            y0List.append(data[i][1])
        elif int(sub[i]) == 1:
            x1List.append(data[i][0])
            y1List.append(data[i][1])
        elif int(sub[i]) == 2:
            x2List.append(data[i][0])
            y2List.append(data[i][1])

    m = np.shape(centroids)[0]
    for i in range(m):
        if centroids[i, 0] not in x4List:
            x4List.append(centroids[i, 0])
        if centroids[i, 0] not in y4List:
            y4List.append(centroids[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='blue')
    ax.scatter(x2List, y2List, s=10, c='green')
    ax.scatter(x4List, y4List, s=10, c='black')
    plt.show()


if __name__ == '__main__':
    # 1、导入数据
    print("---------- 1.load data ------------")
    data = load_data("data", 2)
    # 2、随机初始化k个聚类中心
    print("---------- 2.training ------------")
    points, shift_points, cluster = train_mean_shift(data, 2)
    # 3、保存所属的类别文件
    print("---------- 3.save sub ------------")
    save_result("sub", np.mat(cluster))
    # 5、保存聚类中心
    print("---------- 4.save centroids ------------")
    save_result("center", shift_points)
    draw(data, cluster, shift_points)






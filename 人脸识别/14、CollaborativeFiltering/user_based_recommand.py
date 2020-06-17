# coding:utf-8
import numpy as np


def cos_sim(x, y):
    """ 余弦相似性
    :param x:以行向量的形式存储，可以是用户或者商品
    :param y:
    :return:
    """
    numerator = x * y.T
    denominator = np.sqrt(x * x.T) * np.sqrt(y * y.T)
    return (numerator / denominator)[0, 0]


def similarity(data):
    """ 计算矩阵中任意两行之间的相似度
    :param data:用户对商品的评价矩阵
    :return:
    """
    m = np.shape(data)[0]
    # 初始化相似度矩阵
    w = np.mat(np.zeros((m, m)))
    # 每个人进行对比0-m，i-m
    for i in range(m):
        for j in range(i, m):
            if j != i:
                # 计算任意两行之间的相似度
                w[i, j] = cos_sim(data[i, ], data[j, ])
                w[j, i] = w[i, j]
            else:
                w[i, j] = 0
    return w


def user_based_recommand(data, w, user):
    """ 基于用户相似性为用户user推荐商品
    :param data: 用户商品矩阵
    :param w: 用户之间的相似度
    :param user: 用户的编号
    :return:
    """
    m, n = np.shape(data)
    interaction = data[user, ]      # 用户user与商品信息

    # 1、找到用户user没有互动过的商品
    not_inter = []
    for i in range(n):
        if interaction[0, i] == 0:    # 没有互动的商品
            not_inter.append(i)
    # 2、对没有互动过的商品进行预测
    predict = {}
    for x in not_inter:
        item = np.copy(data[:, x])       # 找到所有用户对商品x的互动信息
        for i in range(m):            # 对每一个用户
            if item[i, 0] != 0:       # 若该用户对商品x有过互动
                if x not in predict:
                    predict[x] = w[user, i] * item[i, 0]
                else:
                    predict[x] = predict[x] + w[user, i] * item[i, 0]
    return sorted(predict.items(), key=lambda d: d[1], reverse=True)


def item_based_recommend(data, w, user):
    """ 基于商品相似度为用户user推荐商品
    :param data: 商品用户矩阵
    :param w: 商品与商品之间的相似性
    :param user: 用户的编号
    :return:
    """
    m, n = np.shape(data)     # m:商品数量，n:用户数量
    interaction = data[:, user].T    # 用户user的互动商品信息
    # 1、找到用户user没有互动的商品
    not_inter = []
    for i in range(n):
        if interaction[0, i] == 0:     # 用户user未打分项
            not_inter.append(i)
    # 2.对没有互动过的商品进行预测
    predict = {}
    for x in not_inter:
        item = np.copy(interaction)     # 获取用户user对商品的互动信息
        for j in range(m):              # 对每一个商品
            if item[0, j] != 0:         # 利用互动过的商品预测
                if x not in predict:
                    predict[x] = w[x, j] * item[0, j]
                else:
                    predict[x] = predict[x] + w[x, j] * item[0, j]
    # 按照预测的大小从大到小排序
    return sorted(predict.items(), key=lambda d: d[1], reverse=True)


def load_data(file_path):
    """ 导入用户商品数据
    :param file_path:
    :return:
    """
    f = open(file_path)
    data = []
    for line in f.readlines():
        lines = line.strip().split("\t")
        tmp = []
        for x in lines:
            if x != "-":
                tmp.append(float(x))    # 直接存储用户对商品的打分
            else:
                tmp.append(0)
        data.append(tmp)
    f.close()
    return np.mat(data)


def top_k(predict, k):
    """ 为用户推荐前k个商品
    :param predict: 排好序的商品列表
    :param k: 推荐的商品个数
    :return:
    """
    top_recom = []
    len_result = len(predict)
    if k >= len_result:
        top_recom = predict
    else:
        for i in range(k):
            top_recom.append(predict[i])
    return top_recom


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    testData = load_data("data.txt")
    # 2、计算用户之间相似性
    print("--------- 2.calculate similarity between users ------------")
    w = similarity(testData)
    # 3、利用用户之间的相似性进行推荐
    print("--------- 3.predict ------------")
    predict = user_based_recommand(testData, w, 0)
    # 4、进行top-K推荐
    top_recom = top_k(predict, 2)
    print(top_recom)

    # draw(testData, sub_class)
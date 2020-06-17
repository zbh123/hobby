# coding:utf-8
import numpy as np


def gradAscent(dataMat, k, alpha, beta, maxCycle):
    """ 利用梯度下降法对矩阵进行分解，最终目的是pxq=dataMax
    :param dataMat: 用户商品矩阵
    :param k: 分解矩阵的参数
    :param alpha: 学习率
    :param beta: 正则化参数
    :param maxCycle: 最大迭代次数
    :return:返回的p,q是根据dataMax的维度mxn来的，假设p为mxr，q为rxn所以p、q的维度即可确认
    """
    m, n = np.shape(dataMat)
    # 1、初始化p和q（确定p、q维度之后，随机分配p、q的值）
    p = np.mat(np.random.random((m, k)))
    q = np.mat(np.random.random((k, n)))
    # 2、开始训练
    # 循环迭代次数
    for step in range(maxCycle):
        for i in range(m):
            for j in range(n):
                if dataMat[i, j] > 0:
                    error = dataMat[i, j]
                    for r in range(k):
                        error = error - p[i, r] * q[r, j]
                    for r in range(k):
                        # 根据负梯度的方向更新变量
                        p[i, r] = p[i, r] + alpha * (2 * error * q[r, j] - beta * p[i, r])
                        q[r, j] = q[r, j] + alpha * (2 * error * p[i, r] - beta * q[r, j])
        loss = 0.0
        for i in range(m):
            for j in range(n):
                if dataMat[i, j] > 0:
                    error = 0.0
                    for r in range(k):
                        error = error + p[i, r] * q[r, j]
                    # 3.计算损失函数，真实值与预测值之间的差
                    loss = (dataMat[i, j] - error) * (dataMat[i, j] - error)
                    for r in range(k):
                        # 加入正则化之后的损失函数
                        loss = loss + beta * (p[i, r] * p[i, r] + q[r, j] * q[r, j]) / 2
        if loss < 0.001:
            break
        if step % 1000 == 0:
            print('\titer:{}, loss:{}'.format(step, loss))
    return p, q


def prediction(dataMatrix, p, q, user):
    """ 为用户user未互动项打分
    :param dataMatrix: 原始用户商品矩阵
    :param p: 分解后的p矩阵
    :param q: 分解后的q矩阵
    :param user: 用户的id
    :return:
    """
    n = np.shape(dataMatrix)[1]
    predict = {}
    for j in range(n):
        if dataMatrix[user, j] == 0:
            predict[j] = (p[user, ] * q[:, j])[0, 0]
    # 按照打分（value）从大到小排序
    return sorted(predict.items(), key=lambda d: d[1], reverse=True)


def load_data(path):
    f = open(path)
    data = []
    for line in f.readlines():
        arr = []
        lines = line.strip().split("\t")
        for x in lines:
            if x != '-':
                arr.append(float(x))
            else:
                arr.append(float(0))
        data.append(arr)
    f.close()
    return np.mat(data)


def save_file(file_name, source):
    f = open(file_name, 'w')
    m, n = np.shape(source)
    for i in range(m):
        tmp = []
        for j in range(n):
            tmp.append(str(source[i, j]))
        f.write('\t'.join(tmp) + '\n')
    f.close()


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
    # 1、导入用户商品数据
    print("------------ 1. load data ------------")
    data = load_data("data.txt")
    # 2、计算商品之间的相似性
    print("------------ 2. training -------------")
    p, q = gradAscent(data, 5, 0.0002, 0.02, 5000)
    # 3、保存分解后的结果
    print("------------ 3. save decompose ------------")
    save_file('p', p)
    save_file('q', q)
    # 4.预测
    print('--------4. prediction ----------')
    predict = prediction(data, p, q, 0)
    # 5.进行top-K推荐
    print("------------ 5. top_k recommendation ------------")
    top_recom = top_k(predict, 2)
    print(top_recom)
    print(p*q)





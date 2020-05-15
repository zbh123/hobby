# coding:UTF-8
import numpy as np


def sig(x):
    '''
    Sigmod函数
    :param x:(mat) feature * w
    :return: sigmoid(x)(mat):Sigmoid值
    '''
    return 1.0 / (1 + np.exp(-x))


def error_rate(h, label):
    '''
    计算损失函数值
    :param h: (mat)预测值
    :param label: (mat)实际值
    :return: err/m(float)
    '''
    m = np.shape(h)[0]
    sum_err = 0.0
    for i in range(m):
        if h[i, 0] > 0 and (1 - h[i, 0]) > 0:
            sum_err -= (label[i, 0] * np.log(h[i, 0]) + (1 - label[i, 0]) * np.log(1 - h[i, 0]))
        else:
            sum_err -= 0
    return sum_err


def lr_train_bgd(feature, label, maxCycle, alpha):
    '''
    梯度下降法训练LR模型
    :param feature: (mat)特征
    :param label:(mat)标签
    :param maxCycle:(int)最大迭代次数
    :param alpha:(float)学习率
    :return:w(mat)权重
    '''
    n = np.shape(feature)[1]
    print(n)
    # print(n, np.shape(feature)[0])
    w = np.mat(np.ones((n, 1)))
    # print(w)
    i = 0
    while i <= maxCycle:
        i += 1
        h = sig(feature * w)
        # print(feature * w)
        # print(h)
        err = label - h
        if i % 100 == 0:
            print('\t----iter=%d, train error rate=%s----' % (i, str(error_rate(h, label))))
        # 进行误差补偿
        w += alpha * feature.T * err
    return w


def load_data(file_name):
    '''
    :param file_name:
    :return:
    '''
    f = open(file_name, 'r')
    feature_data = []
    label_data = []
    for line in f.readlines():
        feature_tmp = []
        label_tmp = []
        lines = line.strip().split(' ')
        # 假设偏置项为1的前提下，才能实现sigmoid的条件--|
        feature_tmp.append(1)
        for i in range(len(lines) - 1):
            feature_tmp.append(float(lines[i]))
        label_tmp.append(float(lines[-1]))
        feature_data.append(feature_tmp)
        label_data.append(label_tmp)
    f.close()
    return np.mat(feature_data), np.mat(label_data)


def save_model(file_name, w):
    '''
    :param file_name:
    :param w:
    :return:
    '''
    m = np.shape(w)[0]
    f_w = open(file_name, 'w')
    w_array = []
    for i in range(m):
        w_array.append(str(w[i, 0]))
    f_w.write('\t'.join(w_array))
    f_w.close()


if __name__ == '__main__':
    # 1.导入训练数据
    print('------1. load data-----')
    feature, label = load_data('data.txt')
    # print(feature)
    # 2. 训练LR模型
    print('-----2. training-----')
    w = lr_train_bgd(feature, label, 1000, 0.05)
    # 3.保存最终的模型
    print('----3.save model----')
    save_model('weights', w)

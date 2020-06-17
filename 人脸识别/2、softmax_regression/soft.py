import numpy as np
import random as rd
import matplotlib.pyplot as plt


def load_weight(w):
    '''导入LR模型
    :param w:(string) 权重所在文件位置
    :return: np.mat(w)(mat)权重的矩阵
    '''
    f = open(w)
    w = []
    for line in f.readlines():
        lines = line.strip().split('\t')
        w_tmp = []
        for x in lines:
            w_tmp.append(float(x))
        w.append(w_tmp)
    f.close()
    weights = np.mat(w)
    m, n = np.shape(weights)
    return weights, m, n


def load_data(num, m):
    '''
    导入测试数据
    :param num:(int) 样本个数
    :param n: (int)样本维度
    :return: np.mat(feature_data)(mat)测试集的特征
    '''
    testDataSet = np.mat(np.ones((num, m)))
    for i in range(num):
        testDataSet[i, 1] = rd.random() * 6 - 3
        testDataSet[i, 2] = rd.random() * 15
    # print(testDataSet)
    return testDataSet


def predict(data, w):
    '''
    对测试数据进行预测
    :param data: (mat)测试数据的特征
    :param w: (mat)模型的参数
    :return: h(mat)最终的预测结果
    '''
    h = data * w
    # print(h, h.argmax(axis=1))
    # argmax取axis所在行或列最大值的索引
    return h.argmax(axis=1)


def save_result(file_name, result):
    '''
    保存最终的预测结果
    :param file_name:(string)
    :param result: (mat):预测结果
    :return:
    '''
    f_result = open(file_name, 'w')
    m = np.shape(result)[0]
    for i in range(m):
        f_result.write(str(result[i, 0]))
        f_result.write('\n')
    f_result.close()


def draw(test_data, result):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    x2List = []
    y2List = []
    x3List = []
    y3List = []
    for i in range(len(result)):
        if result[i, 0] == 0:
            x0List.append(float(test_data[i, 1]))
            y0List.append(float(test_data[i, 2]))
        elif result[i, 0] == 1:
            x1List.append(float(test_data[i, 1]))
            y1List.append(float(test_data[i, 2]))
        elif result[i, 0] == 2:
            x2List.append(float(test_data[i, 1]))
            y2List.append(float(test_data[i, 2]))
        else:
            x3List.append(float(test_data[i, 1]))
            y3List.append(float(test_data[i, 2]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='green')
    ax.scatter(x2List, y2List, s=10, c='blue')
    ax.scatter(x3List, y3List, s=10, c='yellow')
    plt.show()


if __name__ == '__main__':
    # -----1、导入Softmax模型----
    print('--------1、load model ------')
    w, m, n = load_weight('weights')
    # ----2、导入测试数据----
    print('-----1. load data -------')
    testData = load_data(4000, m)
    # ---3、对测试数据进行预测
    print('------3、get prediction -----')
    h = predict(testData, w)
    print(h)
    # ----4、保存预测结果----
    print('-----4、Save prediction------')
    save_result('result', h)
    draw(testData, h)
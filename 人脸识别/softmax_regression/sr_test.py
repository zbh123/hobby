import numpy as np
import matplotlib.pyplot as plt


def gradientAscent(feature_data, label_data, k, maxCycle, alpha):
    ''' 梯度下降法训练Softmax模型
    :param feature_data: (mat)特征
    :param label_data: (mat)标签
    :param k: (int)类别的个数
    :param maxCycle: (int)最大的迭代次数
    :param alpha: (float)学习率
    :return: weights(mat)权重
    '''
    m, n = np.shape(feature_data)
    weights = np.mat(np.ones((n, k)))
    # print(weights)
    i = 0
    while i <= maxCycle:
        err = np.exp(feature_data * weights)
        # print(err, np.shape(err))
        if i % 1000 == 0:
            print('\t----iter:%d,---cost:%f-----' % (i, cost(err, label_data)))
        # 去掉axis所在轴的维度，将这个轴上的数据相加到剩下的维度上
        rowsum = -err.sum(axis=1)
        # print(rowsum)
        # repeat沿着纵轴重复增加k列
        rowsum = rowsum.repeat(k, axis=1)
        # 求取每个维度上的err值的占比，分别进行更新
        err = err / rowsum
        for x in range(m):
            # 加强分类，例如：实际值是1，那么对应位置的权重就+1，以此增加权重的比例
            err[x, label_data[x, 0]] += 1
        weights = weights + (alpha/m)*feature_data.T*err
        i += 1
    return weights


def cost(err, label_data):
    '''
    计算损失函数
    :param err:(mat)exp的值
    :param label_data: (mat)标签的值
    :return: 损失函数的值
    '''
    m = np.shape(err)[0]
    sum_cost = 0
    for i in range(m):
        if err[i, label_data[i, 0]] / np.sum(err[i, :]) > 0:
            sum_cost -= np.log(err[i, label_data[i, 0]] / np.sum(err[i, :]))
        else:
            sum_cost -= 0
    return sum_cost/m


def load_data(inputfile):
    f = open(inputfile, 'r')
    feature_data = []
    label_data = []
    for line in f.readlines():
        feature_tmp = []
        feature_tmp.append(1)
        lines = line.strip().split()
        for i in range(len(lines) - 1):
            feature_tmp.append(float(lines[i]))
        label_data.append(int(lines[-1]))
        feature_data.append(feature_tmp)
    f.close()
    return np.mat(feature_data), np.mat(label_data).T, len(set(label_data))


def save_model(file_name, weights):
    f_w = open(file_name, 'w')
    m, n = np.shape(weights)
    for i in range(m):
        w_tmp = []
        for j in range(n):
            w_tmp.append(str(weights[i, j]))
        f_w.write('\t'.join(w_tmp))
        f_w.write('\n')
    f_w.close()


def draw(weight, file_name):
    x0List=[];y0List=[]
    x1List=[];y1List=[]
    x2List=[];y2List=[]
    x3List=[];y3List=[]
    f=open(file_name,'r')
    for line in f.readlines():
        lines=line.strip().split()
        if lines[2]=='0':
            x0List.append(float(lines[0]))
            y0List.append(float(lines[1]))
        elif lines[2]=='1':
            x1List.append(float(lines[0]))
            y1List.append(float(lines[1]))
        elif lines[2]=='2':
            x2List.append(float(lines[0]))
            y2List.append(float(lines[1]))
        else:
            x3List.append(float(lines[0]))
            y3List.append(float(lines[1]))
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(x0List,y0List,s=10,c='red')
    ax.scatter(x1List,y1List,s=10,c='green')
    ax.scatter(x2List,y2List,s=10,c='blue')
    ax.scatter(x3List,y3List,s=10,c='yellow')
    plt.show()


if __name__ == '__main__':
    # 1.导入训练数据
    print('------1. load data-----')
    # feature是基础数据，label是特征，k是特征值数量
    feature, label, k = load_data('softInput.txt')
    # print(feature)
    # 2. 训练LR模型
    print('-----2. training-----')
    w = gradientAscent(feature, label, k, 10000, 0.4)
    # 3.保存最终的模型
    print('----3.save model----')
    save_model('weights', w)
    # 4，绘制图像
    draw(w, 'softInput.txt')

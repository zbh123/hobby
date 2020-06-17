import numpy as np
from math import sqrt
import matplotlib.pyplot as plt


def bp_train(feature, label, n_hidden, maxCycle, alpha, n_output):
    ''' 计算隐含层的输入
    :param feature: 特征
    :param label: 标签
    :param n_hidden: 隐含层的节点个数，输入层节点个数为400，自定义隐含层节点个数
    :param maxCycle: 最大迭代次数
    :param alpha: 学习率
    :param n_output: 输出层的节点个数
    :return: w0：输入层到隐含层之间的权重
            b0：输入层到隐含层之间的偏置
            w1：输入层到隐含层之间的权重
            b1：输入层到隐含层之间的偏置
    '''
    m, n = np.shape(feature)
    # 1、初始化
    w0 = np.mat(np.random.rand(n, n_hidden))
    w0 = w0 * (8.0 * sqrt(6) / sqrt(n + n_hidden)) - np.mat(np.ones((n, n_hidden))) * (4.0 * sqrt(6) / sqrt(n + n_hidden))
    b0 = np.mat(np.random.rand(1, n_hidden))
    b0 = b0 * (8.0 * sqrt(6) / sqrt(n + n_hidden)) - np.mat(np.ones((1, n_hidden))) * (4.0 * sqrt(6) / sqrt(n + n_hidden))
    w1 = np.mat(np.random.rand(n_hidden, n_output))
    w1 = w1 * (8.0 * sqrt(6) / sqrt(n_hidden + n_output)) - np.mat(np.ones((n_hidden, n_output))) * (4.0 * sqrt(6) / sqrt(n_hidden + n_output))
    b1 = np.mat(np.random.rand(1, n_output))
    b1 = b1 * (8.0 * sqrt(6) / sqrt(n_hidden + n_output)) - np.mat(np.ones((1, n_output))) * (4.0 * sqrt(6) / sqrt(n_hidden + n_output))

    # 2、训练
    i = 0
    while i <= maxCycle:
        # 2.1、信号正向传播
        # 2.1.1、计算隐含层的输入
        hidden_input = hidden_in(feature, w0, b0)  # mXn_hidden
        # 2.1.2、计算隐含层的输出
        hidden_output = hidden_out(hidden_input)
        # 2.1.3、计算输出层的输入
        output_in = predict_in(hidden_output, w1, b1)  # mXn_output
        # 2.1.4、计算输出层的输出
        output_out = predict_out(output_in)

        # 2.2、误差的反向传播
        # 2.2.1、隐含层到输出层之间的残差
        delta_output = -np.multiply((label - output_out), partial_sig(output_in))
        # 2.2.2、输入层到隐含层之间的残差
        delta_hidden = np.multiply((delta_output * w1.T), partial_sig(hidden_input))

        # 2.3、 修正权重和偏置
        w1 = w1 - alpha * (hidden_output.T * delta_output)
        b1 = b1 - alpha * np.sum(delta_output, axis=0) * (1.0 / m)
        w0 = w0 - alpha * (feature.T * delta_hidden)
        b0 = b0 - alpha * np.sum(delta_hidden, axis=0) * (1.0 / m)
        if i % 100 == 0:
            print("\t-------- iter:{} ,cost: {}".format(i, (1.0 / 2) * get_cost(get_predict(feature, w0, w1, b0, b1) - label)))
        i += 1
    return w0, w1, b0, b1


def hidden_in(feature, w0, b0):
    ''' 计算隐含层输入
    :param feature:
    :param w0:
    :param b0:
    :return:
    '''
    m = np.shape(feature)[0]
    hidden_in = feature * w0
    for i in range(m):
        hidden_in[i, ] += b0
    return hidden_in


def hidden_out(hidden_in):
    ''' 隐含层的输出
    :param hidden_in:
    :return:
    '''
    hidden_out = sig(hidden_in)
    return hidden_out


def sig(x):
    ''' sigmoid函数
    :param x:
    :return:
    '''
    return 1.0 / (1 + np.exp(-x))


def partial_sig(x):
    ''' sigmoid倒数的值
    :param x:
    :return:
    '''
    m, n = np.shape(x)
    out = np.mat(np.zeros((m, n)))
    for i in range(m):
        for j in range(n):
            out[i, j] = sig(x[i, j]) * (1 - sig(x[i, j]))
    return out


def predict_in(hidden_out, w1, b1):
    ''' 计算输出层的输入
    :param hidden_out:
    :param w1:
    :param b1:
    :return:
    '''
    m = np.shape(hidden_out)[0]
    predict_in = hidden_out * w1
    for i in range(m):
        predict_in[i, ] += b1
    return predict_in


def predict_out(predict_in):
    ''' 计算输出层的输出
    :param predict_in:
    :return:
    '''
    result = sig(predict_in)
    return result


def get_cost(cost):
    ''' 计算当前损失函数的值
    :param cost:
    :return:
    '''
    m, n = np.shape(cost)
    cost_sum = 0.0
    for i in range(m):
        for j in range(n):
            cost_sum += cost[i, j] * cost[i, j]
    return cost_sum / m


def err_rate(label, pre):
    '''计算训练样本上的错误率
    input:  label(mat):训练样本的标签
            pre(mat):训练样本的预测值
    output: rate[0,0](float):错误率
    '''
    m = np.shape(label)[0]
    err = 0.0
    for i in range(m):
        if label[i, 0] != pre[i, 0]:
            err += 1
    rate = err / m
    return rate


def save_model(w0, w1, b0, b1):
    '''保存最终的模型
    input:  w0(mat):输入层到隐含层之间的权重
            b0(mat):输入层到隐含层之间的偏置
            w1(mat):隐含层到输出层之间的权重
            b1(mat):隐含层到输出层之间的偏置
    output:
    '''

    def write_file(file_name, source):
        f = open(file_name, "w")
        m, n = np.shape(source)
        for i in range(m):
            tmp = []
            for j in range(n):
                tmp.append(str(source[i, j]))
            f.write("\t".join(tmp) + "\n")
        f.close()

    write_file("weight_w0", w0)
    write_file("weight_w1", w1)
    write_file("weight_b0", b0)
    write_file("weight_b1", b1)


def load_data(file_name):
    '''导入数据
    input:  file_name(string):文件的存储位置
    output: feature_data(mat):特征
            label_data(mat):标签
            n_class(int):类别的个数
    '''
    # 1、获取特征
    f = open(file_name)  # 打开文件
    feature_data = []
    label_tmp = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split("\t")
        for i in range(len(lines) - 1):
            feature_tmp.append(float(lines[i]))
        label_tmp.append(int(lines[-1]))
        feature_data.append(feature_tmp)
    f.close()  # 关闭文件

    # 2、获取标签
    m = len(label_tmp)
    n_class = len(set(label_tmp))  # 得到类别的个数

    label_data = np.mat(np.zeros((m, n_class)))
    for i in range(m):
        label_data[i, label_tmp[i]] = 1

    return np.mat(feature_data), label_data, n_class


def get_predict(feature, w0, w1, b0, b1):
    '''计算最终的预测
    input:  feature(mat):特征
            w0(mat):输入层到隐含层之间的权重
            b0(mat):输入层到隐含层之间的偏置
            w1(mat):隐含层到输出层之间的权重
            b1(mat):隐含层到输出层之间的偏置
    output: 预测值
    '''
    # 首先计算隐含层的输入hidden_in：w*feature + b，再计算隐含层输出hidden_out：sigmoid(input)
    # 再计算输出层输入predict_in：w*feature + b，predict_out：sigmoid(input)
    return predict_out(predict_in(hidden_out(hidden_in(feature, w0, b0)), w1, b1))


def draw(file_name):
    x0List = []
    y0List = []
    x1List = []
    y1List = []

    f = open(file_name, 'r')
    for line in f.readlines():
        lines = line.strip().split()
        if float(lines[2]) > 0:
            x0List.append(float(lines[0]))
            y0List.append(float(lines[1]))
        else:
            x1List.append(float(lines[0]))
            y1List.append(float(lines[1]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='green')
    # plt.plot(x0List, y0List, c='red')
    # plt.plot(x1List, y1List, c='green')
    plt.show()


if __name__ == "__main__":
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    feature, label, n_class = load_data("data.txt")
    # 2、训练网络模型
    print("--------- 2.training ------------")
    w0, w1, b0, b1 = bp_train(feature, label, 20, 1000, 0.1, n_class)
    # 3、保存最终的模型
    print("--------- 3.save model ------------")
    save_model(w0, w1, b0, b1)
    # 4、得到最终的预测结果
    print("--------- 4.get prediction ------------")
    result = get_predict(feature, w0, w1, b0, b1)
    print("训练准确性为：", (1 - err_rate(np.argmax(label, axis=1), np.argmax(result, axis=1))))
    draw("data.txt")

# coding:UTF-8

import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    '''导入测试数据
    input:  file_path(string):训练数据
    output: feature(mat):特征
    '''
    f = open(file_path)
    feature = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split("\t")
        feature_tmp.append(1)  # x0
        for i in range(len(lines)):
            feature_tmp.append(float(lines[i]))
        feature.append(feature_tmp)
    f.close()
    return np.mat(feature)


def load_model(model_file):
    '''导入模型
    input:  model_file(string):线性回归模型
    output: w(mat):权重值
    '''
    w = []
    f = open(model_file)
    for line in f.readlines():
        w.append(float(line.strip()))
    f.close()
    return np.mat(w).T


def get_prediction(data, w):
    '''对新数据进行预测
    input:  data(mat):测试数据
            w(mat):权重值
    output: 最终的预测
    '''
    return data * w


def save_result(file_name, predict):
    '''保存最终的结果
    input:  file_name(string):需要保存的文件
            predict(mat):预测结果
    '''
    m = np.shape(predict)[0]
    result = []
    for i in range(m):
        result.append(str(predict[i, 0]))
    f = open(file_name, "w")
    f.write("\n".join(result))
    f.close()


def draw(data, predict):
    x0List = []
    y0List = []
    m = np.shape(data)[0]
    for i in range(m):
        x0List.append(data[i, 1])
        y0List.append(predict[i, 0])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    plt.show()


if __name__ == "__main__":
    # 1、导入测试数据
    print("----------1.load data ------------")
    testData = load_data("data_test.txt")
    # 2、导入线性回归模型
    print("----------2.load model ------------")
    w = load_model("weights")
    # 3、得到预测结果
    print("----------3.get prediction ------------")
    predict = get_prediction(testData, w)
    # 4、保存最终的结果
    print("----------4.save prediction ------------")
    save_result("predict_result", predict)
    draw(testData, predict)
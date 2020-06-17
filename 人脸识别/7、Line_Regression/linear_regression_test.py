# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    f = open(file_path)
    feature = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split('\t')
        feature_tmp.append(1)   # x0
        for i in range(len(lines)):
            feature_tmp.append(float(lines[i]))
        feature.append(feature_tmp)
    # print(feature)
    f.close()
    return np.mat(feature)


def load_model(model_file):
    w = []
    f = open(model_file)
    for line in f.readlines():
        w.append(float(line.strip()))
    f.close()
    return np.mat(w).T


def get_prediction(data, w):
    return data * w


def save_predict(file_name, predict):
    m = np.shape(predict)[0]
    result = []
    for i in range(m):
        result.append(str(predict[i, 0]))
    f = open(file_name, 'w')
    f.write('\n'.join(result))
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


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    testData = load_data("data_test.txt")
    # 2、导入线性回归模型
    print("--------- 2.load weight ------------")
    w = load_model('weights')
    # 3、得到预测结果
    print("--------- 3.predict ------------")
    predict = get_prediction(testData, w)
    # 4、保存结果
    print("--------- 4.save result ------------")
    save_predict('predict_result', predict)

    draw(testData, predict)


import numpy as np
import pickle
import matplotlib.pyplot as plt
import random as rd
from cart_train import predict, node


def load_data():
    data_set = []
    for i in range(400):
        tmp = []
        tmp.append(rd.random())
        data_set.append(tmp)
    return data_set


def load_model(tree_file):
    with open(tree_file, 'rb') as f:
        trees_result = pickle.load(f)

    return trees_result


def get_prediction(data_test, regression_tree):
    '''对测试样本进行预测
    input:  data_test(list):需要预测的样本
            regression_tree(regression_tree):训练好的回归树模型
    output: result(list):
    '''
    result = []
    for x in data_test:
        result.append(predict(x, regression_tree))
    return result


def save_result(data_test, result, prediction_file):
    '''保存最终的预测结果
    input:  data_test(list):需要预测的数据集
            result(list):预测的结果
            prediction_file(string):保存结果的文件
    '''
    f = open(prediction_file, "w")
    for i in range(len(result)):
        a = str(data_test[i][0]) + "\t" + str(result[i]) + "\n"
        f.write(a)
    f.close()


def draw(file_name):
    x0List = []
    y0List = []

    f = open(file_name, 'r')
    for line in f.readlines():
        lines = line.strip().split()
        x0List.append(float(lines[0]))
        y0List.append(float(lines[1]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    plt.show()


if __name__ == '__main__':
    # 1.导入训练数据
    print('------1. load data-----')
    data_test = load_data()
    # print(feature)
    # 2.训练随机森林模型
    print('-----2. random forest training-----')
    trees_result = load_model("regression_tree")
    # 3.保存最终的模型
    print('----3.get prediction correct rate----')
    prediction = get_prediction(data_test, trees_result)

    # 4.保存模型
    print('-----4. save model------')
    save_result(data_test, prediction, 'prediction')
    draw('prediction')

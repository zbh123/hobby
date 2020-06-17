# coding:UTF-8
import pickle
from random_forest_train import get_predict
import matplotlib.pyplot as plt


def load_data(file_name):
    f = open(file_name)
    test_data = []
    for line in f.readlines():
        lines = line.strip().split('\t')
        tmp = []
        for x in lines:
            tmp.append(float(x))
        tmp.append(0)
        test_data.append(tmp)
    f.close()
    return test_data


def load_model(result_file, feature_file):
    trees_feature = []
    f_fea = open(feature_file)
    for line in f_fea.readlines():
        lines = line.strip().split('\t')
        tmp = []
        for x in lines:
            tmp.append(int(x))
        trees_feature.append(tmp)
    f_fea.close()

    with open(result_file, 'rb') as f:
        trees_result = pickle.load(f)

    return trees_result, trees_feature


def save_result(data_test, prediction, result_file):
    m = len(prediction)
    n = len(data_test[0])
    f_result = open(result_file, 'w')
    for i in range(m):
        tmp = []
        for j in range(n-1):
            tmp.append(str(data_test[i][j]))
        tmp.append(str(prediction[i]))
        f_result.writelines('\t'.join(tmp))
        f_result.write('\n')
    f_result.close()


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
    plt.show()


if __name__ == '__main__':
    # 1.导入训练数据
    print('------1. load data-----')
    data_test = load_data('test_data.txt')
    # print(feature)
    # 2.训练随机森林模型
    print('-----2. random forest training-----')
    trees_result, trees_feature = load_model("result_file", "feature_file")
    # 3.保存最终的模型
    print('----3.get prediction correct rate----')
    prediction = get_predict(trees_result, trees_feature, data_test)

    # 4.保存模型
    print('-----4. save model------')
    save_result(data_test, prediction, 'final_result')
    draw('final_result')

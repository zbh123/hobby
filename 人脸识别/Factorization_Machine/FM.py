# coding:UTF-8

import numpy as np
from matplotlib.pylab import plt
from fm_test import getPrediction


def loadDataSet(data):
    '''导入测试数据集
    input:  data(string)测试数据
    output: dataMat(list)特征
    '''
    dataMat = []
    fr = open(data)  # 打开文件
    for line in fr.readlines():
        lines = line.strip().split("\t")
        lineArr = []

        for i in range(len(lines)-1):
            lineArr.append(float(lines[i]))
        dataMat.append(lineArr)

    fr.close()
    return dataMat


def loadModel(model_file):
    '''导入FM模型
    input:  model_file(string)FM模型
    output: w0, np.mat(w).T, np.mat(v)FM模型的参数
    '''
    f = open(model_file)
    line_index = 0
    w0 = 0.0
    w = []
    v = []
    for line in f.readlines():
        lines = line.strip().split("\t")
        if line_index == 0:  # w0
            w0 = float(lines[0].strip())
        elif line_index == 1:  # w
            for x in lines:
                w.append(float(x.strip()))
        else:
            v_tmp = []
            for x in lines:
                v_tmp.append(float(x.strip()))
            v.append(v_tmp)
        line_index += 1
    f.close()
    return w0, np.mat(w).T, np.mat(v)


def save_result(file_name, result):
    '''保存最终的预测结果
    input:  file_name(string)需要保存的文件名
            result(mat):对测试数据的预测结果
    '''
    f = open(file_name, "w")
    f.write("\n".join(str(1) if x >= 0.5 else str(0) for x in result))
    f.close()

def draw(test_data, result):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    for i in range(len(result)):
        if result[i] == 0:
            x0List.append(float(test_data[i][0]))
            y0List.append(float(test_data[i][1]))
        else:
            x1List.append(float(test_data[i][0]))
            y1List.append(float(test_data[i][1]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='green')
    plt.show()

if __name__ == "__main__":
    # 1、导入测试数据
    dataTest = loadDataSet("test_data.txt")
    # print(dataTest)
    # 2、导入FM模型
    w0, w, v = loadModel("weights")
    # print(w0, w, v)
    # 3、预测
    result = getPrediction(dataTest, w0, w, v)
    # print(result)
    # 4、保存最终的预测结果
    save_result("predict_result", result)
    # result_new = []
    result_new = [1 if x >= 0.5 else 0 for x in result]
    # for x in result:
    #     if x >= 0.5:
    #         result_new.append(1)
    #     else:
    #         result_new.append(0)

    print(len(result_new))
    draw(dataTest, result_new)

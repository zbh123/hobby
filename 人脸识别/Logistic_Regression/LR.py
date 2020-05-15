import numpy as np


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
    return np.mat(w)


def load_data(file_name, n):
    '''
    导入测试数据
    :param file_name:(string) 测试集的位置
    :param n: (int)特征的个数
    :return: np.mat(feature_data)(mat)测试集的特征
    '''
    f = open(file_name)
    feature_data = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split('\t')
        if len(lines) != n-1:
            continue
        feature_tmp.append(1)
        for x in lines:
            feature_tmp.append(float(x))
        feature_data.append(feature_tmp)
    f.close()
    return np.mat(feature_data)




if __name__ == '__main__':
    # -----1、导入LR模型----
    print('--------1、load model ------')
    w = load_weight('weights')
    n = np.shape(w)[1]
    # ----2、导入测试数据----
    print('-----1. load data -------')
    testData = load_data('test_data', w)
    # ---3、对测试数据进行预测
    print('------3、get prediction -----')
    h = predict(testData, w)
    # ----4、保存预测结果----
    print('-----4、Save prediction------')
    save_result('result', h)

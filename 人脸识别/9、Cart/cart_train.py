import numpy as np
import pickle
import matplotlib.pyplot as plt


def err_cnt(dataSet):
    """ 回归树的划分指标
    :param dataSet:list 训练数据
    :return:
    """
    data = np.mat(dataSet)
    return np.var(data[:, -1]) * np.shape(data)[0]


def split_tree(data, fea, value):
    """ 根据特征fea中的值value将数据集data划分为左右子树
    :param data: 训练样本
    :param fea: 需要划分的特征
    :param value: 指定的划分的值
    :return:
    """
    set_1 = []  # 左子树的集合
    set_2 = []  # 右子树的集合
    for x in data:
        if x[fea] >= value:
            set_1.append(x)
        else:
            set_2.append(x)
    return (set_1, set_2)


class node:
    """
    树节点的类
    """

    def __init__(self, fea=-1, value=None, results=None, right=None, left=None):
        self.fea = fea  # 用于切分数据集的属性的列索引值
        self.value = value  # 设置划分的值
        self.results = results  # 存储叶节点的值
        self.left = left  # 左子树
        self.right = right  # 右子树


def build_tree(data, min_sample, min_err):
    """ 构建树
    :param data: 训练样本list
    :param min_sample: 叶子节点中最少的样本数 int
    :param min_err: 最小的误差 float
    :return:
    """
    # 构建决策树，函数返回该决策树的根节点
    if len(data) <= min_sample:
        return node(results=leaf(data))
    # 1.初始化
    best_err = err_cnt(data)
    bestCriteria = None  # 存储最佳切分属性以及最佳切分点
    bestSets = None  # 存储切分后的两个数据集

    # 2.开始构建CART回归树
    feature_num = len(data[0]) - 1
    for fea in range(feature_num):
        feature_value = {}
        for sample in data:
            feature_value[sample[fea]] = 1
        for value in feature_value.keys():
            # 2.1 尝试划分
            (set_1, set_2) = split_tree(data, fea, value)
            if len(set_1) < 2 or len(set_2) < 2:
                continue
            # 2.2 计算划分后的error值
            now_err = err_cnt(set_1) + err_cnt(set_2)
            # 2.3 更新最优划分
            if now_err < best_err and len(set_1) > 0 and len(set_2) > 0:
                best_err = now_err
                bestCriteria = (fea, value)
                bestSets = (set_1, set_2)
    # 3.判断划分是否结束
    if best_err > min_err:
        right = build_tree(bestSets[0], min_sample, min_err)
        left = build_tree(bestSets[1], min_sample, min_err)
        return node(fea=bestCriteria[0], value=bestCriteria[1], right=right, left=left)
    else:
        return node(results=leaf(data))  # 返回当前的类别标签作为最终的类别标签


def leaf(dataSet):
    """ 计算叶节点的值
    :param dataSet:
    :return:
    """
    data = np.mat(dataSet)
    return np.mean(data[:, -1])


def load_data(file_path):
    f = open(file_path)
    feature = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split('\t')
        for x in lines:
            feature_tmp.append(float(x))
        feature.append(feature_tmp)
    f.close()
    return feature


def cal_error(data, tree):
    """ 评估CART回归树模型
    :param data: 训练数据集
    :param tree: 训练好的回归树
    :return:
    """
    m = len(data)
    n = len(data[0])
    err = 0.0
    for i in range(m):
        tmp = []
        for j in range(n):
            tmp.append(data[i][j])
        pre = predict(tmp, tree)  # 对样本计算其预测值
        # 计算残差
        err += (data[i][-1] - pre) * (data[i][-1] - pre)
    return err / m


def save_model(regression_tree, result_file):
    with open(result_file, 'wb') as f:
        pickle.dump(regression_tree, f)


def predict(sample, tree):
    """ 对每一个样本sample进行预测
    :param sample: list 样本
    :param tree: 训练好的回归树模型
    :return:
    """
    # 1、只是树根
    if tree.results != None:
        return tree.results
    else:
        # 2.有左由子树
        val_sample = sample[tree.fea]  # fea处的值
        branch = None
        # 2.1 选择右子树
        if val_sample >= tree.value:
            branch = tree.right
        # 2.2 选择左子树
        else:
            branch = tree.left
        return predict(sample, branch)


def draw(file_name, tree):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    m = len(data)
    n = len(data[0])
    for i in range(m):
        tmp = []
        for j in range(n):
            tmp.append(data[i][j])
        pre = predict(tmp, tree)  # 对样本计算其预测值
        y1List.append(pre)
    f = open(file_name, 'r')
    for line in f.readlines():
        lines = line.strip().split()
        x0List.append(float(lines[0]))
        y0List.append(float(lines[1]))
    data_dict = {}
    for i in range(len(y1List)):
        data_dict[x0List[i]] = [y0List[i], y1List[i]]
    data_list = sorted(data_dict.items(), key=lambda item: item[0])
    x0List = []
    y0List = []
    y1List = []
    for i in range(len(data_list)):
        x0List.append(data_list[i][0])
        y0List.append(data_list[i][1][0])
        y1List.append(data_list[i][1][1])
    for i in range(len(y1List)):
        print(x0List[i])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.plot(x0List, y1List, c='green')
    plt.show()


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    data = load_data("sine.txt")
    # 2、最下二乘求解
    print("--------- 2.training ------------")
    regression_tree = build_tree(data, 5, 0.1)
    # 3、评估CART树
    print("--------- 3.cal error ------------")
    err = cal_error(data, regression_tree)
    print('\t---correct rate:{}----'.format(err))
    # 4.保存模型
    print('-----4. save model------')
    save_model(regression_tree, 'regression_tree')
    draw('sine.txt', regression_tree)

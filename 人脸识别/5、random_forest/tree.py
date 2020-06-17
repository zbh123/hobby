# coding=utf-8
from math import pow


class Node:
    ''' 树的节点的类
    '''

    def __init__(self, fea=-1, value=None, results=None, right=None, left=None):
        self.fea = fea  # 用于切分数据集的属性的列索引值
        self.value = value  # 设置划分的值
        self.results = results  # 存储叶节点所属的类别
        self.right = right  # 右子树
        self.left = left  # 左子树


def build_tree(data):
    ''' 构建树
    :param data:(list)训练样本
    :return:  node树的根节点
    '''
    # 构建决策树，函数返回该树的根节点
    if len(data) == 0:
        return Node()
    # 1.计算当前Gini值
    currentGini = cal_gini_index(data)
    bestGain = 0.0
    bestCriteria = None  # 存储最佳切分属性以及最佳切分点
    bestSets = None  # 存储切分后的两个数据集
    feature_num = len(data[0]) - 1  # 样本中特征的个数
    # 2.找到最好的划分
    for fea in range(0, feature_num):
        # 2.1取得fea特征处所有可能的取值
        feature_value = {}  # 在fea位置处可能的取值
        for sample in data:
            feature_value[sample[fea]] = 1  # 存储特征fea处所有可能的取值
        # 2.2 针对每一个可能的取值，尝试将数据集划分，并计算Gini指数
        for value in feature_value.keys():  # 遍历该属性的所有切分点
            # 2.2.1 根据fea特征中的值value将数据集划分成左右子树（从第一行数据的第一列的数开始遍历，大于这个数的右子树，小于的左子树）
            (set_1, set_2) = split_tree(data, fea, value)
            # 2.2.2 计算当前的Gini指数
            nowGini = float(len(set_1) * cal_gini_index(set_1) + len(set_2) * cal_gini_index(set_2)) / len(data)
            # 2.2.3 计算Gini指数的增加量
            gain = currentGini - nowGini
            # 2.2.4 判断次划分是否比当前的划分更好
            if gain > bestGain and len(set_1) > 0 and len(set_2) > 0:
                bestGain = gain
                bestCriteria = (fea, value)
                bestSets = (set_1, set_2)
    # 3. 判断划分是否结束,迭代函数，左右子树肯定都有一个最佳节点，其tree.result的结果是统计值
    if bestGain > 0:
        right = build_tree(bestSets[0])
        left = build_tree(bestSets[1])
        return Node(fea=bestCriteria[0], value=bestCriteria[1], right=right, left=left)
    else:
        return Node(results=label_uniq_cnt(data))


def split_tree(data, fea, value):
    ''' 根据特征fea中的值value将数据集data划分成左右子树
    :param data:
    :param fea:
    :param value:
    :return:
    '''
    set_1 = []
    set_2 = []
    for x in data:
        if x[fea] >= value:
            set_1.append(x)
        else:
            set_2.append(x)
    return (set_1, set_2)


def cal_gini_index(data):
    ''' 根据基尼指数计算给定数据集的Gini指数
    :param data: (list)数据集
    :return: gini(float)Gini指数
    '''
    total_sample = len(data)
    if total_sample == 0:
        return 0
    label_counts = label_uniq_cnt(data)  # 统计数据集中不同标签个数
    gini = 0
    for label in label_counts:
        gini += pow(label_counts[label], 2)
    gini = 1 - float(gini) / pow(total_sample, 2)
    return gini


def label_uniq_cnt(data):
    ''' 统计数据集中不同类标签label的个数
    :param data:
    :return:
    '''
    label_uniq_cnt = {}
    for x in data:
        label = x[-1]  # 取得每一个样本的类标签label
        if label not in label_uniq_cnt:
            label_uniq_cnt[label] = 0
        label_uniq_cnt[label] = label_uniq_cnt[label] + 1
    return label_uniq_cnt


def predict(sample, tree):
    ''' 对每一个样本sample进行预测
    :param sample: (list) 需要预测的样本
    :param tree: (class)构建好的分类树
    :return:
    '''
    # 1.只是树根
    if tree.results != None:
        return tree.results
    else:
        # 2.有左右节点，训练数据中的数据与树节点的值比较，大于属于右子树，小于属于左子树
        val_sample = sample[tree.fea]
        branch = None
        if val_sample >= tree.value:
            branch = tree.right
        else:
            branch = tree.left
        return predict(sample, branch)

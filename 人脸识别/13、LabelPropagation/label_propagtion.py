# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt


def label_propagation(vector_dict, edge_dict):
    """ 标签传播
    :param vector_dict:节点，社区
    :param edge_dict: 存储节点之间的边和权重
    :return:
    """
    # 初始化，设置每个节点属于不同社区
    t = 0
    # 以随机的次序处理每个节点
    while True:
        if check(vector_dict, edge_dict) == 0:
            t += 1
            print('iteration:{}'.format(t))
            # 对每一个node进行更新
            for node in vector_dict.keys():
                adjacency_node_list = edge_dict[node]    # 获取节点node的邻接节点
                vector_dict[node] = get_max_community_label(vector_dict, adjacency_node_list)
            print(vector_dict)
        else:
            break
    return vector_dict


def get_max_community_label(vector_dict, adjacency_node_list):
    """ 得到相邻的节点中标签数最多的标签
    :param vector_dict: 节点，社区
    :param adjacency_node_list:的邻接节点
    :return:
    """
    label_dict = {}
    for node in adjacency_node_list:
        node_id_weight = node.strip().split(":")
        node_id = node_id_weight[0]   # 邻接节点
        node_weight = int(node_id_weight[1])  # 与邻接节点之间的权重
        if vector_dict[node_id] not in label_dict:
            label_dict[vector_dict[node_id]] = node_weight
        else:
            label_dict[vector_dict[node_id]] += node_weight
    # 找到最大的标签
    sort_list = sorted(label_dict.items(), key=lambda d: d[1], reverse=True)
    return sort_list[0][0]


def check(vector_dict, edge_dict):
    """ 检查是否满足终止条件
    :param vector_dict: 节点，社区
    :param edge_dict: 存储节点之间的边和权重
    :return:
    """
    for node in vector_dict.keys():
        adjacency_node_list = edge_dict[node]    # 与节点node相连接的节点
        node_label = vector_dict[node]  # 节点node所属社区
        label = get_max_community_label(vector_dict, adjacency_node_list)
        if node_label == label:    # 对每个节点，其所属的社区标签是最大的
            continue
        else:
            return 0
    return 1


def loadData(filePath):
    f = open(filePath)
    vector_dict = {}    # 存储节点
    edge_dict = {}      # 存储边
    for line in f.readlines():
        lines = line.strip().split('\t')
        for i in range(2):
            if lines[i] not in vector_dict:    # 节点已存储
                # 将节点放入到vector_dict中，设置所属社区为其自身
                vector_dict[lines[i]] = int(lines[i])
                # 将边放入到edge_dict
                edge_list = []
                if len(lines) == 3:
                    edge_list.append(lines[1 - i] + ":" + lines[2])
                else:
                    edge_list.append(lines[1 - i] + ":" + "1")
                edge_dict[lines[i]] = edge_list
            else:   # 节点未存储
                edge_list = edge_dict[lines[i]]
                if len(lines) == 3:
                    edge_list.append(lines[1 - i] + ":" + lines[2])
                else:
                    edge_list.append(lines[1 - i] + ":" + "1")
                edge_dict[lines[i]] = edge_list
    f.close()
    return vector_dict, edge_dict


def save_result(file_name, vec_new):
    f_result = open(file_name, "w")
    for key in vec_new.keys():
        f_result.write(str(key) + "\t" + str(vec_new[key]) + "\n")
    f_result.close()


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    vector_dict, edge_dict = loadData("cd_data.txt")
    print('original community:{} \n'.format(vector_dict))
    # 2、计算半径
    print("--------- 2.calculate eps ------------")
    vec_new = label_propagation(vector_dict, edge_dict)
    # 3、保存结果
    print("--------- 4.save result ------------")
    save_result('result1', vec_new)
    print('final_result:{}'.format(vec_new))
    # draw(testData, sub_class)

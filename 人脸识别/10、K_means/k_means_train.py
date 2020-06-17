# coding:UTF-8
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    '''导入数据
    input:  file_path(string):文件的存储位置
    output: data(mat):数据
    '''
    f = open(file_path)
    data = []
    for line in f.readlines():
        row = []  # 记录每一行
        lines = line.strip().split("\t")
        for x in lines:
            row.append(float(x))  # 将文本中的特征转换成浮点数
        data.append(row)
    f.close()
    return np.mat(data)


def distance(vecA, vecB):
    '''计算vecA与vecB之间的欧式距离的平方
    input:  vecA(mat)A点坐标
            vecB(mat)B点坐标
    output: dist[0, 0](float)A点与B点距离的平方
    '''
    dist = (vecA - vecB) * (vecA - vecB).T
    return dist[0, 0]


def randCent(data, k):
    '''随机初始化聚类中心
    input:  data(mat):训练数据
            k(int):类别个数
    output: centroids(mat):聚类中心
    '''
    n = np.shape(data)[1]  # 属性的个数
    centroids = np.mat(np.zeros((k, n)))  # 初始化k个聚类中心
    for j in range(n):  # 初始化聚类中心每一维的坐标
        minJ = np.min(data[:, j])  # 第j列数据的最小值
        rangeJ = np.max(data[:, j]) - minJ    # 第j列数据的最小值、最大值之差
        # 在最大值和最小值之间随机初始化， 初始化np.mat(np.ones((k, 1)))为4x1矩阵，乘以最小值。加上差值*初始值
        centroids[:, j] = minJ * np.mat(np.ones((k, 1))) \
                          + np.random.rand(k, 1) * rangeJ
    return centroids


def kmeans(data, k, centroids):
    '''根据KMeans算法求解聚类中心
    input:  data(mat):训练数据
            k(int):类别个数
            centroids(mat):随机初始化的聚类中心
    output: centroids(mat):训练完成的聚类中心
            subCenter(mat):每一个样本所属的类别
    '''
    m, n = np.shape(data)  # m：样本的个数，n：特征的维度
    subCenter = np.mat(np.zeros((m, n)))  # 初始化每一个样本所属的类别
    change = True  # 判断是否需要重新计算聚类中心
    while change == True:
        change = False  # 重置
        for i in range(m):
            minDist = np.inf  # 设置样本与聚类中心之间的最小的距离，初始值为正无穷
            minIndex = 0  # 所属的类别
            for j in range(k):     # 循环确认每个data值所属的类别以及到聚类中心的距离
                # 计算i和每个聚类中心之间的距离
                dist = distance(data[i, ], centroids[j, ])
                if dist < minDist:
                    minDist = dist
                    minIndex = j
            # 判断是否需要改变
            if subCenter[i, 0] != minIndex:  # 需要改变
                change = True
                subCenter[i, ] = np.mat([minIndex, minDist])
        # 重新计算聚类中心
        for j in range(k):
            sum_all = np.mat(np.zeros((1, n)))
            r = 0  # 每个类别中的样本的个数
            for i in range(m):
                if subCenter[i, 0] == j:  # 计算第j个类别
                    sum_all += data[i, ]  # 计算属于j类的所有data的值的和
                    r += 1
            for z in range(n):
                try:
                    centroids[j, z] = sum_all[0, z] / r     # 求平均值，获取新的聚类中心
                except:
                    print("r is zero")
    return subCenter


def save_result(file_name, source):
    '''保存source中的结果到file_name文件中
    input:  file_name(string):文件名
            source(mat):需要保存的数据
    output:
    '''
    m, n = np.shape(source)
    f = open(file_name, "w")
    for i in range(m):
        tmp = []
        for j in range(n):
            tmp.append(str(source[i, j]))
        f.write("\t".join(tmp) + "\n")
    f.close()


def draw(data, sub):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    x2List = []
    y2List = []
    x3List = []
    y3List = []
    m = np.shape(data)[0]
    for i in range(m):
        if float(sub[i, 0]) == 0.0:
            x0List.append(data[i, 0])
            y0List.append(data[i, 1])
        elif float(sub[i, 0]) == 1.0:
            x1List.append(data[i, 0])
            y1List.append(data[i, 1])
        elif float(sub[i, 0]) == 2.0:
            x2List.append(data[i, 0])
            y2List.append(data[i, 1])
        elif float(sub[i, 0]) == 3.0:
            x3List.append(data[i, 0])
            y3List.append(data[i, 1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='yellow')
    ax.scatter(x2List, y2List, s=10, c='green')
    ax.scatter(x3List, y3List, s=10, c='blue')
    plt.show()


if __name__ == "__main__":
    k = 4  # 聚类中心的个数
    file_path = "data.txt"
    # 1、导入数据
    print("---------- 1.load data ------------")
    data = load_data(file_path)
    # 2、随机初始化k个聚类中心
    print("---------- 2.random center ------------")
    centroids = randCent(data, k)
    # 3、聚类计算
    print("---------- 3.kmeans ------------")
    subCenter = kmeans(data, k, centroids)
    # 4、保存所属的类别文件
    print("---------- 4.save subCenter ------------")
    save_result("sub", subCenter)
    # 5、保存聚类中心
    print("---------- 5.save centroids ------------")
    save_result("center", centroids)
    draw(data, subCenter)

# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt


def ridge_regression(feature, label, lam):
    ''' 最小二乘求解方程
    :param feature: 特征
    :param label:  标签
    :param lam: 正则化系数
    :return:
    '''
    n = np.shape(feature)[1]
    w = (feature.T * feature + lam * np.mat(np.eye(n))).I * feature.T * label
    return w


def bfgs(feature, label, lam, maxCycle):
    ''' 利用bfgs训练Ridge Regression模型
    :param feature: 特征
    :param label: 标签
    :param lam: 正则化系数
    :param maxCycle: 最大迭代次数
    :return:
    '''
    n = np.shape(feature)[1]
    # 初始化
    w0 = np.mat(np.zeros((n, 1)))
    rho = 0.55
    sigma = 0.4
    Bk = np.eye(n)
    k = 1
    while k < maxCycle:
        print('\t iter:{} \t error:{}'.format(k, get_error(feature, label, w0)))
        gk = get_gradient(feature, label, w0, lam)  # 计算梯度
        dk = np.mat(-np.linalg.solve(Bk, gk))  # np.linalg.solve： 求解ax = b
        m = 0
        mk = 0
        while m < 20:
            newf = get_result(feature, label, (w0 + rho ** m * dk), lam)
            oldf = get_result(feature, label, w0, lam)
            if newf < oldf + sigma * (rho ** m) * (gk.T * dk)[0, 0]:
                mk = m
                break
            m += 1
        # BFGS校正
        w = w0 + rho ** mk * dk
        sk = w - w0
        yk = get_gradient(feature, label, w, lam) - gk
        if yk.T * sk > 0:
            # BFGS校正公式
            Bk = Bk - (Bk * sk * sk.T * Bk) / (sk.T * Bk * sk) + (yk * yk.T) / (yk.T * sk)
        k = k + 1
        w0 = w
    return w0


def get_gradient(feature, label, w, lam):
    ''' 计算导数的值
    :param feature:
    :param label:
    :param w:
    :param lam:
    :return:
    '''
    err = (label - feature * w).T
    left = err * (-1) * feature
    return left.T + lam * w


def get_result(feature, label, w, lam):
    ''' 计算训练样本的岭回归模型即建立的岭回归模型
    :param feature:
    :param label:
    :param w:
    :param lam:
    :return:
    '''
    left = (label - feature * w).T * (label - feature * w)
    right = lam * w.T * w
    return (left + right) / 2


def get_error(feature, label, w):
    '''
    input:  feature(mat):特征
            label(mat):标签
    output: w(mat):回归系数
    '''
    m = np.shape(feature)[0]
    left = (label - feature * w).T * (label - feature * w)
    return (left / (2 * m))[0, 0]


def lbfgs(feature, label, lam, maxCycle, m=10):
    ''' 利用lbfgs训练Ridge Regression模型
    :param feature: 特征
    :param label: 标签
    :param lam: 正则化参数
    :param maxCycle: 最大迭代次数
    :param m: lbfgs中选择保留的个数
    :return:
    '''
    n = np.shape(feature)[1]
    # 1、初始化
    w0 = np.mat(np.zeros((n, 1)))
    rho = 0.55
    sigma = 0.4
    H0 = np.eye(n)
    s = []
    y = []
    k = 1
    gk = get_gradient(feature, label, w0, lam)
    dk = -H0 * gk
    # 2、迭代
    while k < maxCycle:
        if k % 100 == 0:
            print('iter:{}\t error:{}'.format(k, get_error(feature, label, w0)))
        m1 = 0
        mk = 0
        gk = get_gradient(feature, label, w0, lam)
        # 2.1 Armijo线搜索
        while m1 < 20:
            newf = get_result(feature, label, (w0 + rho ** m1 * dk), lam)
            oldf = get_result(feature, label, w0, lam)
            if newf < oldf + sigma * (rho ** m1) * (gk.T * dk)[0, 0]:
                mk = m1
                break
            m1 = m1 + 1
        # 2.2 LBFGS校正
        w = w0 + rho ** mk * dk
        # 保留m个
        if k > m:
            s.pop(0)
            y.pop(0)
        # 保留最新的
        sk = w - w0
        qk = get_gradient(feature, label, w, lam)
        yk = qk - gk

        s.append(sk)
        y.append(yk)
        # two-loop
        t = len(s)
        a = []
        for i in range(t):
            alpha = (s[t - i - 1].T * qk) / (y[t - i - 1].T * s[t - i - 1])
            qk = qk - alpha[0, 0] * y[t - i - 1]
            a.append(alpha[0, 0])
        r = H0 * qk
        for i in range(t):
            beta = (y[i].T * r) / (y[i].T * s[i])
            r = r + s[i] * (a[t-i-1] - beta[0, 0])

        if yk.T * sk > 0:
            dk = -r
        k = k + 1
        w0 = w
    return w0


def load_data(file_path):
    f = open(file_path)
    feature = []
    label = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split('\t')
        feature_tmp.append(1)
        for i in range(len(lines) - 1):
            feature_tmp.append(float(lines[i]))
        feature.append(feature_tmp)
        label.append(float(lines[-1]))
    f.close()
    return np.mat(feature), np.mat(label).T


def save_model(file_name, w):
    f = open(file_name, 'w')
    m, n = np.shape(w)
    for i in range(m):
        w_tmp = []
        for j in range(n):
            w_tmp.append(str(w[i, j]))
        f.write('\t'.join(w_tmp))
        f.write('\n')
    f.close()


def draw(file_name, feature, w):
    x0List = []
    y0List = []
    x1List = []
    y1List = []
    predict = feature * w
    m = np.shape(predict)[0]
    for i in range(m):
        y1List.append(predict[i, 0])
    f = open(file_name, 'r')
    for line in f.readlines():
        lines = line.strip().split('\t')

        x0List.append(float(lines[0]))
        y0List.append(float(lines[-1]))
        x1List.append(float(lines[0]))

    f.close()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List, y0List, s=10, c='red')
    ax.scatter(x1List, y1List, s=10, c='black')
    plt.show()


if __name__ == '__main__':
    # 1、导入数据
    print("--------- 1.load data ------------")
    # feature：数据， label：标签， n_class：标签个数
    feature, label = load_data("data.txt")
    # 2、最下二乘求解
    print("--------- 2.training ------------")
    method = 'lbfgs'   # 选择的方法
    if method == 'bfgs':
        w0 = bfgs(feature, label, 0.5, 1000)
    elif method == 'lbfgs':
        w0 = lbfgs(feature, label, 0.5, 1000, m=10)
    else:
        w0 = ridge_regression(feature, label, 0.5)

    # 4、保存结果
    print("--------- 4.save result ------------")
    save_model('weights', w0)
    # draw("data.txt", feature, w0)


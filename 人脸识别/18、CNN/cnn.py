# coding: utf-8

import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

batch_size = 128


class CNN():
    def __init__(self, input_data_trX, input_data_trY, input_data_vaX, input_data_vaY, input_data_teX, input_data_teY):
        self.w = None  # 第一个卷积层的权重
        self.b = None  # 第一个卷积层的偏置
        self.w2 = None  # 第二个卷积层的权重
        self.b2 = None  # 第二个卷积层的偏置
        self.w3 = None  # 第三个卷积层的权重
        self.b3 = None  # 第三个卷积层的偏置
        self.w4 = None  # 全连接层中输入层到隐含层的权重
        self.b4 = None  # 全连接层中输入层到隐含层的偏置
        self.w_0 = None  # 隐含层到输出层的权重
        self.b_0 = None  # 隐含层到输出层的偏置
        self.p_keep_conv = None  # 卷积层中样本保持不变的比例
        self.p_keep_hidden = None  # 全连接层中样本保持不变的比例
        self.trX = input_data_trX  # 训练数据中的特征
        self.trY = input_data_trY  # 训练数据中的标签
        self.vaX = input_data_vaX  # 验证数据中的特征
        self.vaY = input_data_vaY  # 验证数据中的标签
        self.teX = input_data_teX  # 测试数据中的特征
        self.teY = input_data_teY  # 测试数据中的标签

    def fit(self):
        X = tf.placeholder("float", [None, 28, 28, 1])
        Y = tf.placeholder("float", [None, 10])

        # 第一层卷积核大小为3x3，输入一张图，输出32个feature map
        self.w = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))
        self.b = tf.Variable(tf.constant(0.0, shape=[32]))
        # 第二层卷积核大小为3x3,输入32个feature map,输出64个feature map
        self.w2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
        self.b2 = tf.Variable(tf.constant(0.0, shape=[64]))
        # 第三层卷积核大小为3x3，输入64个feature map,输出128个feature map
        self.w3 = tf.Variable(tf.random_normal([3, 3, 64, 128], stddev=0.01))
        self.b3 = tf.Variable(tf.constant(0.0, shape=[128]))
        # FC 128*4*4  inputs, 625 output
        self.w4 = tf.Variable(tf.random_normal([128 * 4 * 4, 625], stddev=0.01))
        self.b4 = tf.Variable(tf.constant(0.0, shape=[625]))
        # FC 625 inputs, 10 output (labels)
        self.w_0 = tf.Variable(tf.random_normal([625, 10], stddev=0.01))
        self.b_0 = tf.Variable(tf.constant(0.0, shape=[10]))
        self.p_keep_conv = tf.placeholder("float")  # 卷积层的dropout概率
        self.p_keep_hidden = tf.placeholder("float")  # 全连接层的dropout概率

        # 第一个卷积层：padding=SAME, 保证输出的feature map与输入矩阵的大小相同，输出值与输入值大小相同，卷积不会改变输出值的大小
        l_c_1 = tf.nn.relu(
            tf.nn.conv2d(X, self.w, strides=[1, 1, 1, 1], padding='SAME') + self.b)  # l_c_1大小为(?,28,28,32)
        # max_pooling,窗口大小为2x2，池化会改变输入值的大小
        l_p_1 = tf.nn.max_pool(l_c_1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                               padding='SAME')  # l_p_1 shape=（？, 14, 14, 32）
        # dropout: 每个神经元有p_keep_conv的概率以1/p_keep_conv的比例进行归一化，有(1-p_keep_conv)的概率置为0
        l1 = tf.nn.dropout(l_p_1, self.p_keep_conv)

        # 第二个卷积层
        l_c_2 = tf.nn.relu(
            tf.nn.conv2d(l1, self.w2, strides=[1, 1, 1, 1], padding='SAME') + self.b2)  # l_c_2大小为(?,14,14,64)
        # max_pooling,窗口大小为2x2
        l_p_2 = tf.nn.max_pool(l_c_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                               padding='SAME')  # l_p_1 shape=（？, 7, 7, 64）
        # dropout: 每个神经元有p_keep_conv的概率以1/p_keep_conv的比例进行归一化，有(1-p_keep_conv)的概率置为0
        l2 = tf.nn.dropout(l_p_2, self.p_keep_conv)

        # 第三个卷积层
        l_c_3 = tf.nn.relu(
            tf.nn.conv2d(l2, self.w3, strides=[1, 1, 1, 1], padding='SAME') + self.b3)  # l_c_2大小为(?,7,7,128)
        # max_pooling,窗口大小为2x2
        l_p_3 = tf.nn.max_pool(l_c_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                               padding='SAME')  # l_p_1 shape=（？, 4, 4, 128）
        # dropout: 每个神经元有p_keep_conv的概率以1/p_keep_conv的比例进行归一化，有(1-p_keep_conv)的概率置为0
        l3 = tf.reshape(l_p_3, [-1, self.w4.get_shape().as_list()[0]])  # reshape to (?, 2048)
        l3 = tf.nn.dropout(l3, self.p_keep_conv)

        # 后面两层为全连接层
        l4 = tf.nn.relu(tf.matmul(l3, self.w4) + self.b4)
        l4 = tf.nn.dropout(l4, self.p_keep_hidden)

        pyx = tf.matmul(l4, self.w_0) + self.b_0
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pyx, labels=Y))  # 交叉熵目标函数
        train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)  # RMSPro算法最小化目标函数
        predict_op = tf.argmax(pyx, 1)  # 返回每个样本的预测结果
        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            for i in range(30):
                training_batch = zip(range(0, len(self.trX), batch_size),
                                     range(batch_size, len(self.trX) + 1, batch_size))
                for start, end in training_batch:
                    sess.run(train_op, feed_dict={X: self.trX[start:end], Y: self.trY[start:end], self.p_keep_conv: 0.8,
                                                  self.p_keep_hidden: 0.5})
                if i % 3 == 0:
                    corr = np.mean(np.argmax(self.vaY, axis=1) == sess.run(predict_op,
                                                                           feed_dict={X: self.vaX, Y: self.vaY,
                                                                                      self.p_keep_conv: 1.0,
                                                                                      self.p_keep_hidden: 1.0}))
                    print('Accuaracy at step %d on validation set: %s' % (i, corr))
            # 最终在测试集上的输出
            corr_te = np.mean(np.argmax(self.teY, axis=1) == sess.run(predict_op, feed_dict={X: self.teX, Y: self.teY,
                                                                                             self.p_keep_conv: 1.0,
                                                                                             self.p_keep_hidden: 1.0}))
            print('Accuaracy on test set: %s' % corr_te)


if __name__ == '__main__':
    # 1.导入数据集
    mnist = input_data.read_data_sets("D:/tensfl/MNIST_data/", one_hot=True)
    # 2.mnist.train.images是一个55000*784维的矩阵，mnist.train.labels是一个55000*10维的矩阵
    trX, trY, vaX, vaY, teX, teY = mnist.train.images, mnist.train.labels, mnist.validation.images, mnist.validation.labels, mnist.test.images, mnist.test.labels
    trX = trX.reshape(-1, 28, 28, 1)
    vaX = vaX.reshape(-1, 28, 28, 1)
    teX = teX.reshape(-1, 28, 28, 1)
    cnn = CNN(trX, trY, vaX, vaY, teX, teY)
    cnn.fit()

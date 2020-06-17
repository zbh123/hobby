# coding：utf-8

import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data


class DenoisingAutoEncoder():
    def __init__(self, n_hidden, input_data, corruption_level=0.3):
        self.W = None  # 输入层到隐含层的权重
        self.b = None  # 输入层到隐含层的偏置
        self.encode_r = None  # 隐含层的输出
        self.input_data = input_data  # 输入样本
        self.layer_size = n_hidden  # 隐含层节点的个数
        self.keep_prob = 1 - corruption_level  # 特征保持不变的比例
        self.W_eval = None  # 权重W的值
        self.b_eval = None  # 偏置b的值

    def fit(self):
        # 输入层节点的个数
        n_visible = self.input_data.shape[1]
        # 输入的一张图片用28*28=784的向量表示
        X = tf.placeholder("float", [None, n_visible], name='X')
        # 用于将部分输入数据置为0
        mask = tf.placeholder('float', [None, n_visible], name='mask')
        # 创建权重和偏置
        W_init_max = 4 * np.sqrt(6. / (n_visible + self.layer_size))
        W_init = tf.random_uniform(shape=[n_visible, self.layer_size], minval=-W_init_max, maxval=W_init_max)
        # 编码器
        self.W = tf.Variable(W_init, name='W')  # 784*500
        self.b = tf.Variable(tf.zeros([self.layer_size]), name='b')  # 隐含层的偏置
        # 解码器
        W_prime = tf.transpose(self.W)
        b_prime = tf.Variable(tf.zeros([n_visible]), name='b_prime')
        tilde_X = mask * X  # 对输入样本加入噪音
        Y = tf.nn.sigmoid(tf.matmul(tilde_X, self.W) + self.b)  # 隐含层的输出
        Z = tf.nn.sigmoid(tf.matmul(Y, W_prime) + b_prime)  # 重构输出
        cost = tf.reduce_mean(tf.pow(X - Z, 2))  # 均方误差
        # 最小化均方误差
        train_op = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

        trX = self.input_data
        # 开始训练
        with tf.Session() as sess:
            # 初始化所有的参数
            tf.initialize_all_variables().run()
            for i in range(30):
                for start, end in zip(range(0, len(trX), 128), range(128, len(trX) + 1, 128)):
                    input_ = trX[start:end]  # 设置输入
                    mask_np = np.random.binomial(1, self.keep_prob, input_.shape)  # 设置mask
                    # 开始训练
                    sess.run(train_op, feed_dict={X: input_, mask: mask_np})
                if i % 5 == 0:
                    mask_np = np.random.binomial(1, 1, trX.shape)
                    print("loss function at step %d is %s" % (i, sess.run(cost, feed_dict={X: trX, mask: mask_np})))
                # 保存好输入层到隐含层的参数
                self.W_eval = self.W.eval()
                self.b_eval = self.b.eval()
                mask_np = np.random.binomial(1, 1, trX.shape)
                self.encode_r = Y.eval({X: trX, mask: mask_np})

    def get_value(self):
        return self.W_eval, self.b_eval, self.encode_r


class StackedDenoisingAutoEncoder():
    def __init__(self, hidden_list, input_data_trainX, input_data_trainY, input_data_validX, input_data_validY,
                 input_data_testX, input_data_testY, corruption_level=0.3):
        self.ecod_W = []  # 保存网络中每一层权重
        self.ecod_b = []  # 保存网络中每一层偏置
        self.hidden_list = hidden_list  # 每个隐含层的节点个数
        self.input_data_trainX = input_data_trainX  # 训练样本的特征
        self.input_data_trainY = input_data_trainY  # 训练样本的标签
        self.input_data_validX = input_data_validX  # 验证样本的特征
        self.input_data_validY = input_data_validY  # 验证样本的标签
        self.input_data_testX = input_data_testX  # 测试样本的特征
        self.input_data_testY = input_data_testY  # 测试样本的标签

    def fit(self):
        # 1.训练每个降噪自编码器
        next_input_data = self.input_data_trainX
        for i, hidden_size in enumerate(self.hidden_list):
            print('-----training the %s sda-------' % (i + 1))
            dae = DenoisingAutoEncoder(hidden_size, next_input_data)
            dae.fit()
            W_eval, b_eval, encode_eval = dae.get_value()
            self.ecod_W.append(W_eval)
            self.ecod_b.append(b_eval)
            next_input_data = encode_eval
        # 2.堆叠
        n_input = self.input_data_trainX.shape[1]
        n_output = self.input_data_trainY.shape[1]

        X = tf.placeholder("float", [None, n_input], name='X')
        Y = tf.placeholder("float", [None, n_output], name='Y')

        encoding_w_tmp = []
        encoding_b_tmp = []

        last_layer = None
        layer_nodes = []
        encoder = X
        for i, hidden_size in enumerate(self.hidden_list):
            # 以每一个自编码器的值作为初始值
            encoding_w_tmp.append(tf.Variable(self.ecod_W[i], name='enc-w-{}'.format(i)))
            encoding_b_tmp.append(tf.Variable(self.ecod_b[i], name='enc-b-{}'.format(i)))
            encoder = tf.nn.sigmoid(tf.matmul(encoder, encoding_w_tmp[i]) + encoding_b_tmp[i])
            layer_nodes.append(encoder)
            last_layer = layer_nodes[i]
        # 加入少量的噪声来打破对称性以及避免0梯度
        last_W = tf.Variable(tf.truncated_normal([last_layer.get_shape()[1].value, n_output], stddev=0.1),
                             name='sm-weights')
        last_b = tf.Variable(tf.constant(0.1, shape=[n_output]), name='sm-biases')
        last_out = tf.matmul(last_layer, last_W) + last_b
        layer_nodes.append(last_out)
        cost_sme = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=last_out, labels=Y))
        train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cost_sme)
        model_prediction = tf.argmax(last_out, 1)
        correct_prediction = tf.equal(model_prediction, tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        # 微调
        trX = self.input_data_trainX
        trY = self.input_data_trainY
        vaX = self.input_data_validX
        vaY = self.input_data_validY
        teX = self.input_data_testX
        teY = self.input_data_testY
        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            for i in range(50):
                for start, end in zip(range(0, len(trX), 128), range(128, len(trX) + 1, 128)):
                    sess.run(train_step, feed_dict={X: trX[start:end], Y: trY[start:end]})
                if i % 5.0 == 0:
                    print('Accuracy at step %d on validation set: %s' % (
                    i, sess.run(accuracy, feed_dict={X: vaX, Y: vaY})))
                    print('Accuracy on test set: %s' % (sess.run(accuracy, feed_dict={X: teX, Y: teY})))


if __name__ == '__main__':
    # 1.导入数据集
    mnist = input_data.read_data_sets("D:/tensfl/MNIST_data/", one_hot=True)
    # 2.训练SDAE模型
    sda = StackedDenoisingAutoEncoder([1000, 1000, 1000], mnist.train.images, mnist.train.labels,
                                      mnist.validation.images, mnist.validation.labels, mnist.test.images,
                                      mnist.test.labels)
    sda.fit()

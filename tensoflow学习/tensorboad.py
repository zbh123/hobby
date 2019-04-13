import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def add_layer(input, in_size, out_size, n_layer, activation_function=None):
    '''
    添加层
    :param input: 输入数据
    :param in_size:input的size
    :param out_size: 输出的size
    :param activation_function:激励函数
    :return:
    '''
    layer_name = 'layer%s'%n_layer
    with tf.name_scope('layer'):
        with tf.name_scope('weights'):
            Weights = tf.Variable(tf.random_normal([in_size, out_size]), name='W')
            tf.histogram_summary(layer_name+'/weights', Weights)
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size])+0.1, name='b')
            tf.histogram_summary(layer_name + '/biases', biases)
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.add(tf.matmul(input, Weights), biases)
        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)
        tf.histogram_summary(layer_name + '/outputs', outputs)
        return outputs

# Make up some real data
x_data = np.linspace(-1,1,300)[:,np.newaxis]
noise = np.random.normal(0,0.05,x_data.shape)
y_data = np.square(x_data)-0.5+noise

# inputs部分
with tf.name_scope('inputs'):
    xs = tf.placeholder(tf.float32,[None, 1], name='x_input')
    ys = tf.placeholder(tf.float32,[None, 1], name='y_input')

#
l1 = add_layer(xs, 1, 10, 1, activation_function=tf.nn.relu)
# 输入l1， l1的size是上一步输出的size10， out_size是y的size也就相当于预测值的size
predition = add_layer(l1, 10, 1, 2, activation_function=None)
# tf.square：求误差的平方， tf.reduce_sum是求和函数，tf.reduce_mean是求均值的函数
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-predition), reduction_indices=[1]))
    tf.scalar_summary('loss', loss)
# 优化器
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)


sess = tf.Session()
merged = tf.merge_all_summaries()
# 上述内容写入logs文件夹，可以在terminor上，运行 tensorboard --logdir='logs/',会返回一个网址
# 打开网址即可看到内容
writer = tf.train.SummaryWriter("logs/", sess.graph)
sess.run(tf.initialize_all_variables())

for i in range(1000):
    sess.run(train_step, feed_dict={xs:x_data, ys:y_data})
    if i%50 == 0:
        result = sess.run(merged, feed_dict={xs:x_data, ys:y_data})
        writer.add_summary(result, i)







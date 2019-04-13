import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# number 1 to 10 data
mnist = input_data.read_data_sets('MNIST_data', onehot=True)


def add_layer(input, in_size, out_size, activation_function=None):
    '''
    添加层
    :param input: 输入数据
    :param in_size:input的size
    :param out_size: 输出的size
    :param activation_function:激励函数
    :return:
    '''
    Weights = tf.Variable(tf.random_normal([in_size, out_size]), name='W')
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name='b')
    Wx_plus_b = tf.add(tf.matmul(input, Weights), biases)
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

def compute_accuracy(v_xs,v_ys):
    global prediction
    # 是一个10*1的数列，值是0-1之间的值
    y_pre = sess.run(prediction, feed_dict={xs:v_xs})
    # 判断相等，取预测值最大的值和准确值相比
    correction_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys,1))
    # 查看预测准确的平均值，即准确率
    accuracy = tf.reduce_mean(tf.cast(correction_prediction, tf.float32))
    # result是预测百分比
    result = sess.run(accuracy, feed_dict={xs:v_xs, ys:v_ys})
    return result


# 784是784个像素点，即28*28的大小
xs = tf.placeholder(tf.float32, [None, 784])
# 输出是一个矩阵，10*1.用来表示十个数
ys = tf.placeholder(tf.float32, [None, 10])

prediction = add_layer(xs, 784, 10, activation_function=tf.nn.softmax)

# 计算loss
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.Session()
sess.run(tf.initialize_all_variables())

for i in range(100):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={xs:batch_xs, ys:batch_ys})
    if i%50 == 0:
        print(compute_accuracy(
            mnist.test.images, mnist.test.lables
        ))

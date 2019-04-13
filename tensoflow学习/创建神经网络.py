import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def add_layer(input, in_size, out_size, activation_function=None):
    '''
    添加层
    :param input: 输入数据
    :param in_size:input的size
    :param out_size: 输出的size
    :param activation_function:激励函数
    :return:
    '''
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size])+0.1)
    Wx_plus_b = tf.matmul(input, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs
# linspace(-1,1,300)[:,np.newaxis],含义（-1,1,300）区间是-1到1，有300行（300个例子），
# [:,np.newaxis]相应的维度
x_data = np.linspace(-1,1,300)[:, np.newaxis]
# 噪音区间是0到0.05，大小是x_data的维度
noise = np.random.normal(0,0.05,x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

# 用于传值，[None, 1]数值大小及shape，None可以系统自己计算，1是每次计算的个数
# xs， ys一个xs对应一个ys
xs = tf.placeholder(tf.float32,[None, 1])
ys = tf.placeholder(tf.float32,[None, 1])

# x_data一个参数， 隐藏层有10个神经元
l1 = add_layer(x_data, 1, 10, activation_function=tf.nn.relu)
# 输入l1， l1的size是上一步输出的size10， out_size是y的size也就相当于预测值的size
predition = add_layer(l1, 10, 1, activation_function=None)
# tf.square：求误差的平方， tf.reduce_sum是求和函数，tf.reduce_mean是求均值的函数
loss = tf.reduce_mean(tf.reduce_sum(tf.square(y_data-predition), reduction_indices=[1]))
# 优化器
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
# 初始变量
init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
# 显示真实数据
ax.scatter(x_data, y_data)
# 使函数连续执行，不会暂停
plt.ion()
plt.show()
for i in range(1000):
    sess.run(train_step, feed_dict={xs:x_data, ys:y_data})
    if i % 50 ==0 :
        print(sess.run(loss, feed_dict={xs:x_data, ys:y_data}))
        try:
            # 去除上面的线
            ax.lines.remove(lines[0])
        except Exception:
            pass
        predition_value = sess.run(predition, feed_dict={xs:x_data})
        # 线宽为5
        lines = ax.plot(x_data, predition_value,'r-',lw=5)
        plt.pause(0.1)



import tensoflow as tf
import numpy as np

#创建数据
# 随机生成100个数
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data*0.1 + 0.3

# 开始创建TensorFlow结构
# 权重是一个[1],随机取值范围-1.0到1.0
Weights = tf.Variable(tf.random_uniform([1],-1.0,1.0))
# 偏置值个数为1，初始为0
biases = tf.Variable(tf.zeros([1]))
# 预测值
y = Weights*x_data + biases
# 损失值
loss = tf.reduce_mean(tf.square(y-y_data))
# 优化器，0.5是学习效率，小于1
optimizer = tf.train.GradientDescentOptimizer(0.5)
# 优化器减小误差
train = optimizer.minimize(loss)

# 初始化结构
init = tf.initialize_all_variables()

# 开始创建TensorFlow结构

# 设置神经网络
sess = tf.Session()
# 激活神经网络
sess.run(init)

for step in range(201):
    sess.run(train)
    if step % 20 ==0:
        print(step, sess.run(Weights), sess.run(biases))






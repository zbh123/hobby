import tensorflow as tf

# Variable变量定义，初始值为0，名称为counter
state = tf.Variable(0, name='counter')
# print(state.name)

# 定义常量
one = tf.constant(1)

# 变量加法
new_value = tf.add(state, one)
# 变量更新
update = tf.assign(state, new_value)

# 初始化所有tf的变量
init = tf.initialize_all_variables()

with tf.Session() as sess:
    # 激活变量，有变量的时候需要激活tf中的变量
    sess.run(init)
    for _ in range(3):
        # 执行update操作
        sess.run(update)
        print(sess.run(state))






import tensorflow as tf

# placeholder占位符，（变量类型，结构如[2,2]）
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

output = tf.mul(input1, input2)

with tf.Session() as sess:
    # 当用placeholder定义变量时，需要使用feed_dict传值
    print(sess.run(output, feed_dict={input1:[7.], input2:[5.]}))






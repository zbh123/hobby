import tensoflow as tf


matrix1 = tf.constant([[3,3]])
matrix2 = tf.constant([[2],
                       [2]])
# matmul矩阵乘法，返回值
product = tf.matmul(matrix1, matrix2)

# 方式1
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()

# 方式2
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)




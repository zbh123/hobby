import tensorflow as tf


def add_layer(input, in_size, out_size, activation_function=None):
    '''
    添加层
    :param input: 输入数据
    :param in_size:行
    :param out_size: 列
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







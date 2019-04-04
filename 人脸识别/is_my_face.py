import tensorflow as tf
import cv2
import dlib
import numpy as np
import os
import random
import sys
from sklearn.model_selection import train_test_split

my_faces_path = './my_faces'
other_faces_path = './other_faces'
size = 64

imgs = []
labs = []


def getPaddingSize(img):
    h, w, _ = img.shape
    top, bottom, left, right = (0, 0, 0, 0)
    longest = max(h, w)

    if w < longest:
        tmp = longest - w
        # //表示整除符号
        left = tmp // 2
        right = tmp - left
    elif h < longest:
        tmp = longest - h
        top = tmp // 2
        bottom = tmp - top
    else:
        pass
    return top, bottom, left, right


def readData(path, h=size, w=size):
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            filename = path + '/' + filename

            img = cv2.imread(filename)

            top, bottom, left, right = getPaddingSize(img)
            # 将图片放大， 扩充图片边缘部分
            # 这里的作用是将图片扩充成正方形，top, bottom, left, right分别是按最大边长合成正方形所缺少的部分
            img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            img = cv2.resize(img, (h, w))

            imgs.append(img)
            labs.append(path)


readData(my_faces_path)
readData(other_faces_path)
# 将图片数据与标签转换成数组
imgs = np.array(imgs)
labs = np.array([[0, 1] if lab == my_faces_path else [1, 0] for lab in labs])
# 随机划分测试集与训练集
train_x, test_x, train_y, test_y = train_test_split(imgs, labs, test_size=0.05, random_state=random.randint(0, 100))
# 参数：图片数据的总数，图片的高、宽、通道
# np中的shape：二维情况下0,1表示二维数组的行列，三维情况下：0表示包含二维数组的个数，1,2表示三维数组的行和列
train_x = train_x.reshape(train_x.shape[0], size, size, 3)
test_x = test_x.reshape(test_x.shape[0], size, size, 3)
# 将数据转换成小于1的数
train_x = train_x.astype('float32') / 255.0
test_x = test_x.astype('float32') / 255.0

print('train size:%s, test size:%s' % (len(train_x), len(test_x)))
# 图片块，每次取128张图片
batch_size = 128
num_batch = len(train_x) // 128
# placeholder占位符，它的好处是可以避免生成大量常量来提供输入数据，提高了计算图的利用率
# 占位符，顾名思义，用来占位置的字符，即可以定义模型大小，而不填充参数，类似于形参，先将graph的大小框架搭建好
# 当sess.run的时候才会正式执行，feed_dict用于传参
# 式中shape=[None,size,size,3]None表示要传入的图片数量（None表示不确定），size是图片大小，高宽可不同，最后的3是通道数
x = tf.placeholder(tf.float32, [None, size, size, 3])
y_ = tf.placeholder(tf.float32, [None, 2])

keep_prob_5 = tf.placeholder(tf.float32)
keep_prob_75 = tf.placeholder(tf.float32)


def weightVariable(shape):
    # 返回随机张量（卷积核），其正态分布的标准差为0.01，即从正态分布的值中随机选取几个张量，张量的形状为shape
    init = tf.random_normal(shape, stddev=0.01)
    return tf.Variable(init)


def biasVariable(shape):
    # 用于从服从指定正太分布的数值中取出指定个数的值
    init = tf.random_normal(shape)
    return tf.Variable(init)


def conv2d(x, W):
    # 参数：x是输入图像，W是卷积核包含（卷积核的高度，卷积核的宽度，图像通道数，卷积核个数），strides卷积时图像每一维的步长，padding卷积方式
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def maxPool(x):
    # 参数： x是输入，ksize池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]，因为我们不想在batch和channels上做池化，
    # 所以这两个维度设为了1，height, width是池化窗口的大小，
    # 第三个参数strides：和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def dropout(x, keep):
    # x：输入
    # keep_prob：保留比例，取值(0,1]
    return tf.nn.dropout(x, keep)


def cnnLayer():
    # 第一层： 输入层预处理
    W1 = weightVariable([3, 3, 3, 32])  # 卷积核大小(3,3)， 输入通道(3)即移动步长， 输出通道(32)即填充大小，为调用函数输出张量的形状
    b1 = biasVariable([32])   # 其他影响因子
    # 卷积和激励层ReLU，目的计算激活函数即max（features， 0），实际上就是卷积层的输出结果做一次非线性映射
    conv1 = tf.nn.relu(conv2d(x, W1) + b1)
    # 池化，特征降维
    pool1 = maxPool(conv1)
    # 减少过拟合，随机让某些权重不更新
    drop1 = dropout(pool1, keep_prob_5)

    # 第二层
    W2 = weightVariable([3, 3, 32, 64])
    b2 = biasVariable([64])
    conv2 = tf.nn.relu(conv2d(drop1, W2) + b2)
    pool2 = maxPool(conv2)
    drop2 = dropout(pool2, keep_prob_5)

    # 第三层
    W3 = weightVariable([3, 3, 64, 64])
    b3 = biasVariable([64])
    conv3 = tf.nn.relu(conv2d(drop2, W3) + b3)
    pool3 = maxPool(conv3)
    drop3 = dropout(pool3, keep_prob_5)

    # 全连接层
    Wf = weightVariable([8 * 16 * 32, 512])
    bf = biasVariable([512])
    # reshape改变张量形状，[-1,8*16*32]，转换为第二个维度尺寸为9的张量，即n*9的张量，-1代表n，可自动计算出来
    # 如果shape传入的向量某一个分量设置为-1，那么这个分量代表的维度尺寸会被自动计算出来。
    drop3_flat = tf.reshape(drop3, [-1, 8 * 16 * 32])
    # tf.matmul(drop3_flat, Wf)计算两个张量矩阵的乘积
    # tf.multiply（）两个矩阵中对应元素各自相乘
    dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
    dropf = dropout(dense, keep_prob_75)

    # 输出层
    Wout = weightVariable([512, 2])
    bout = biasVariable([2])
    # tf.add（，）将参数相加
    out = tf.add(tf.matmul(dropf, Wout), bout)
    return out


output = cnnLayer()
# tf.argmax()函数中有个axis参数（轴），该参数能指定按照哪个维度计算。
# 如 在矩阵的结构中，axis可被设置为0或1，分别表示
# 0：按列计算，1：行计算
predict = tf.argmax(output, 1)

# 保存和恢复模型的方法是使用tf.train.Saver 对象，将训练的结果保存在saver里面
saver = tf.train.Saver()

sess = tf.Session()
# restore载入变量，直接恢复所有变量
saver.restore(sess, tf.train.latest_checkpoint('.'))


def is_my_face(image):
    # 参数：predict预测值
    # feed_dict的作用是给使用placeholder创建出来的tensor赋值。
    # 其实，他的作用更加广泛：feed 使用一个 值临时替换一个 op 的输出结果. 你可以提供 feed 数据作为 run() 调用的参数.
    # feed 只在调用它的方法内有效, 方法结束, feed 就会消失.
    # 其中用[image / 255.0]代替x，1.0代替keep_prob_5。。。。
    res = sess.run(predict, feed_dict={x: [image / 255.0], keep_prob_5: 1.0, keep_prob_75: 1.0})
    if res[0] == 1:
        return True
    else:
        return False

    # 使用dlib自带的frontal_face_detector作为我们的特征提取器


detector = dlib.get_frontal_face_detector()

cam = cv2.VideoCapture(0)

while True:
    _, img = cam.read()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray_image, 1)
    if not len(dets):
        # print('Can`t get face.')
        cv2.imshow('img', img)
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            sys.exit(0)

    for i, d in enumerate(dets):
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0
        face = img[x1:y1, x2:y2]
        # 调整图片的尺寸
        face = cv2.resize(face, (size, size))
        print('Is this my face? %s' % is_my_face(face))

        cv2.rectangle(img, (x2, x1), (y2, y1), (255, 0, 0), 3)
        cv2.imshow('image', img)
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            sys.exit(0)

sess.close()

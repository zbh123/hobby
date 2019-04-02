import cv2
import dlib
import os
import sys
import random

output_dir = './my_faces'
size = 64

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 改变图片的亮度与对比度
def relight(img, light=1, bias=0):
    w = img.shape[1]
    h = img.shape[0]
    #image = []
    for i in range(0,w):
        for j in range(0,h):
            for c in range(3):
                tmp = int(img[j,i,c]*light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j,i,c] = tmp
    return img

#使用dlib自带的frontal_face_detector作为我们的特征提取器，返回的是一个识别出人脸的矩阵（多人的话，是多个矩阵），包含上下左右四个坐标
detector = dlib.get_frontal_face_detector()
# 打开摄像头 参数为输入流，可以为摄像头值为0或视频文件值为文件路径
camera = cv2.VideoCapture(0)

index = 1
while True:
    if (index <= 10000):
        #10000帧以内，index指识别出的图片数
        print('Being processed picture %s' % index)
        # 从摄像头读取照片，返回值为bool型和图片， cap.read()按帧读取视频，success, img是获取camera.read()方法的两个返回值。
        # 其中success是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。img就是每一帧的图像，是个三维矩阵。
        success, img = camera.read()
        # 转为灰度图片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用detector进行人脸检测，dets
        dets = detector(gray_img, 1)
        # enumerate是返回对象的索引和值
        for i, d in enumerate(dets):
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0

            face = img[x1:y1,x2:y2]
            # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
            face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))
            # 重置图片大小
            face = cv2.resize(face, (size,size))
            # 显示图片，名称为image
            cv2.imshow('image', face)
            # 将识别出的图片按index编号输出
            cv2.imwrite(output_dir+'/'+str(index)+'.jpg', face)
            index += 1
        # c得到的是键盘输入的ASCII码，esc键对应的ASCII码是27，即当按esc键是if条件句成立
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break
    else:
        print('Finished!')
        break
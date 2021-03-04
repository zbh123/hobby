# coding=utf-8
# 人脸识别类 - 使用face_recognition模块
import face_recognition
import numpy as np
import cv2


def face_re(face1, face2):
    face_encoding1 = []
    is_face1 = face_recognition.face_encodings(face_recognition.load_image_file(face1))

    if (len(is_face1) <= 0):
        print('未识别人脸1')
        return '未识别人脸1'
    else:
        face_encoding1.append(is_face1[0])
    # print(is_face1[0],len(is_face1[0]))
    # path2 = "img/face_recognition/time1.jpg"  # 模型数据图片目录
    face_encoding2 = []
    is_face2 = face_recognition.face_encodings(face_recognition.load_image_file(face2))
    if (len(is_face2) <= 0):
        print('未识别人脸2')
        return '未识别人脸2'
    else:
        face_encoding2.append(is_face2[0])
    match = face_recognition.compare_faces(np.array(is_face1), np.array(is_face2), tolerance=0.5)

    print(match)
    if match[0]:
        print('图片识别为同一人')
        return True
    else:
        print('图片识别不是一个人')
        return False


def is_face(face_img):
    is_face1 = face_recognition.face_encodings(face_recognition.load_image_file(face_img))

    if (len(is_face1) <= 0):
        print('未识别人脸1')
        return False
    else:
        print('识别人脸')
        return True


def video_rec(video_path):
    cap = cv2.VideoCapture(video_path)
    total_image_name = []
    total_face_encoding = []
    while 1:
        ret, frame = cap.read()
        # 发现在视频帧所有的脸和face_enqcodings
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        # 在这个视频帧中循环遍历每个人脸
        for (top, right, bottom, left), face_encoding in zip(
                face_locations, face_encodings):
            # 画出一个框，框住脸
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # 画出一个带名字的标签，放在框下
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255),
                          cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, 'face', (left + 6, bottom - 6), font, 1.0,
                        (255, 255, 255), 1)
        # 显示结果图像
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# video_rec(r'D:\pyfile\ryven\Ryven\pyside2\这也太可爱了吧.mp4')
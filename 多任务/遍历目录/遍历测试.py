
import os
from collections import deque
#遍历文件夹

#递归遍历
def getAllfile(path, sp=''):
    fileList = os.listdir(path)
    sp += '  '
    for fileName in fileList:
        fileAbsPath = os.path.join(path, fileName)
        if os.path.isdir(fileAbsPath):
            print(sp + '文件夹：' + fileAbsPath)
            getAllfile(fileAbsPath, sp)
        else:
            print(sp + '文件名：' + fileName)



#栈遍历 深度遍历
def stackAllfile(path):
    stack = []
    stack.append(path)
    while len(stack) != 0:
        dirPath = stack.pop()
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            fileAbsPath = os.path.join(dirPath, fileName)
            if os.path.isdir(fileAbsPath):
                stack.append(fileAbsPath)
                print('文件夹：' + fileAbsPath)
            else:
                print('文件名：' + fileName)

#队列遍历，广度遍历
def queAllfile(path):
    queue = deque()
    queue.append(path)
    while len(queue) != 0:
        dirPath = queue.popleft()
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            fileAbsPath = os.path.join(dirPath, fileName)
            if os.path.isdir(fileAbsPath):
                queue.append(fileAbsPath)
                print('文件夹：' + fileAbsPath)
            else:
                print('文件名：' + fileName)

path = 'D:\\ruanjian\matplot_test'
fileList = queAllfile(path)































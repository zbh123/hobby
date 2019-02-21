#递归遍历目录
import os

def getAllDir(path,sp=''):
    fileList = os.listdir(path)
    sp += '   '
    for fileName in fileList:
        fileAbsPath = os.path.join(path,fileName)
        if os.path.isdir(fileAbsPath):
            print(sp + 'dir:' + fileName)
            getAllDir(fileAbsPath,sp)
        else:
            print(sp + 'file name:' +fileName)

getAllDir('D:\\ruanjian')

#深度遍历，栈模拟递归,深度根据栈先进后出的特点，先遍历一个文件的所有目录，再遍历同级其他目录
import os


def getAllDirDE(path):
    stack = []
    stack.append(path)
    #处理栈，当栈为空结束循环
    while len(stack) !=0 :
        #从栈里取数据
        dirPath = stack.pop()
        #目录下所有文件
        fileList = os.listdir(dirPath)
        #处理每个文件，是目录继续压栈
        for fileName in fileList:
            fileAbsPath = os.path.join(dirPath,fileName)
            if os.path.isdir(fileAbsPath):
                print('目录：' + fileAbsPath)
                stack.append(fileAbsPath)
            else:
                print('普通文件：'+ fileAbsPath)

getAllDirDE('D:\\ruanjian')



#队列模拟递归遍历目录，广度遍历


import os
import collections

def getAllDirQU(path):
    queue = collections.deque()
    #进队
    queue.append(path)

    while len(queue) != 0:
        dirPath = queue.popleft()
        #找出所有文件
        filesList = os.listdir(dirPath)

        for fileName in filesList:
            fileAbsPath = os.path.join(dirPath,fileName)
            if os.path.isdir(fileAbsPath):
                print('目录：'+ fileAbsPath)
                queue.append(fileAbsPath)
            else:
                print('普通文件：' + fileAbsPath)

getAllDirQU('D:\\ruanjian')




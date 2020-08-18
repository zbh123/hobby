# python3
# coding='utf-8'

import os
import collections


def static_code(path):
    queue = collections.deque()
    # 进队
    queue.append(path)
    count = 0
    while len(queue) != 0:
        dirPath = queue.popleft()
        # 找出所有文件
        filesList = os.listdir(dirPath)

        for fileName in filesList:
            fileAbsPath = os.path.join(dirPath, fileName)
            if os.path.isdir(fileAbsPath):
                print('目录：' + fileAbsPath)
                queue.append(fileAbsPath)
            else:
                print('普通文件：' + fileAbsPath)
                if 'static' in fileAbsPath:
                    continue
                with open(fileAbsPath, 'r', encoding='gbk', errors='ignore') as fp:
                    content = fp.readlines()
                count += len(content)
                print('统计行数：', count)
    print(count)


# getAllDirQU(r'D:\0RPA\代码统计')
static_code(r'D:\pyfile\github_files\hobby\RPA_web\RPA')

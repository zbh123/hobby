import os
def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #os.listdir的功能是列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):    #判断路径下的是不是文件夹
              _files.extend(list_all_files(path))
           if os.path.isfile(path):    #判断路径下的是不是文件
              _files.append(path)
    return _files

rootdir = 'F:\data'  #要遍历的文件夹
_fs = list_all_files(rootdir)
#将第一阶段的文件遍历出来
_k = filter(lambda x:re.compile(r'stage2.txt').search(x),_fs)


# rootdir = 'F:\data'
# list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
# for i in range(0,len(list)):
#         path = os.path.join(rootdir,list[i])
#        if os.path.isfile(path):

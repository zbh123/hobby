# from ctypes import *
# # tomo = CDLL('./a.so')
# import os
#
# os.system('"C:\Program Files\Microsoft MPI\Bin\mpiexec.exe" -n 10 D:\BaiduYunDownload\Mycode\BPcode\\b')
# import numpy as np
# import struct
# nx = 150
# ny = 460
# f = open('elevation.dat', 'rb')
#     # print(fp.read())
# item = np.zeros((nx, ny))
# for i in range(nx):
#     for j in range(ny):
#         elem = struct.unpack("f", f.read(4))[0]
#         item[i][j] = elem
#         print(elem)
# print(item)



from ctypes import *
# import lsqr
fast = CDLL('fast.so')
fast.run()
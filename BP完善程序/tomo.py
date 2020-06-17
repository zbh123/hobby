'''
调用C语言的so文件，是通过gcc -fPIC -shared func.c -o libfunc.so -lm -w 编译出来的
传参目前浮点型只能传32位的浮点型，其他的C语言不能正确的识别数值
python向C传参时出现OSerror，肯定是传入的参数有问题，检查参数类型，值
mpi执行时，因为整体都是多进程所以每一部分相互独立，暂时未解决
进程池和队列结合，可以解决上述问题
'''

import os
import gc
from multiprocessing import Pool, Process
import numpy as np
import pandas as pd
import struct
import math
from mpi4py import rc
from ctypes import *
import numpy.ctypeslib as npct
import queue
import sys
import argparse
# import lsqr
fast = npct.load_library('fast.so', '.')
# fast = CDLL('fast.so', mode=RTLD_GLOBAL)
lsqr_re = npct.load_library('lsqr_re.so', '.')
shotpath = npct.load_library('shotpath.so', '.')
class tomo():
    def __init__(self):
        self.nshot = 0
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
        self.v0 = 0.0
        self.dv = 0.0
        self.stepsize = 0.0
        self.sign = 1
        self.damp = 0.0
        self.lamda = 0.0
        self.sz = 0.0
        self.omega = 0.0
        self.itmax = 0
        self.niter = 0

        self.readpar()
        # self.buildrealmodel()
        self.buildmodel()


    def readpar(self):
        with open('Tomo3D.par', 'r') as fp:
            readlines = fp.readlines()
        self.nshot = int(readlines[0].strip('\n'))
        self.nx = int(readlines[1].strip('\n'))
        self.ny = int(readlines[2].strip('\n'))
        self.nz = int(readlines[3].strip('\n'))
        self.dx = float(readlines[4].strip('\n'))
        self.dy = float(readlines[5].strip('\n'))
        self.dz = float(readlines[6].strip('\n'))
        self.v0 = float(readlines[7].strip('\n'))
        self.dv = float(readlines[8].strip('\n'))
        self.stepsize = float(readlines[9].strip('\n'))
        self.sign = 1
        self.damp = float(readlines[10].strip('\n'))
        self.lamda = float(readlines[11].strip('\n'))
        self.sz = float(readlines[12].strip('\n'))
        self.omega = float(readlines[13].strip('\n'))
        self.itmax = int(readlines[14].strip('\n'))
        self.niter = int(readlines[15].strip('\n'))
        with open('count.txt','r') as fp:
            self.neachshot = fp.readlines()
        if len(self.neachshot) < self.nshot:
            print('number of shot error')
            os._exit(0)
        self.nray = 0
        for i in self.neachshot:
            self.nray += int(i)

    def read_3d(self, file, nx, ny, nz):
        f = open(file, 'rb')
        item = np.zeros((nx, ny, nz), dtype=np.float32)
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    data = f.read(4)
                    elem = struct.unpack("f", data)[0]
                    item[i][j][k] = elem
        return item

    def read_2d(self, file, nx, ny):
        f = open(file, 'rb')
        item = np.zeros((nx, ny))
        for i in range(nx):
            for j in range(ny):
                data = f.read(4)
                elem = struct.unpack("f", data)[0]
                item[i][j] = elem
        return item

    def buildrealmodel(self):
        self.ele = self.read_2d('elevation.dat', self.nx, self.ny)

        realvel3D = self.read_3d('velmodel_bp.dat', self.nx, self.ny, self.nz)
        realeps = self.read_3d('epsilon_bp.dat', self.nx, self.ny, self.nz)
        realdelta = self.read_3d('delta_bp.dat', self.nx, self.ny, self.nz)
        self.realvel = np.zeros(self.nx * self.ny * self.nz)
        self.realvx = np.zeros(self.nx * self.ny * self.nz)
        self.realq = np.zeros(self.nx * self.ny * self.nz)
        print("read file OK")
        print(self.ele[0][0])
        count = 0
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    self.realvel[count] = (1 / realvel3D[i][j][k]) ** 2
                    self.realq[count] = (1 + 2 * realdelta[i][j][k]) / (1 + 2 * realeps[i][j][k])
                    self.realvx[count] = self.realvel[count] / (1 + 2 * realeps[i][j][k])
                    count += 1

    def buildmodel(self):
        self.ele = self.read_2d('elevation.dat', self.nx, self.ny)
        self.vel3D = np.zeros((self.nx, self.ny, self.nz), dtype=np.float32)
        self.eps = np.zeros((self.nx, self.ny, self.nz), dtype=np.float32)
        self.delta = np.zeros((self.nx, self.ny, self.nz), dtype=np.float32)
        self.vel = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        self.vx = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        self.q = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        self.vel3D_1 = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        self.eps_1 = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        self.delta_1 = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        count = 0
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    if k < int(self.ele[i][j]/self.dz):
                        self.vel3D[i][j][k] = 340
                        self.eps[i][j][k] = 0.0001
                        self.delta[i][j][k] = 0.0001
                    else:
                        self.vel3D[i][j][k] = self.v0 + k*self.dv
                        self.eps[i][j][k] = self.vel3D[i][j][k]/15000
                        self.delta[i][j][k] = self.vel3D[i][j][k]/30000

                    self.vel[count] = (1 / self.vel3D[i][j][k]) ** 2
                    self.q[count] = (1 + 2 * self.delta[i][j][k]) / (1 + 2 * self.eps[i][j][k])
                    self.vx[count] = self.vel[count] / (1 + 2 * self.eps[i][j][k])

                    self.vel3D_1[count] = self.vel3D[i][j][k]
                    self.eps_1[count] = self.eps[i][j][k]
                    self.delta_1[count] = self.delta[i][j][k]
                    count += 1
        print("build model OK")
        self.shotxyz = np.zeros((self.nshot, 3))
        self.recxyz = np.zeros((self.nray, 3))
        with open('shot.txt','r') as fp:
            shot_location = fp.readlines()
        if len(shot_location) >= self.nshot:
            for i, line in enumerate(shot_location):
                line = line.strip('\n').strip().split()
                tempx = int(float(line[0])/self.dx + 0.5)
                tempy = int(float(line[1])/self.dy + 0.5)
                # print(tempx, tempy)
                self.shotxyz[i][0] = float(line[0])
                self.shotxyz[i][1] = float(line[1])
                self.shotxyz[i][2] = self.ele[tempx][tempy]
                # print(self.shotxyz[i][0], self.shotxyz[i][1], self.shotxyz[i][2], type(self.shotxyz[i][0]))

        with open('rec.txt','r') as fp:
            rec_location = fp.readlines()
        if len(rec_location) >= self.nray:
            for i, line in enumerate(rec_location):
                line = line.strip('\n').strip().split()
                tempx = int(float(line[0])/self.dx + 0.5)
                tempy = int(float(line[1])/self.dy + 0.5)
                # print(tempx, tempy)
                self.recxyz[i][0] = line[0]
                self.recxyz[i][1] = line[1]
                self.recxyz[i][2] = self.ele[tempx][tempy]

    def calculate_time(self, iter, ishot, flag, plane, stepsize, neachshot, rank):
        gc.enable()
        print(rank)
        ifree = int(2 * math.sqrt((self.nx * self.dx) ** 2 + (self.ny * self.dy) ** 2 + (self.nz * self.dz) ** 2))
        realtime = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        tmp_time = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)
        time = np.zeros(self.nx * self.ny * self.nz, dtype=np.float32)

        fast.fastmarch_init.argtypes = [c_int, c_int, c_int]
        fast.fastmarch.argtypes = [npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.int, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.bool, ndim=1, flags="C_CONTIGUOUS"),
                                   c_int, c_int, c_int, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_int, c_int, c_int, c_int]

        fast.fastmarch_init(c_int(self.nx), c_int(self.ny), c_int(self.nz))
        fast.fastmarch(time, tmp_time, self.vx, self.vel, self.q, flag, plane, c_int(self.nx), c_int(self.ny), c_int(self.nz), c_float(0.), c_float(0.), c_float(0.), c_float(self.dx), c_float(self.dy), c_float(self.dz),
                 c_float(float(self.shotxyz[ishot][0])), c_float(float(self.shotxyz[ishot][1])), c_float(float(self.shotxyz[ishot][2])), c_int(1), c_int(1), c_int(1), c_int(1))
        fast.fastmarch_close()

        # fast.run.argtypes = [c_int, c_int, c_int, npct.ndpointer(dtype=np.float, ndim=1, flags="C_CONTIGUOUS"), npct.ndpointer(dtype=np.float, ndim=1, flags="C_CONTIGUOUS"),
        #                      npct.ndpointer(dtype=np.float, ndim=1, flags="C_CONTIGUOUS"), npct.ndpointer(dtype=np.float, ndim=1, flags="C_CONTIGUOUS"),npct.ndpointer(dtype=np.float, ndim=1, flags="C_CONTIGUOUS"),
        #                      npct.ndpointer(dtype=np.int, ndim=1, flags="C_CONTIGUOUS"), npct.ndpointer(dtype=np.bool, ndim=1, flags="C_CONTIGUOUS"), c_float,
        #                      c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_int, c_int, c_int, c_int]
        # # fast.run.restype = c_float
        # # print(type(c_float(dx)), type(c_float(float(shotxyz[ishot][0]))),type(tmp_vel),type(tmp_vx),type(tmp_q),type(tmp_plane),type(tmp_flag),)
        # # print(time, tmp_time, tmp_vx, tmp_vel, tmp_q, tmp_flag, tmp_plane)
        # print(time, tmp_time, vx, vel, q, flag, plane,)
        # fast.run(c_int(nx), c_int(ny), c_int(nz), time, tmp_time, vx, vel, q, flag, plane,
        #                 c_float(0.), c_float(0.), c_float(0.), c_float(dx), c_float(dy), c_float(dz),
        #          c_float(float(shotxyz[ishot][0])), c_float(float(shotxyz[ishot][1])),
        #                 c_float(float(shotxyz[ishot][2])), c_int(1), c_int(1), c_int(1), c_int(1))
        # fast.run(c_int(nx), c_int(ny), c_int(nz), time, tmp_time, tmp_vx, tmp_vel, tmp_q, tmp_flag, tmp_plane,
        #                 c_float(0.), c_float(0.), c_float(0.), c_float(dx), c_float(dy), c_float(dz),
        #          c_float(float(shotxyz[ishot][0])), c_float(float(shotxyz[ishot][1])),
        #                 c_float(float(shotxyz[ishot][2])), c_int(1), c_int(1), c_int(1), c_int(1))

        # fast.run(c_int(self.nx), c_int(self.ny), c_int(self.nz), (c_float * len(time))(time), (c_float * len(tmp_time))(tmp_time),
        #                (c_float * len(self.vx))(self.vx), (c_float * len(self.vel))(self.vel), (c_float * len(self.q))(self.q),
        #          (c_int * len(flag))(flag), (c_bool * len(plane))(plane),  c_float(0.), c_float(0.), c_float(0.),
        #          c_float(self.dx), c_float(self.dy), c_float(self.dz), c_float(float(self.shotxyz[ishot][0])), c_float(float(self.shotxyz[ishot][1])),
        #          c_float(float(self.shotxyz[ishot][2])), c_int(1), c_int(1), c_int(1), c_int(1))
        # fast.run((c_float * len(realtime))(*realtime.tolist()), (c_float * len(tmp_time))(*tmp_time.tolist),
        #                (c_float * len(realvx))(*realvx.tolist()), (c_float * len(realvel))(*realvel.tolist()), (c_float * len(realq))(*realq.tolist()),
        #                flag, plane, nx, ny, nz, 0, 0, 0, dx, dy, dz, float(shotxyz[ishot][0]),
        #                float(shotxyz[ishot][0][1]), float(shotxyz[ishot][0][2]), 1, 1, 1, 1)
        print("VTIFMM of %s shot has been calculated(ID:%d, Ite:%d)\n" % (ishot + 1, ishot + 1, iter + 1))
        count = 0
        # print(time, tmp_time)
        time3D = np.zeros((self.nx, self.ny, self.nz))
        realtime3D = np.zeros((self.nx, self.ny, self.nz))
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    time3D[i][j][k] = time[count]
                    realtime3D[i][j][k] = realtime[count]
                    count += 1
        gx = np.zeros((self.nx, self.ny, self.nz))
        gy = np.zeros((self.nx, self.ny, self.nz))
        gz = np.zeros((self.nx, self.ny, self.nz))
        self.laplace(self.nx, self.ny, self.nz, time3D, self.dx, self.dy, self.dz, gx, gy, gz)
        count = 0
        gradientArray = np.zeros((3 * self.nx * self.ny * self.nz), dtype=np.float32)
        for k in range(self.nz):
            for j in range(self.ny):
                for i in range(self.nx):
                    gradientArray[count] = gx[i][j][k]
                    count += 1
        for k in range(self.nz):
            for j in range(self.ny):
                for i in range(self.nx):
                    gradientArray[count] = gy[i][j][k]
                    count += 1
        for k in range(self.nz):
            for j in range(self.ny):
                for i in range(self.nx):
                    gradientArray[count] = gz[i][j][k]
                    count += 1
        js = self.sum(neachshot, ishot)
        dt = realtime3D[int(self.recxyz[js][0] / self.dx)][int(self.recxyz[js][1] / self.dy)][int(self.recxyz[js][2] / self.dz)] - \
             time3D[int(self.recxyz[js][0] / self.dx)][int(self.recxyz[js][1] / self.dy)][int(self.recxyz[js][2] / self.dz)]
        dt1 = dt
        shotpoint = np.zeros((3), dtype=np.float32)
        recpoint = np.zeros((3), dtype=np.float32)

        shotpoint[0] = self.shotxyz[ishot][0] + self.dx
        shotpoint[1] = self.shotxyz[ishot][1] + self.dy
        shotpoint[2] = self.shotxyz[ishot][2] + self.dz
        recpoint[0] = self.recxyz[js][0] + self.dx
        recpoint[1] = self.recxyz[js][1] + self.dy
        recpoint[2] = self.recxyz[js][2] + self.dz
        gArray1 = np.zeros((ifree), np.int)
        gArray2 = np.zeros((ifree), np.int)
        freArray1 = np.zeros((ifree), np.float32)
        freArray2 = np.zeros((ifree), np.float32)

        cal1 = 0
        cal2 = 0
        shotpath.shortestpath.argtypes = [npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                    c_float,
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                    c_int, c_int, c_int, c_float, c_float, c_float, c_int, c_int, c_float, c_float,
                                   npct.ndpointer(dtype=np.int, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),c_int,
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                   npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS")]
        siren1 = shotpath.shortestpath(recpoint, shotpoint, c_float(stepsize), gradientArray, c_int(self.nx), c_int(self.ny), c_int(self.nz), c_float(self.dx), c_float(self.dy), c_float(self.dz),
                                   c_int(rank), c_int(self.nmax), c_float(self.countdt), c_float(dt), gArray1, freArray1, c_int(cal1), self.eps_1, self.delta_1, self.vel3D_1)
        # siren1 = self.shortestpath1(recpoint, shotpoint, stepsize, gradientArray, self.nx, self.ny, self.nz, self.dx,
        #                            self.dy, self.dz, dt, gArray1, freArray1, cal1, fdelta, frechet)

        for js in range(self.sum(neachshot, ishot) + 1, self.sum(neachshot, ishot) + int(neachshot[ishot])):
            dt = realtime3D[int(self.recxyz[js][0] / self.dx)][int(self.recxyz[js][1] / self.dy)][int(self.recxyz[js][2] / self.dz)] - \
                 time3D[int(self.recxyz[js][0] / self.dx)][int(self.recxyz[js][1] / self.dy)][int(self.recxyz[js][2] / self.dz)]
            dt2 = dt
            shotpoint = np.zeros((3), np.float32)
            recpoint = np.zeros((3), np.float32)
            shotpoint[0] = self.shotxyz[ishot][0] + self.dx
            shotpoint[1] = self.shotxyz[ishot][1] + self.dy
            shotpoint[2] = self.shotxyz[ishot][2] + self.dz
            recpoint[0] = self.recxyz[js][0] + self.dx
            recpoint[1] = self.recxyz[js][1] + self.dy
            recpoint[2] = self.recxyz[js][2] + self.dz
            # siren2 = self.shortestpath1(recpoint, shotpoint, stepsize, gradientArray, self.nx, self.ny, self.nz, self.dx, self.dy, self.dz,
            #                       dt, gArray2, freArray2, cal2, fdelta, frechet)

            siren2 = shotpath.shortestpath(recpoint, shotpoint, c_float(stepsize), gradientArray, c_int(self.nx), c_int(self.ny),
                                  c_int(self.nz), c_float(self.dx), c_float(self.dy), c_float(self.dz),
                                  c_int(rank), c_int(self.nmax), c_float(self.countdt), c_float(dt), gArray2, freArray2,
                                  c_int(cal2), self.eps_1, self.delta_1, self.vel3D_1)
            self.appvel(js, self.recxyz, dt1, dt2, gArray1, freArray1, cal1, gArray2, freArray2, cal2, rank)

        print("Raytrace of %d shot has been calculated(ID:%d, Ite:%d)\n" % (ishot + 1, rank+1, iter + 1))
        del realtime, tmp_time, shotpoint, recpoint, time, gx, gy, gz, gradientArray, gArray1, gArray2, freArray1, freArray2, \
            dt, ifree, time3D, realtime3D, count
        gc.collect()


    def laplace(self, nx, ny, nz, time3D, dx, dy, dz, gx, gy, gz):
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if i == 0:
                        gx[i][j][k] = (time3D[i + 1][j][k] - time3D[i][j][k]) / dx
                    elif i == nx - 1:
                        gx[i][j][k] = (time3D[i][j][k] - time3D[i - 1][j][k]) / dx
                    else:
                        gx[i][j][k] = (time3D[i + 1][j][k] - time3D[i - 1][j][k]) / (2 * dx)
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if j == 0:
                        gy[i][j][k] = (time3D[i][j + 1][k] - time3D[i][j][k]) / dy
                    elif j == ny - 1:
                        gy[i][j][k] = (time3D[i][j][k] - time3D[i][j - 1][k]) / dy
                    else:
                        gy[i][j][k] = (time3D[i][j + 1][k] - time3D[i][j - 1][k]) / (2 * dy)
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if k == 0:
                        gz[i][j][k] = (time3D[i][j][k + 1] - time3D[i][j][k]) / dz
                    elif k == nz - 1:
                        gz[i][j][k] = (time3D[i][j][k] - time3D[i][j][k - 1]) / dz
                    else:
                        gz[i][j][k] = (time3D[i][j][k + 1] - time3D[i][j][k - 1]) / (2 * dz)

    def mindex3(self, x, y, z, sizx, sizy):
        return int(z * sizy * sizx + y * sizx + x)

    def interpgrad3d(self, Ireturn, grad, Isize, point, dx, dy, dz):
        perc = np.zeros((8))
        index = np.zeros((8), dtype=np.int)
        fTlocalx = math.floor(point[0] / dx)
        fTlocaly = math.floor(point[1] / dy)
        fTlocalz = math.floor(point[2] / dz)
        xBase0 = int(fTlocalx)
        yBase0 = int(fTlocaly)
        zBase0 = int(fTlocalz)
        xBase1 = xBase0 + 1
        yBase1 = yBase0 + 1
        zBase1 = zBase0 + 1
        xCom = point[0] - fTlocalx * dx
        yCom = point[1] - fTlocaly * dy
        zCom = point[2] - fTlocalz * dz
        xComi = dx - xCom
        yComi = dy - yCom
        zComi = dz - zCom
        perc[0] = xComi * yComi
        perc[1] = perc[0] * zCom
        perc[0] = perc[0] * zComi
        perc[2] = xComi * yCom
        perc[3] = perc[2] * zCom
        perc[2] = perc[2] * zComi
        perc[4] = xCom * yComi
        perc[5] = perc[4] * zCom
        perc[4] = perc[4] * zComi
        perc[6] = xCom * yCom
        perc[7] = perc[6] * zCom
        perc[6] = perc[6] * zComi
        if xBase0 < 0:
            xBase0 = 0
            if xBase1 < 0:
                xBase1 = 0
        if yBase0 < 0:
            yBase0 = 0
            if yBase1 < 0:
                yBase1 = 0
        if zBase0 < 0:
            zBase0 = 0
            if zBase1 < 0:
                zBase1 = 0
        if xBase1 > (Isize[0] - 1):
            xBase1 = (Isize[0] - 1)
            if xBase0 > Isize[0] - 1:
                xBase0 = Isize[0] - 1
        if yBase1 > (Isize[1] - 1):
            yBase1 = (Isize[1] - 1)
            if yBase0 > Isize[1] - 1:
                yBase0 = Isize[1] - 1
        if zBase1 > (Isize[2] - 1):
            zBase1 = (Isize[2] - 1)
            if zBase0 > Isize[2] - 1:
                zBase0 = Isize[2] - 1
        index[0] = self.mindex3(xBase0, yBase0, zBase0, Isize[0], Isize[1])
        index[1] = self.mindex3(xBase0, yBase0, zBase1, Isize[0], Isize[1])
        index[2] = self.mindex3(xBase0, yBase1, zBase0, Isize[0], Isize[1])
        index[3] = self.mindex3(xBase0, yBase1, zBase1, Isize[0], Isize[1])
        index[4] = self.mindex3(xBase1, yBase0, zBase0, Isize[0], Isize[1])
        index[5] = self.mindex3(xBase1, yBase0, zBase1, Isize[0], Isize[1])
        index[6] = self.mindex3(xBase1, yBase1, zBase0, Isize[0], Isize[1])
        index[7] = self.mindex3(xBase1, yBase1, zBase1, Isize[0], Isize[1])
        f0 = Isize[0] * Isize[1] * Isize[2]
        f1 = f0 + f0
        # print(index[0],index[1],index[2],index[3],index[4],index[5],index[6],index[7])
        temp = grad[index[0]] * perc[0] + grad[index[1]] * perc[1] + grad[index[2]] * perc[2] + grad[index[3]] * \
               perc[3]
        Ireturn[0] = temp + grad[index[4]] * perc[4] + grad[index[5]] * perc[5] + grad[index[6]] * perc[6] + grad[
            index[7]] * perc[7]
        temp = grad[index[0] + f0] * perc[0] + grad[index[1] + f0] * perc[1] + grad[index[2] + f0] * perc[2] + grad[
            index[3] + f0] * perc[3]
        Ireturn[1] = temp + grad[index[4] + f0] * perc[4] + grad[index[5] + f0] * perc[5] + grad[index[6] + f0] * \
                     perc[6] + grad[index[7] + f0] * perc[7]
        temp = grad[index[0] + f1] * perc[0] + grad[index[1] + f1] * perc[1] + grad[index[2] + f1] * perc[2] + grad[
            index[3] + f1] * perc[3]
        Ireturn[2] = temp + grad[index[4] + f1] * perc[4] + grad[index[5] + f1] * perc[5] + grad[index[6] + f1] * \
                     perc[6] + grad[index[7] + f1] * perc[7]

    def norm3(self, a):
        return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)

    def checkBounds3d(self, point, Isize, dx, dy, dz):
        if point[0] < 0 or point[1] < 0 or point[2] < 0 or point[0] > (Isize[0] - 1) * dx or point[1] > (
                Isize[1] - 1) * dy or point[2] > (Isize[2] - 1) * dz:
            return False
        return True

    def RK4STEP_3D(self, gradientArray, gradientArraySize, startpoint1, nextpoint, stepsize, dx, dy, dz):
        k1 = np.zeros((3))
        k2 = np.zeros((3))
        k3 = np.zeros((3))
        k4 = np.zeros((3))
        tmpPoint = np.zeros((3))

        self.interpgrad3d(k1, gradientArray, gradientArraySize, startpoint1, dx, dy, dz)
        tempnorm = self.norm3(k1)
        k1[0] = k1[0] * stepsize / tempnorm
        k1[1] = k1[1] * stepsize / tempnorm
        k1[2] = k1[2] * stepsize / tempnorm

        tmpPoint[0] = startpoint1[0] - k1[0] * 0.5
        tmpPoint[1] = startpoint1[1] - k1[1] * 0.5
        tmpPoint[2] = startpoint1[2] - k1[2] * 0.5
        if not self.checkBounds3d(tmpPoint, gradientArraySize, dx, dy, dz):
            return False

        self.interpgrad3d(k2, gradientArray, gradientArraySize, tmpPoint, dx, dy, dz)
        tempnorm = self.norm3(k2)
        k2[0] = k2[0] * stepsize / tempnorm
        k2[1] = k2[1] * stepsize / tempnorm
        k2[2] = k2[2] * stepsize / tempnorm

        tmpPoint[0] = startpoint1[0] - k2[0] * 0.5
        tmpPoint[1] = startpoint1[1] - k2[1] * 0.5
        tmpPoint[2] = startpoint1[2] - k2[2] * 0.5
        if not self.checkBounds3d(tmpPoint, gradientArraySize, dx, dy, dz):
            return False

        self.interpgrad3d(k3, gradientArray, gradientArraySize, tmpPoint, dx, dy, dz)
        tempnorm = self.norm3(k3)
        k3[0] = k3[0] * stepsize / tempnorm
        k3[1] = k3[1] * stepsize / tempnorm
        k3[2] = k3[2] * stepsize / tempnorm

        tmpPoint[0] = startpoint1[0] - k3[0] * 0.5
        tmpPoint[1] = startpoint1[1] - k3[1] * 0.5
        tmpPoint[2] = startpoint1[2] - k3[2] * 0.5
        if not self.checkBounds3d(tmpPoint, gradientArraySize, dx, dy, dz):
            return False

        self.interpgrad3d(k4, gradientArray, gradientArraySize, tmpPoint, dx, dy, dz)
        tempnorm = self.norm3(k4)
        k4[0] = k4[0] * stepsize / tempnorm
        k4[1] = k4[1] * stepsize / tempnorm
        k4[2] = k4[2] * stepsize / tempnorm

        nextpoint[0] = startpoint1[0] - (k1[0] + k2[0] * 2.0 + k3[0] * 2.0 + k4[0]) / 6.0
        nextpoint[1] = startpoint1[1] - (k1[1] + k2[1] * 2.0 + k3[1] * 2.0 + k4[1]) / 6.0
        nextpoint[2] = startpoint1[2] - (k1[2] + k2[2] * 2.0 + k3[2] * 2.0 + k4[2]) / 6.0
        if not self.checkBounds3d(tmpPoint, gradientArraySize, dx, dy, dz):
            return False
        return True

    def rk4(self, startpoint, gradientArray, stepsize, nx, ny, nz, dx, dy, dz, nextpoint):
        gradientArraySize = np.zeros((3), np.int)
        startpoint1 = np.zeros((3))
        gradientArraySize[0] = nx
        gradientArraySize[1] = ny
        gradientArraySize[2] = nz
        startpoint1[0] = startpoint[0] - dx
        startpoint1[1] = startpoint[1] - dy
        startpoint1[2] = startpoint[2] - dz
        if self.RK4STEP_3D(gradientArray, gradientArraySize, startpoint1, nextpoint, stepsize, dx, dy, dz):
            nextpoint[0] = nextpoint[0] + dx
            nextpoint[1] = nextpoint[1] + dy
            nextpoint[2] = nextpoint[2] + dz
        else:
            nextpoint[0] = 0.0
            nextpoint[1] = 0.0
            nextpoint[2] = 0.0

    def shortestpath1(self, startpoint, sourcepoint, stepsize, gradientArray, nx, ny, nz, dx, dy, dz, dt,
                     gArraym, freArraym, calm, fdelta, frechet):
        l = 0.0
        nextpoint = np.zeros((3))
        ifree = int(2 * math.sqrt((nx * dx) ** 2 + (ny * dy) ** 2 + (nz * dz) ** 2) / stepsize)
        shortestLine = np.zeros((ifree, 3))
        # theta = np.zeros((ifree))
        theta = []
        gArray = np.zeros((ifree))
        # freArray = np.zeros((ifree))
        freArray = []
        self.rk4(startpoint, gradientArray, stepsize, nx, ny, nz, dx, dy, dz, nextpoint)
        shortestLine[0][0] = startpoint[0]
        shortestLine[0][1] = startpoint[1]
        shortestLine[0][2] = startpoint[2]
        sfregridx = 0
        sfregridy = 0
        sfregridz = 0
        nfregridx = 0
        nfregridy = 0
        nfregridz = 0
        cal = 0
        count = 0
        flag = 0
        siren = 0
        while math.fabs(nextpoint[0]) > 1e-6:
            sfregridx = int((startpoint[0] - dx) / dx)
            sfregridy = int((startpoint[1] - dy) / dy)
            sfregridz = int((startpoint[2] - dz) / dz)
            nfregridx = int((nextpoint[0] - dx) / dx)
            nfregridy = int((nextpoint[1] - dy) / dy)
            nfregridz = int((nextpoint[2] - dz) / dz)
            if sfregridx == nfregridx and sfregridy == nfregridy and sfregridz == nfregridz:
                l += math.sqrt((float(startpoint[0]) - float(nextpoint[0])) ** 2 + (float(startpoint[1]) - float(nextpoint[1])) ** 2 + (
                            float(startpoint[2]) - float(nextpoint[2])) ** 2)
                # print("l is", l)
                theta.append(math.atan((float(startpoint[2]) - float(nextpoint[2])) / l))
            else:
                l = l + math.sqrt((float(startpoint[0]) - dx - (float(startpoint[0]) - dx + float(nextpoint[0]) - dx) / 2) ** 2 + (
                            float(startpoint[1]) - dy - (float(startpoint[1]) - dy + float(nextpoint[1]) - dy) / 2) ** 2 + (
                                              float(startpoint[2]) - dz - (float(startpoint[2]) - dz + float(nextpoint[2]) - dz) / 2) ** 2)
                igrid = sfregridz * nx * ny + sfregridy * nx + sfregridx
                gArray[cal] = igrid
                freArray.append(l)
                cal += 1
            distanceToEnd = math.sqrt((float(sourcepoint[0]) - float(nextpoint[0])) ** 2 + (float(sourcepoint[1]) - float(nextpoint[1])) ** 2 + (
                        float(sourcepoint[2]) - float(nextpoint[2])) ** 2)
            if distanceToEnd < stepsize:
                break
            if count > 10:
                movement = math.sqrt((float(nextpoint[0]) - float(shortestLine[count - 10][0])) ** 2 + (
                            float(nextpoint[1]) - float(shortestLine[count - 10][1])) ** 2 + (
                                                 float(nextpoint[2]) - float(shortestLine[count - 10][2])) ** 2)
            else:
                movement = stepsize
            if movement < stepsize:
                break
            count += 1
            shortestLine[count][0] = nextpoint[0]
            shortestLine[count][1] = nextpoint[1]
            shortestLine[count][2] = nextpoint[2]
            startpoint[0] = nextpoint[0]
            startpoint[1] = nextpoint[1]
            startpoint[2] = nextpoint[2]
            self.rk4(startpoint, gradientArray, stepsize, nx, ny, nz, dx, dy, dz, nextpoint)
            if count == ifree - 1:
                flag = 1
                break
        if count != 0:
            if sfregridx == nfregridx and sfregridy == nfregridy and sfregridz == nfregridz:
                igrid = sfregridz * nx * ny + sfregridy * nx + sfregridx
                gArray[cal] = igrid
                freArray.append(l)
                cal += 1
            else:
                igrid = nfregridz * nx * ny + nfregridy * nx + nfregridx
                gArray[cal] = igrid
                freArray.append(l)
                cal += 1
        if flag == 0 and cal != 0:
            calm += cal
            for i in range(cal):
                # print(freArray[i])
                if np.fabs(freArray[i]) > 1e-6:
                    gArraym[i] = gArray[i]
                    freArraym[i] = freArray[i]
                    frechet.write("%f %f\n" % (gArray[i], freArray[i]))
                    self.nmax += 1
                    siren = 1
            if siren == 1:
                frechet.write('%d %f' % (-1, 0.))
                self.countdt += 1
                fdelta.write('%f\n' % dt)
        return siren

    def appvel(self, js, recxyz, dt1, dt2, gArray1, freArray1, cal1, gArray2, freArray2, cal2, rank):
        fdeltaapp = open('fdeltaapp%d.dat' % rank, 'a')
        frechetapp = open('frechetapp%d.dat' % rank, 'a')
        siren = 0
        dt = dt1 - dt2
        dx = math.sqrt((float(recxyz[js][0]) - float(recxyz[js - 1][0])) ** 2 + (float(recxyz[js][1]) - float(recxyz[js - 1][1])) ** 2 + (
                    float(recxyz[js][2]) - float(recxyz[js - 1][2])) ** 2)
        if cal1 != 0 and cal2 != 0:
            for i in range(cal1):
                if math.fabs(freArray1[i]) > 1e-6:
                    frechetapp.write('%d %f' % (gArray1[i], freArray1[i] / dx))
                    self.nmaxapp += 1
                    siren = 1
            for i in range(cal2):
                if math.fabs(freArray2[i]) > 1e-6:
                    frechetapp.write('%d %f' % (gArray2[i], freArray2[i] / dx))
                    self.nmaxapp += 1
                    siren = 1
            if siren == 1:
                frechetapp.write('%d %f\n' % (-1, 0.0))
                self.countdtapp += 1
                fdeltaapp.write('%f\n' % dt / dx)
        fdeltaapp.close()
        frechetapp.close()

    def sum(self, neachshot, ishot):
        s = 0
        for i in range(ishot):
            s += int(neachshot[i].strip('\n'))
        return s

    def start(self):
        from mpi4py import MPI
        MPI.Init()
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        # print(rank)
        if len(sys.argv) > 1:
            npool = sys.argv[1]
        else:
            npool = 1
        self.ds = np.zeros((self.nx*self.ny*self.nz), np.float32)
        self.sel3D = np.zeros((self.nx*self.ny*self.nz), np.float32)
        # self.dens = np.zeros((self.nx*self.ny*self.nz), np.float32)
        flag = np.zeros((self.nx*self.ny*self.nz), np.int)
        initdelta = 0
        plane = np.array([False, False, False], dtype=np.bool)
        if rank == 0:
            print("==========The 3D VTI First Break Tomo Start==========\n")
        for iter in range(self.niter):
            if iter > 0:
                self.velupdate = self.read_3d('velupdate.dat', self.nx, self.ny, self.nz)
                self.eps = self.read_3d('velupdate.dat', self.nx, self.ny, self.nz)
                self.delta = self.read_3d('velupdate.dat', self.nx, self.ny, self.nz)

                count = 0
                for i in range(self.nx):
                    for j in range(self.ny):
                        for k in range(self.nz):
                            self.vel3D[count] = (1 / (self.velupdate[i][j][k])) ** 2
                            self.q[count] = (1 + 2 * self.delta[i][j][k]) / (1 + 2 * self.eps[i][j][k])
                            self.vx[count] = self.vel3D[count] / (1 + 2 * self.eps[i][j][k])

                            self.vel3D_1[count] = self.vel3D[i][j][k]
                            self.eps_1[count] = self.eps[i][j][k]
                            self.delta_1[count] = self.delta[i][j][k]
                            count += 1

            if rank == 0:
                print("**************The %d ITERATION**************"%(iter+1))

            self.countdt = 10
            self.countdtapp = 10
            sumnmax = 10
            sumcountdt = 10
            self.nmax = 10
            self.nmaxapp = 10
            sumnmaxapp =10
            sumcountdtapp = 10
            sumdelta = 0
            p = Pool(processes=npool)
            step = npool
            q = queue.Queue()
            for ishot in range(0, self.nshot, size):
                # self.calculate_time(iter, ishot, flag, plane, self.stepsize, self.neachshot, rank)
                # print("Raytrace of %d shot has been calculated(ID:%d, Ite:%d)\n" % (ishot + 1, ishot+1, iter + 1))
                for i in range(step):
                    q.put(i)
                p.apply_async(self.calculate_time, (iter, ishot, flag, plane, self.stepsize, self.neachshot, q.get()))
                    # p = Process(target=self.calculate_time, args=(iter, ishot, flag, plane, self.stepsize, self.neachshot, i))

                # p.apply_async(self.calculate_time, (iter, ishot, flag, plane, self.stepsize, self.neachshot, rank)

            p.close()
            p.join()

            tempnmax = []
            tempcountdt = []
            tempnmaxapp = []
            tempcountdtapp = []
            if rank!=0:
                comm.send(self.nmax, dest=0, tag=1)
                comm.send(self.countdt, dest=0, tag=2)
                comm.send(self.nmaxapp, dest=0, tag=3)
                comm.send(self.countdtapp, dest=0, tag=4)
            if rank == 0:
                tempnmax.append(self.nmax)
                tempcountdt.append(self.nmax)
                tempnmaxapp.append(self.nmax)
                tempcountdtapp.append(self.nmax)

                for i in range(1, size):
                    tempnmax.append(comm.recv(source=i, tag=1))
                    tempcountdt.append(comm.recv(source=i, tag=2))
                    tempnmaxapp.append(comm.recv(source=i, tag=3))
                    tempcountdtapp.append(comm.recv(source=i, tag=4))

                for i in range(size):
                    sumnmax += tempnmax[i]
                    sumcountdt += tempcountdt[i]
                    sumnmaxapp += tempnmaxapp[i]
                    sumcountdtapp += tempcountdtapp[i]
                # sfrenum = np.zeros((sumnmax + sumcountdt), np.int)
                # sfrelen = np.zeros((sumnmax + sumcountdt))
                # sdeltat = np.zeros((sumcountdt))
                # sfrenumapp = np.zeros((sumnmaxapp + sumcountdtapp), np.int)
                # sfrelenapp = np.zeros((sumnmaxapp + sumcountdtapp))
                # sdeltatapp = np.zeros((sumcountdtapp))
            # if rank==1:
                sfrenum = []
                sfrelen = []
                sdeltat = []
                sfrenumapp = []
                sfrelenapp = []
                sdeltatapp = []
                frechet_file = []
                fdelta_file = []
                frechetapp_file = []
                fdeltaapp_file = []
                for i in range(size):
                    with open("frechet%d.dat"%i, 'rb') as fp:
                        for line in fp.readlines():
                            frechet_file.append(line)
                    with open("frechetapp%d.dat"%i, 'rb') as fp:
                        for line in fp.readlines():
                            frechetapp_file.append(line)
                    with open("fdelta%d.dat"%i, 'rb') as fp:
                        for line in fp.readlines():
                            fdelta_file.append(line)
                    with open("fdeltaapp%d.dat"%i, 'rb') as fp:
                        for line in fp.readlines():
                            fdeltaapp_file.append(line)
                    os.remove("frechet%d.dat"%i)
                    os.remove("frechetapp%d.dat"%i)
                    os.remove("fdelta%d.dat"%i)
                    os.remove("fdeltaapp%d.dat"%i)
                for line in frechet_file:
                    line = line.strip('\n').split()
                    sfrenum.append(int(line[0]))
                    sfrelen.append(float(line[1]))
                for line in fdelta_file:
                    line = line.strip('\n')
                    sdeltat.append(float(line[1]))
                for line in frechet_file:
                    line = line.strip('\n').split()
                    sfrenumapp.append(int(line[0]))
                    sfrelenapp.append(float(line[1]))
                for line in frechet_file:
                    line = line.strip('\n')
                    sdeltatapp.append(float(line[1]))

                for i in range(sumcountdt):
                    sumdelta += sdeltat[i]**2

                if iter == 0:
                    initdelta = sumdelta
                print("the delta t of iteration %d is %f\n",iter+1,sumdelta/initdelta)
                count = 0
                for i in range(self.nx):
                    for j in range(self.ny):
                        for k in range(self.nz):
                            # self.sel3D[i][j][k] = 1000/self.vel3D[i][j][k]
                            self.sel3D[count] = 1000/self.vel3D[i][j][k]
                            count += 1

                _sdeltat = np.array(sdeltat, np.float32)
                _sfrenum = np.array(sfrenum, np.int)
                _sdeltatapp = np.array(sdeltatapp, np.float32)
                _sfrenumapp = np.array(sfrenumapp, np.int)
                _sfrelenapp = np.array(sfrelenapp, np.float32)
                _sfrelen = np.array(sfrelen, np.float32)
                lsqr_re.RegLSQR.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_float,c_float,c_float,c_float,c_int,c_int,
                                            npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.int, ndim=1, flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                            # npct.ndpointer(dtype=np.float32, ndim=1, shape=(self.nx, self.ny, self.nz), flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.int, ndim=1, flags="C_CONTIGUOUS"),
                                            npct.ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS")
                                            ]

                self.dens = lsqr_re.RegLSQR(c_int(sumcountdt), c_int(sumnmax), c_int(sumcountdtapp), c_int(sumnmaxapp), c_int(self.sign),c_int(self.nx),
                                c_int(self.ny), c_int(self.nz), c_float(self.damp), c_float(self.lamda), c_float(self.sz),c_float(self.omega),
                                c_int(self.itmax), c_int(self.nx * self.ny * self.nz), _sdeltat, _sfrenum, _sfrelen,self.ds, self.sel3D, _sdeltatapp, _sfrenumapp,_sfrelenapp)

                # lsqr_re.RegLSQR(sumcountdt, sumnmax, sumcountdtapp, sumnmaxapp, self.sign, self.nx, self.ny, self.nz, self.damp, self.lamda, self.sz, self.omega, self.itmax,
                #         self.nx * self.ny * self.nz, sdeltat, sfrenum, sfrelen, self.ds, self.sel3D, sdeltatapp, sfrenumapp, sfrelenapp, self.dens)
                # RegLSQR = lsqr.LSQRFramework(sfrelen)
                # RegLSQR.solve(sdeltat,damp=self.damp, show=True)
                self.smooth()
                with open('velupdate.dat', 'wb+') as fp:
                    for i in range(self.nx):
                        for j in range(self.ny):
                            for k in range(self.nz):
                                if k < int(self.ele[i][j] / self.dz):
                                    self.vel[i][j][k] = 340
                                fp.write(self.vel[i][j][k])
        MPI.Finalize()

    def smooth(self):
        for i in range(self.nx*self.ny*self.nz):
            self.ds[i] = self.ds[i]/1000
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    if self.vel[i][j][k] != 0:
                        s1 = 1.0/self.vel[i][j][k]
                        if self.ds[i + self.nx * j + self.nx * self.ny * k] > s1 * 0.5:
                            self.ds[i+self.nx * j+self.nx * self.ny * k]=s1 * 0.5
                        if self.ds[i + self.nx * j + self.nx * self.ny * k] < -s1 * 0.5:
                            self.ds[i+self.nx * j+self.nx * self.ny * k]=-s1 * 0.5
                        self.vel[i][j][k] = 1. / (s1 + self.ds[i + self.nx * j + self.nx * self.ny * k])

        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    if self.vel[i][j][k] > 10:
                        v = 0
                        siren = 0
                        if i-1>=0 and j-1>=0 and k-1>=0:
                            v=v+self.vel[i-1][j-1][k-1]
                            siren += 1
                        if j-1>=0 and k-1>= 0:
                            v=v+self.vel[i][j-1][k-1]
                            siren+=1
                        if i+1<=self.nx-1 and j-1>=0 and k-1>=0:
                            v=v+self.vel[i+1][j-1][k-1];siren+=1
                        if i-1>=0 and k-1>=0:
                            v=v+self.vel[i-1][j][k-1];siren+=1
                        if k-1>=0:
                            v=v+self.vel[i][j][k-1];siren+=1
                        if (i+1 <= self.nx-1 and k-1 >= 0):
                            v=v+self.vel[i+1][j][k-1];siren+=1
                        if (i-1>=0 and j+1<=self.ny-1 and k-1>=0):
                            v=v+self.vel[i-1][j+1][k-1];siren+=1
                        if (j+1 <= self.ny-1 and k-1 >= 0):
                            v=v+self.vel[i][j+1][k-1];siren+=1
                        if (i+1 <= self.nx-1 and j+1 <= self.ny-1 and k-1 >= 0):
                            v=v+self.vel[i+1][j+1][k-1];siren+=1
                        if (i-1 >= 0 and j-1 >= 0):
                            v=v+self.vel[i-1][j-1][k];siren+=1
                        if (j-1 >= 0):
                            v=v+self.vel[i][j-1][k];siren+=1
                        if (i+1 <= self.nx-1 and j-1 >= 0):
                            v=v+self.vel[i+1][j-1][k];siren+=1
                        if (i-1 >= 0):
                            v=v+self.vel[i-1][j][k];siren+=1
                        if (i+1 <= self.nx-1):
                            v=v+self.vel[i+1][j][k];siren+=1
                        if (i-1 >= 0 and j+1 <= self.ny-1):
                            v=v+self.vel[i-1][j+1][k];siren+=1
                        if (j+1 <= self.ny-1):
                            v=v+self.vel[i][j+1][k];siren+=1
                        if (i+1 <= self.nx-1 and j+1 <= self.ny-1):
                            v=v+self.vel[i+1][j+1][k];siren+=1
                        if (i-1 >= 0 and j-1 >= 0 and k+1 <= self.nz-1):
                            v=v+self.vel[i-1][j-1][k+1];siren+=1
                        if (j-1 >= 0 and k+1 <= self.nz-1):
                            v=v+self.vel[i][j-1][k+1];siren+=1
                        if (i+1 <= self.nx-1 and j-1 >= 0 and k+1 <= self.nz-1):
                            v=v+self.vel[i+1][j-1][k+1];siren+=1
                        if (i-1 >= 0 and k+1 <= self.nz-1):
                            v=v+self.vel[i-1][j][k+1];siren+=1
                        if (k+1 <= self.nz-1):
                            v=v+self.vel[i][j][k+1];siren+=1
                        if (i+1 <= self.nx-1 and k+1 <= self.nz-1):
                            v=v+self.vel[i+1][j][k+1];siren+=1
                        if (i-1 >= 0 and j+1 <= self.ny-1 and k+1 <= self.nz-1):
                            v=v+self.vel[i-1][j+1][k+1];siren+=1
                        if (j+1 <= self.ny-1 and k+1 <= self.nz-1):
                            v=v+self.vel[i][j+1][k+1];siren+=1
                        if (i+1 <= self.nx-1 and j+1 <= self.ny-1 and k+1 <= self.nz-1):
                            v=v+self.vel[i+1][j+1][k+1];
                            siren+=1

                        self.vel[i][j][k]=1.0 / (2 * siren) * v+0.5 * self.vel[i][j][k]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("-n", help="the pool number.")
    # npool = parser.parse_args()
    rc.initialize = False
    tomo3D = tomo()
    tomo3D.start()

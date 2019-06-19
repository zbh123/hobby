import os
from multiprocessing import Pool
import numpy as np
import pandas as pd
import struct
import math
from mpi4py import MPI
from ctypes import *
# import lsqr
fast = CDLL('fast.so', mode=RTLD_GLOBAL)
lsqr_re = CDLL('lsqr_re.so', mode=RTLD_GLOBAL)

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
        self.delta = 0.0
        self.sign = 1.0
        self.damp = 0.0
        self.lamda = 0.0
        self.sz = 0.0
        self.omega = 0.0
        self.itmax = 0
        self.niter = 0


        self.readpar()
        self.buildrealmodel()
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
        self.delta = float(readlines[9].strip('\n'))
        self.sign = 1.0
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
        item = np.zeros((nx, ny, nz))
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
        vel3D = np.zeros((self.nx, self.ny, self.nz))
        eps = np.zeros((self.nx, self.ny, self.nz))
        delta = np.zeros((self.nx, self.ny, self.nz))
        self.vel = np.zeros(self.nx * self.ny * self.nz)
        self.vx = np.zeros(self.nx * self.ny * self.nz)
        self.q = np.zeros(self.nx * self.ny * self.nz)
        count = 0
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    if k < int(self.ele[i][j]/self.dz):
                        vel3D[i][j][k] = 340
                        eps[i][j][k] = 0.0001
                        delta[i][j][k] = 0.0001
                    else:
                        vel3D[i][j][k] = self.v0 + k*self.dv
                        eps[i][j][k] = vel3D[i][j][k]/15000
                        delta[i][j][k] = vel3D[i][j][k]/30000

                    self.vel[count] = (1 / vel3D[i][j][k]) ** 2
                    self.q = (1 + 2 * delta[i][j][k]) / (1 + 2 * eps[i][j][k])
                    self.vx[count] = self.vel[count] / (1 + 2 * eps[i][j][k])
                    count += 1
        print("build model OK")
        self.shotxyz = np.zeros((self.nshot, 3))
        self.recxyz = np.zeros((self.nray, 3))
        with open('shot.txt','r') as fp:
            shot_location = fp.readlines()
        if len(shot_location) >= self.nshot:
            for i in range(self.nshot):
                if shot_location[i].strip('\n').strip():
                    shot = shot_location[i].strip('\n').strip().split()
                    tempx = int(float(shot[0].strip('\n').strip()) / self.dx + 0.5)
                    tempy = int(float(shot[1].strip('\n').strip()) / self.dy + 0.5)
                    self.shotxyz[i][0] = float(shot[0].strip('\n').strip())
                    self.shotxyz[i][1] = float(shot[1].strip('\n').strip())
                    self.shotxyz[i][2] = self.ele[tempx][tempy]

        with open('rec.txt','r') as fp:
            rec_location = fp.readlines()
        if len(rec_location) >= self.nray:
            for i in range(self.nray):
                if rec_location[i].strip('\n').strip():
                    rec = rec_location[i].strip('\n').strip().split()
                    tempx = int(float(rec[0].strip('\n').strip()) / self.dx + 0.5)
                    tempy = int(float(rec[1].strip('\n').strip()) / self.dy + 0.5)
                    self.recxyz[i][0] = float(rec[0].strip('\n').strip())
                    self.recxyz[i][1] = float(rec[1].strip('\n').strip())
                    self.recxyz[i][2] = self.ele[tempx][tempy]

    def calculate_time(self, iter, ishot, nx, ny, nz, vel, q, vx, realvel, realq, realvx, flag, plane, dx, dy, dz,
                       shotxyz, recxyz, delta, neachshot, fdelta, fdeltaapp,
                       frechet, frechetapp):

        ifree = int(2 * math.sqrt((nx * dx) ** 2 + (ny * dy) ** 2 + (nz * dz) ** 2))
        time = np.zeros((nx * ny * nz))
        time3D = np.zeros((nx, ny, nz))
        realtime3D = np.zeros((nx, ny, nz))
        realtime = np.zeros((nx * ny * nz))
        tmp_time = np.zeros((nx * ny * nz))
        fast.fastmarch_init(nx, ny, nz)
        fast.fastmarch((c_float * len(time))(*time.tolist()), (c_float * len(tmp_time))(*tmp_time.tolist),
                       (c_float * len(vx))(*vx.tolist()), (c_float * len(vel))(*vel.tolist()), (c_float * len(q))(*q.tolist()),
                       flag, plane, nx, ny, nz, 0, 0, 0, dx, dy, dz, float(shotxyz[ishot][0]),
                       float(shotxyz[ishot][0][1]), float(shotxyz[ishot][0][2]), 1, 1, 1, 1)
        fast.fastmarch((c_float * len(realtime))(*realtime.tolist()), (c_float * len(tmp_time))(*tmp_time.tolist),
                       (c_float * len(realvx))(*realvx.tolist()), (c_float * len(realvel))(*realvel.tolist()), (c_float * len(realq))(*realq.tolist()),
                       flag, plane, nx, ny, nz, 0, 0, 0, dx, dy, dz, float(shotxyz[ishot][0]),
                       float(shotxyz[ishot][0][1]), float(shotxyz[ishot][0][2]), 1, 1, 1, 1)
        # fast.fastmarch(realtime, tmp_time, realvx, realvel, realq, flag, plane, nx, ny, nz, 0, 0, 0, dx, dy, dz,
        #                shotxyz[ishot][0], shotxyz[ishot][1], shotxyz[ishot][2], 1, 1, 1, 1)
        fast.fastmarch_close()
        print("VTIFMM of %s shot has been calculated(ID:%d, Ite:%d)\n" % (ishot + 1, ishot + 1, iter + 1))
        count = 0
        time = np.array(time)
        realtime = np.array(realtime)
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    time3D[i][j][k] = time[count]
                    realtime3D[i][j][k] = realtime[count]
                    count += 1
        gx = np.zeros((nx, ny, nz))
        gy = np.zeros((nx, ny, nz))
        gz = np.zeros((nx, ny, nz))
        self.laplace(nx, ny, nz, time3D, dx, dy, dz, gx, gy, gz)
        count = 0
        gradientArray = np.zeros((3 * nx * ny * nz))
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    gradientArray[count] = gx[i][j][k]
                    count += 1
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    gradientArray[count] = gy[i][j][k]
                    count += 1
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    gradientArray[count] = gz[i][j][k]
                    count += 1
        js = sum(neachshot, ishot)
        dt = realtime3D[int(recxyz[js][0] / dx)][int(recxyz[js][1] / dy)][int(recxyz[js][2] / dy)] - \
             time3D[int(recxyz[js][0] / dx)][int(recxyz[js][1] / dy)][int(recxyz[js][2] / dy)]
        dt1 = dt
        shotpoint = np.zeros((3))
        recpoint = np.zeros((3))
        shotpoint[0] = shotxyz[ishot][0] + dx
        shotpoint[1] = shotxyz[ishot][1] + dy
        shotpoint[2] = shotxyz[ishot][2] + dz
        recpoint[0] = recxyz[js][0] + dx
        recpoint[1] = recxyz[js][1] + dy
        recpoint[2] = recxyz[js][2] + dz
        gArray1 = np.zeros((ifree), np.int)
        gArray2 = np.zeros((ifree), np.int)
        freArray1 = np.zeros((ifree))
        freArray2 = np.zeros((ifree))
        cal1 = 0
        cal2 = 0
        siren1 = self.shortestpath(recpoint, shotpoint, delta, gradientArray, nx, ny, nz, dx, dy, dz, dt,
                              gArray1, freArray1, cal1, fdelta, frechet)
        for js in range(sum(neachshot, ishot) + 1, sum(neachshot, ishot) + neachshot[ishot]):
            dt = realtime3D[int(recxyz[js][0] / dx)][int(recxyz[js][1] / dy)][int(recxyz[js][2] / dy)] - \
                 time3D[int(recxyz[js][0] / dx)][int(recxyz[js][1] / dy)][int(recxyz[js][2] / dy)]
            dt2 = dt
            shotpoint = np.zeros((3))
            recpoint = np.zeros((3))
            shotpoint[0] = shotxyz[ishot][0] + dx
            shotpoint[1] = shotxyz[ishot][1] + dy
            shotpoint[2] = shotxyz[ishot][2] + dz
            recpoint[0] = recxyz[js][0] + dx
            recpoint[1] = recxyz[js][1] + dy
            recpoint[2] = recxyz[js][2] + dz
            siren2 = self.shortestpath(recpoint, shotpoint, delta, gradientArray, nx, ny, nz, dx, dy, dz,
                                  dt, gArray2, freArray2, cal2, fdelta, frechet)
            self.appvel(js, recxyz, dt1, dt2, gArray1, freArray1, cal1, gArray2, freArray2, cal2,
                   fdeltaapp, frechetapp)

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
                    elif j == nz - 1:
                        gz[i][j][k] = (time3D[i][j][k] - time3D[i][j][k - 1]) / dz
                    else:
                        gz[i][j][k] = (time3D[i][j][k + 1] - time3D[i][j][k - 1]) / (2 * dz)

    def mindex3(self, x, y, z, sizx, sizy):
        return z * sizy * sizx + y * sizx + x

    def interpgrad3d(self, Ireturn, grad, Isize, point, dx, dy, dz):
        perc = np.zeros((8))
        index = np.zeros((8))
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

    def shortestpath(self, startpoint, sourcepoint, stepsize, gradientArray, nx, ny, nz, dx, dy, dz, dt,
                     gArraym, freArraym, calm, fdelta, frechet):
        l = 0.0
        nextpoint = np.zeros((3))
        ifree = int(2 * math.sqrt((nx * dx) ** 2 + (ny * dy) ** 2 + (nz * dz) ** 2) / stepsize)
        shortestLine = np.zeros((3, ifree))
        theta = np.zeros((ifree))
        gArray = np.zeros((ifree))
        freArray = np.zeros((ifree))
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
                l += math.sqrt((startpoint[0] - nextpoint[0]) ** 2 + (startpoint[1] - nextpoint[1]) ** 2 + (
                            startpoint[2] - nextpoint) ** 2)
                theta[cal] = math.atan((startpoint[2] - nextpoint[2]) / l)
            else:
                l = l + math.sqrt((startpoint[0] - dx - (startpoint[0] - dx + nextpoint[0] - dx) / 2) ** 2 + (
                            startpoint[1] - dy - (startpoint[1] - dy + nextpoint[1] - dy) / 2) ** 2 + (
                                              startpoint[2] - dz - (startpoint[2] - dz + nextpoint[2] - dz) / 2) ** 2)
                igrid = sfregridz * nx * ny + sfregridy * nx + sfregridx
                gArray[cal] = igrid
                freArray[cal] = l
                cal += 1
            distanceToEnd = math.sqrt((sourcepoint[0] - nextpoint[0]) ** 2 + (sourcepoint[1] - nextpoint[1]) ** 2 + (
                        sourcepoint[2] - nextpoint[2]) ** 2)
            if distanceToEnd < stepsize:
                break
            if count > 10:
                movement = math.sqrt((nextpoint[0] - shortestLine[count - 10][0]) ** 2 + (
                            nextpoint[1] - shortestLine[count - 10][1]) ** 2 + (
                                                 nextpoint[2] - shortestLine[count - 10][2]) ** 2)
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
                freArray[cal] = l
                cal += 1
            else:
                igrid = nfregridz * nx * ny + nfregridy * nx + nfregridx
                gArray[cal] = igrid
                freArray[cal] = l
                cal += 1
        if flag == 0 and cal != 0:
            calm = cal
            for i in range(cal):
                if math.fabs(freArray[i]) > 1e-6:
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

    def appvel(self, js, recxyz, dt1, dt2, gArray1, freArray1, cal1, gArray2, freArray2, cal2, fdeltaapp,
               frechetapp):
        siren = 0
        dt = dt1 - dt2
        dx = math.sqrt((recxyz[js][0] - recxyz[js - 1][0]) ** 2 + (recxyz[js][1] - recxyz[js - 1][1]) ** 2 + (
                    recxyz[js][2] - recxyz[js - 1][2]) ** 2)
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

    def sum(self, neachshot, ishot):
        s = 0
        for i in range(ishot):
            s += neachshot[i]
        return s

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
                            v=v+self.vel[i+1][j+1][k+1];siren+=1

                        self.vel[i][j][k]=1.0 / (2 * siren) * v+0.5 * self.vel[i][j][k]
    def start(self):

        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        self.ds = np.zeros((self.nx*self.ny*self.nz))
        self.sel3D = np.zeros((self.nx, self.ny, self.nz))
        self.dens = np.zeros((self.nx, self.ny, self.nz))
        flag = np.zeros((self.nx*self.ny*self.nz), np.int)
        initdelta = 0
        plane = [False, False, False]
        if rank == 0:
            print("==========The 3D VTI First Break Tomo Start==========\n")
        for iter in range(self.niter):
            if iter > 0:
                self.vel = self.read_3d('velupdate.dat', self.nx, self.ny, self.nz)
                self.eps = self.read_3d('velupdate.dat', self.nx, self.ny, self.nz)
                self.delta = self.read_3d('velupdate.dat', self.nx, self.ny, self.nz)
                self.vel = np.zeros(self.nx * self.ny * self.nz)
                self.vx = np.zeros(self.nx * self.ny * self.nz)
                self.q = np.zeros(self.nx * self.ny * self.nz)
                count = 0
                for i in range(self.nx):
                    for j in range(self.ny):
                        for k in range(self.nz):
                            self.vel[count] = (1 / (self.vel[i][j][k])) ** 2
                            self.q[count] = (1 + 2 * self.delta[i][j][k]) / (1 + 2 * self.eps[i][j][k])
                            self.vx[count] = self.vel[count] / (1 + 2 * self.eps[i][j][k])
                            count += 1
            if rank == 0:
                print("**************The %d ITERATION**************"%(iter+1))

            fdelta = open('fdelta%d.dat'%rank, 'a')
            fdeltaapp = open('fdeltaapp%d.dat'%rank, 'a')
            frechet = open('frechet%d.dat'%rank, 'a')
            frechetapp = open('frechetapp%d.dat'%rank, 'a')
            self.countdt = 0
            self.countdtapp = 0
            sumnmax = 0
            sumcountdt = 0
            self.nmax = 0
            self.nmaxapp = 0
            sumnmaxapp = 0
            sumcountdtapp = 0
            sumdelta = 0
            # p = Pool(processes=10)
            for ishot in range(rank, self.nshot, size):
                self.calculate_time(iter, ishot, self.nx, self.ny, self.nz, self.vel, self.q, self.vx,
                                               self.realvel, self.realq, self.realvx, flag, plane, self.dx, self.dy,
                                               self.dz, self.shotxyz, self.recxyz, self.delta, self.neachshot, fdelta, fdeltaapp, frechet, frechetapp)
                print("Raytrace of %d shot has been calculated(ID:%d, Ite:%d)\n" % (ishot + 1, ishot+1, iter + 1))
            fdeltaapp.close(); fdelta.close(); frechetapp.close(); frechet.close()
            tempnamx = []
            tempcountdt = []
            tempnmaxapp = []
            tempcountdtapp = []
            if rank!=0:
                comm.send(self.nmax, dest=0)
                comm.send(self.countdt, dest=0)
                comm.send(self.nmaxapp, dest=0)
                comm.send(self.countdtapp, dest=0)
            if rank == 0:
                tempnamx.append(self.nmax)
                tempcountdt.append(self.nmax)
                tempnmaxapp.append(self.nmax)
                tempcountdtapp.append(self.nmax)

                for i in range(1, size):
                    tempnamx.append(comm.recv(source=i))
                    tempcountdt.append(comm.recv(source=i))
                    tempnmaxapp.append(comm.recv(source=i))
                    tempcountdtapp.append(comm.recv(source=i))

                for i in range(size):
                    sumnmax += tempnamx[i]
                    sumcountdt += tempcountdt[i]
                    sumnmaxapp += tempnmaxapp[i]
                    sumcountdtapp += tempcountdtapp[i]

                # sfrenum = np.zeros((sumnmax + sumcountdt), np.int)
                # sfrelen = np.zeros((sumnmax + sumcountdt))
                # sdeltat = np.zeros((sumcountdt))
                # sfrenumapp = np.zeros((sumnmaxapp + sumcountdtapp), np.int)
                # sfrelenapp = np.zeros((sumnmaxapp + sumcountdtapp))
                # sdeltatapp = np.zeros((sumcountdtapp))
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
                    with open("frechet%d.dat"%i, 'r') as fp:
                        for line in fp.readlines():
                            frechet_file.append(line)
                    with open("frechetapp%d.dat"%i, 'r') as fp:
                        for line in fp.readlines():
                            frechetapp_file.append(line)
                    with open("fdelta%d.dat"%i, 'r') as fp:
                        for line in fp.readlines():
                            fdelta_file.append(line)
                    with open("fdeltaapp%d.dat"%i, 'r') as fp:
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

                for i in range(self.nx):
                    for j in range(self.ny):
                        for k in range(self.nz):
                            self.sel3D[i][j][k] = 1000/self.vel[i][j][k]

                lsqr_re.RegLSQR(sumcountdt, sumnmax, sumcountdtapp, sumnmaxapp, self.sign, self.nx, self.ny, self.nz, self.damp, self.lamda, self.sz, self.omega, self.itmax,
                        self.nx * self.ny * self.nz, sdeltat, sfrenum, sfrelen, (c_float * len(self.ds))(*self.ds.tolist()), self.sel3D, sdeltatapp, sfrenumapp, sfrelenapp, self.dens)
                # RegLSQR = lsqr.LSQRFramework(sfrelen)
                # RegLSQR.solve(sdeltat,damp=self.damp, show=True)
                self.ds = np.array(self.ds)
                self.smooth()
                with open('velupdate.dat', 'wb+') as fp:
                    for i in range(self.nx):
                        for j in range(self.ny):
                            for k in range(self.nz):
                                if k < int(self.ele[i][j] / self.dz):
                                    self.vel[i][j][k] = 340
                                fp.write(self.vel[i][j][k])




if __name__ == '__main__':
    tomo3D = tomo()
    tomo3D.start()














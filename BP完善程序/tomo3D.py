import os

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
        self.omega = 0.0
        self.itmax = 0
        self.niter = 0

    def readpar(self):
        with open('Tomo3D.par', 'r') as fp:
            readlines = fp.readline()
        self.nshot = int(readlines[0])
        self.nx = int(readlines[1])
        self.ny = int(readlines[2])
        self.nz = int(readlines[3])
        self.dx = float(readlines[4])
        self.dy = float(readlines[5])
        self.dz = float(readlines[6])
        self.v0 = float(readlines[7])
        self.dv = float(readlines[8])
        self.delta = float(readlines[9])
        self.sign = 1.0
        self.damp = float(readlines[10])
        self.lamda = float(readlines[11])
        self.omega = float(readlines[12])
        self.itmax = int(readlines[13])
        self.niter = int(readlines[14])
        with open('count.txt','r') as fp:
            self.neachshot = fp.readlines()
        if len(self.neachshot) <= self.nshot:
            print('number of shot error')
            os._exit(0)
        self.nray = 0
        for i in self.neachshot:
            self.nray += int(i)

    def buildrealmodel(self):
        with open('elevation.dat','r') as fp:
            self.ele = fp.readlines()
        with open('velmodel_bp.dat','r') as fp:
            self.realvel = fp.readlines()
        with open('epsilon_bp.dat','r') as fp:
            self.realeps = fp.readlines()
        with open('delta_bp.dat','r') as fp:
            self.realdelta = fp.readlines()

    def buildmodel(self):
        with open('shot.txt','r') as fp:




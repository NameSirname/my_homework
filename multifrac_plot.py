from PyQt5.QtWidgets import QSizePolicy

import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.animation as ani
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure


import numpy as np
import time

import subprocess as sub


class PLOT(FCanvas):
    def __init__(self, parent,pic=[],ims=[]):
        self.parent = parent
        self.deph = parent.deph.value()
        self.w = parent.Width.value()-parent.toolbar_width
        self.h = parent.Height.value()

        self.pic = pic
        self.ims = ims

        self.a = float(parent.a.text())
        self.c = float(parent.c.text())
        self.b = round(float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)
        self.d = round(-float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)

        self.frames = int(parent.frames.text())
        self.speed = int(parent.speed.text())
        
        self.D = [self.a,self.b]
        self.colorMap = parent.CMap.currentText()
        self.const = complex(self.parent.const.text())

        
###
        self.fig = Figure(figsize = (self.w,self.h),dpi=1)

        FCanvas.__init__(self,self.fig)
        self.setParent(parent)

        FCanvas.setSizePolicy(self,
                              QSizePolicy.Expanding,
                              QSizePolicy.Expanding)
        FCanvas.updateGeometry(self)

###                      
        self.fig.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0)
        ax = self.fig.add_subplot(111)
        ax.axis('scaled')
        ax.axis([0,self.w,0,self.h])
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.yaxis.set_major_formatter(plt.NullFormatter())


    def plot(self):
        if len(self.pic)==0:
            self.pic=self.bitmap()    
        ax = self.fig.gca()
        ax.imshow(self.pic, cmap = self.colorMap)


    def animate(self):
        if len(self.ims)==0:
            self.ims = self.ani_bitmap()
            self.plot()
        ax = self.fig.gca()
        ims = [[ax.imshow(im, cmap = self.colorMap)] for im in self.ims]
        self.Anima = ani.ArtistAnimation(self.fig, ims, interval = self.speed,
                                         blit = True, repeat = False)
        
        
    def bitmap(self):
        inp = open("in.txt","w")
        inp.write("{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(
            self.w,self.h,self.deph,
            self.a,self.b,self.c,self.d,
            self.const.real,self.const.imag))
        inp.close()

        start = time.time()
        p = sub.Popen(["./a.o"], stdout=sub.PIPE)
        p.communicate()
        print("{0:.2f} sec".format(time.time()-start))
        
        out = open("out.txt","r")
        B = np.array([[float(e) for e in line.split()] for line in out.read().split('\n')[:-1]])
        out.close()
        
        return B

    def ani_bitmap(self):
        exec('''global G
G = lambda c: {0}'''.format(self.parent.delta.text()),globals())
        ims=[]
        c = self.const
        for i in range(self.frames):
            print(i,end='\t')
            im = self.bitmap()
            ims.append(im)
            self.const = G(self.const)
        self.const = c
        
        return ims


    def mousePressEvent(self,event):
        if self.parent.i:
            self.a = round((self.c-self.a)*event.pos().x()/self.w+self.a,6)
            self.b = round((self.d-self.b)*event.pos().y()/self.h+self.b,6)
        
    def mouseReleaseEvent(self,event):
        if self.parent.i:
            self.c = round((self.c-self.D[0])*event.pos().x()/self.w+self.D[0],6)
            self.d = round((self.d-self.D[1])*event.pos().y()/self.h+self.D[1],6)
            self.parent.find(self.a,self.b,self.c,self.d)
            self.parent.i=False



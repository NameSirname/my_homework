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
    def __init__(self, parent):
        self.parent = parent
        
        self.pic = []
        self.ims = []
        
        self.fig = Figure(figsize = ((self.parent.Width.value()-self.parent.toolbar_width)/8,
                                     (self.parent.Height.value())/8), dpi=8)

        FCanvas.__init__(self,self.fig)
        self.setParent(self.parent)

        FCanvas.setSizePolicy(self,
                              QSizePolicy.Expanding,
                              QSizePolicy.Expanding)
        FCanvas.updateGeometry(self)
                
        self.fig.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0)
        self.ax = self.fig.add_subplot(111)

        self.ax.axis('scaled')
        self.ax.xaxis.set_major_formatter(plt.NullFormatter())
        self.ax.yaxis.set_major_formatter(plt.NullFormatter())

    def Build(self):
        self.w = self.parent.Width.value()-self.parent.toolbar_width
        self.h = self.parent.Height.value()
        self.fig.set_size_inches(self.w/8,self.h/8)
        
        self.deph = self.parent.deph.value()

        self.offset = float(self.parent.offset.text())
        self.a = float(self.parent.minX.text())
        self.c = float(self.parent.maxX.text())
        self.b = float((self.c-self.a)/2*self.h/self.w)+self.offset
        self.d = -float((self.c-self.a)/2*self.h/self.w)+self.offset

        self.frames = int(self.parent.frames.text())
        
        self.colorMap = self.parent.CMap.currentText()
        self.const = complex(self.parent.const.text())
        
        self.ax.axis([0,self.w-1,0,self.h-1])

    def plot(self):
        if len(self.pic)==0:
            self.pic = self.bitmap()
            
        self.ax.imshow(self.pic, cmap = self.colorMap)

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

    def animate(self):
        if len(self.ims)==0:
            self.plot()
            self.ani_bitmap()
            
        ims = [[self.ax.imshow(im, cmap = self.colorMap)] for im in self.ims]
        self.Anima = ani.ArtistAnimation(self.fig, ims,
                                         interval = int(self.parent.speed.text()),
                                         blit = True, repeat = False)


    def ani_bitmap(self):
        exec('''global D
D = lambda c: {0}'''.format(self.parent.delta.text()),globals())
        c = self.const
        for i in range(self.frames):
            print(i,end='\t')
            self.pic = self.bitmap()
            self.ims.append(self.pic)
            self.const = D(self.const)
        self.const = c
        
        return None

    def mousePressEvent(self,event):
        if self.parent.zooming:
            self.parent.zoom_point = event.pos()
        
    def mouseReleaseEvent(self,event):
        if self.parent.zooming:
            self.parent.minX.setText(str(round(self.a + (self.c - self.a)*self.parent.zoom_point.x()/self.w,6)))
            self.parent.maxX.setText(str(round(self.a + (self.c - self.a)*event.x()/self.w,6)))
            self.parent.offset.setText(str(round(self.b - (self.b - self.d)*(self.parent.zoom_point.y()+event.y())/2/self.h,6)))




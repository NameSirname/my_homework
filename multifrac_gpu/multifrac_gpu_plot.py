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

from importlib import reload

import multifrac_gpu_bitmap as f_bitmap

class PLOT(FCanvas):
    def __init__(self, parent):
        self.parent = parent
        self.w = self.parent.Width.value()-self.parent.toolbar_width
        self.h = self.parent.Height.value()
        
        self.pic = []
        self.ims = []
        
        self.fig = Figure(figsize = (self.w/8,self.h/8),dpi=8)

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
        self.deph = self.parent.deph.value()

        self.offset = float(self.parent.offset.text())
        self.a = float(self.parent.minX.text())
        self.c = float(self.parent.maxX.text())
        self.b = float((self.c-self.a)/2*self.h/self.w)+self.offset
        self.d = -float((self.c-self.a)/2*self.h/self.w)+self.offset

        self.frames = int(self.parent.frames.text())
        self.speed = int(self.parent.speed.text())
        
        self.colorMap = self.parent.CMap.currentText()
        self.const = complex(self.parent.const.text())
        
        self.ax.axis([0,self.w-1,0,self.h-1])

    def plot(self):
        if len(self.pic)==0:
            delta = (self.c-self.a)/self.w
            self.pic = np.array([complex(self.a+(i%self.w)*delta,
                                         self.d+(i//self.w)*delta) for i in range(self.w*self.h)])
            
            start = time.time()
            self.pic = f_bitmap.bitmap(self.pic,self.const,self.deph).reshape([self.h,self.w])
            print("{0:.2f} sec".format(time.time()-start))
            
        self.ax.imshow(self.pic.real, cmap = self.colorMap)

    def animate(self):
        if len(self.ims)==0:
            self.ims = self.ani_bitmap()
            self.plot()
            
        ims = [[self.ax.imshow(im, cmap = self.colorMap)] for im in self.ims]
        self.Anima = ani.ArtistAnimation(self.fig, ims, interval = self.speed,
                                         blit = True, repeat = False)


    def ani_bitmap(self):
        ims=[]
        c = self.const
        delta = (self.c-self.a)/self.w
        for i in range(self.frames):
            print(i,end='\t')
            self.pic = np.array([complex(self.a+(i%self.w)*delta,
                                         self.d+(i//self.w)*delta) for i in range(self.w*self.h)])
            self.pic = f_bitmap.bitmap(self.pic,self.const,self.deph).reshape([self.h,self.w])
            ims.append(self.pic.real)
            self.const = H(self.const)
        self.const = c
        
        return ims

    def mousePressEvent(self,event):
        if self.parent.zooming:
            self.parent.zoom_point = event.pos()
        
    def mouseReleaseEvent(self,event):
        if self.parent.zooming:
            self.parent.minX.setText(str(round(self.a + (self.c - self.a)*self.parent.zoom_point.x()/self.w,6)))
            self.parent.maxX.setText(str(round(self.a + (self.c - self.a)*event.x()/self.w,6)))
            self.parent.offset.setText(str(round(self.b - (self.b - self.d)*(self.parent.zoom_point.y()+event.y())/2/self.h,6)))

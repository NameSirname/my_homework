import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QComboBox, QCheckBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

import numpy as np
import random
import time

import ctypes as C

import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.animation as ani
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure

import my_cmaps

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 900
        self.height = 700
        self.title = 'Jolia'

        self.i=False
        
        self.initGUI()
                
    def initGUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.win = QWidget(self)
        self.win.resize(200,self.size().height())
        self.win.move(self.width-200,0)

        self.win.setStyleSheet("""
            .QWidget {
                background-color: #123;}""")
        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(pal)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        self.win.setLayout(grid)
 ###       
        self.deph = QSpinBox(self)
        self.deph.setValue(2)
        self.deph.setRange(1,10000)
        grid.addWidget(self.deph,0,0,1,2)

        self.deph.l = QLabel('deph')
        self.deph.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.deph.l,0,2,1,-1)
 ###       

        self.const_re = QLineEdit('-0.745',self)
        grid.addWidget(self.const_re,1,0,1,2)

        self.const_im = QLineEdit('0.115',self)
        grid.addWidget(self.const_im,2,0,1,2)
        
        self.const_re.l = QLabel('real(c)')
        self.const_re.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.const_re.l,1,2,1,-1)
        
        self.const_im.l = QLabel('imag(c)')
        self.const_im.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.const_im.l,2,2,1,-1)

 ###
        self.func = QLineEdit(self)
        self.func.setText('z*z+c')
        grid.addWidget(self.func,3,0,1,-1)
        
 ###
        self.CMap = QComboBox(self)
        A = sorted(['hot','viridis','plasma','inferno',
             'flag','prism','nipy_spectral','RdYlBu',
             'BuPu','YlGnBu','ocean','gist_earth',
             'gist_ncar','jet','cubehelix','rainbow'])
        self.CMap.addItems(A)        
        self.CMap.addItems(list(map(lambda x: x+'_r',A)))


        self.CMap.addItems(my_cmaps.A)
                            
        self.CMap.setCurrentText('p2')
        grid.addWidget(self.CMap,4,0,1,2)
        self.CMap.activated.connect(self.CMap_act)

        self.CMap.l = QLabel('cmap')
        self.CMap.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.CMap.l,4,2,1,-1)

 ###
        Enter = QPushButton('Draw', self)
        Enter.clicked.connect(self.Enter)
        grid.addWidget(Enter,5,0,1,2)

        self.plot = QCheckBox(self)
        self.plot.setCheckState(2);
        grid.addWidget(self.plot,5,2,1,-1)
 ###       
        self.Width = QSpinBox(self)
        self.Width.setRange(900,25000)
        self.Width.setValue(900)
        self.Width.setSingleStep(10)
        grid.addWidget(self.Width,6,0,1,2)
        
        self.Height = QSpinBox(self)
        self.Height.setRange(700,23000)
        self.Height.setValue(700)
        self.Height.setSingleStep(10)
        grid.addWidget(self.Height,7,0,1,2)

        self.Width.l = QLabel('width')
        self.Width.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.Width.l,6,2,1,-1)
        
        self.Height.l = QLabel('height')
        self.Height.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.Height.l,7,2,1,-1)
 ###        
        Resize = QPushButton('Resize', self)
        Resize.clicked.connect(self.Resize)
        grid.addWidget(Resize,8,0,1,-1)
###
        self.a = QLineEdit('-1.5',self)
        grid.addWidget(self.a,9,0,1,1)

        self.c = QLineEdit('1.5',self)
        grid.addWidget(self.c,10,0,1,1)
        
        self.d = QLineEdit('0',self)
        grid.addWidget(self.d,10,2,1,1)

        self.d.l = QLabel('offset')
        self.d.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.d.l,9,2,1,-1)

###        
        lg = QPushButton("Lupa'n'Pupa", self)
        lg.clicked.connect(self.lg)
        grid.addWidget(lg,11,0,1,-1)
###
        Save = QPushButton('Save', self)
        Save.clicked.connect(self.Save)
        grid.addWidget(Save,12,0,1,-1)

###
        Animate = QPushButton('Animate', self)
        Animate.clicked.connect(self.Animate)
        grid.addWidget(Animate,13,0,1,1)

        self.speed = QLineEdit('500',self)
        grid.addWidget(self.speed,13,2,1,1)

        self.delta = QLineEdit('c+0-0.01j',self)
        grid.addWidget(self.delta,14,0,1,1)
        
        self.fps = QLineEdit('2',self)
        grid.addWidget(self.fps,14,2,1,1)
###
        Save_Ani = QPushButton('Save_Ani', self)
        Save_Ani.clicked.connect(self.Save_Ani)
        grid.addWidget(Save_Ani,15,0,1,-1)

###
        self.Mp = Mplot(self)
        self.Mp.move(0,0)
        self.state = 0
        
        self.show()


    def Enter(self):
        self.Mp.close()
        self.Mp = Mplot(self, ims = self.Mp.ims)
        self.Mp.move(0,0)
        self.Mp.plot()
        self.state = 1
        if self.plot.checkState():
            self.Mp.show()

    def Resize(self):
        self.resize(self.Width.value(),self.Height.value())
        self.move(0,0)
        self.win.resize(200,self.size().height())
        self.win.move(self.size().width()-200,0)

        self.Mp.close()
        self.Mp = Mplot(self)
        self.Mp.move(0,0)
        self.state = 0
            

    def Save(self):
        filename = QFileDialog.getSaveFileName(self,
                            directory = '/home/mister/Изображения/fractals/',
                            caption = 'save_fractal')[0]
        if filename!='':
            self.Mp.fig.savefig(filename, format='png')

    def Animate(self):
        self.Mp.close()
        self.Mp = Mplot(self, pic = self.Mp.pic)
        self.Mp.move(0,0)
        self.Mp.animate()
        self.state = 2
        if self.plot.checkState():
            self.Mp.show()
        
    def Save_Ani(self):
        filename = QFileDialog.getSaveFileName(self,
                            directory = '/home/mister/Изображения/animated_fractals/',
                            caption = 'save_animated_fractal')[0]
        if filename!='':
            self.Mp.Anima.save(filename)
            
    def CMap_act(self):
        self.Mp.close()
        self.Mp = Mplot(self, pic = self.Mp.pic, ims = self.Mp.ims)
        self.Mp.move(0,0)
        if self.state == 1:
            self.Mp.plot()
        elif self.state == 2:
            self.Mp.animate()
        if self.plot.checkState():
            self.Mp.show()

        
    def lg(self):
        self.i = not self.i
        if self.i:
            QApplication.setOverrideCursor(Qt.CrossCursor)
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
    
    def find(self,a,b,c,d):       
        self.a.setText(str(round(a,6)))
        self.c.setText(str(round(c,6)))
        self.d.setText(str(round((b+d)/2,6)))


        
class Mplot(FCanvas):
    def __init__(self, parent,pic=[],ims=[]):
        self.parent = parent
        self.deph = parent.deph.value()
        self.w = parent.Width.value()-200
        self.h = parent.Height.value()

        self.pic = pic
        self.ims = ims

        self.a = float(parent.a.text())
        self.c = float(parent.c.text())
        self.b = round(float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)
        self.d = round(-float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)

        self.fps = int(parent.fps.text())
        self.speed = int(parent.speed.text())
        
        self.D = [self.a,self.b]
        self.colorMap = parent.CMap.currentText()


        self.const = complex(float(self.parent.const_re.text())
                             ,float(self.parent.const_im.text()))
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
##            f_file = open("fractal1.1.h","w")
##            f_file.write('''#include<complex.h>
###include<math.h>
##double complex F(double complex,double complex);
##
##double complex F(double complex z,double complex c){
##	return %s;
##}'''%(self.parent.func.text()))
##            f_file.close()

            self.lib_c = C.cdll.LoadLibrary('/home/mister/PyProj/fractals_C/a1.so.6')
            self.pic=self.bitmap()    
        ax = self.fig.gca()
        ax.imshow(self.pic, cmap = self.colorMap)


    def animate(self):
        if len(self.ims)==0:
##            f_file = open("fractal1.1.h","w")
##            f_file.write('''#include<complex.h>
###include<math.h>
##double complex F(double complex,double complex);
##
##double complex F(double complex z,double complex c){
##	return %s;
##}'''%(self.parent.func.text()))
##            f_file.close()
            
            self.lib_c = C.cdll.LoadLibrary('/home/mister/PyProj/fractals_C/a1.so.6')
            self.ims = self.ani_bitmap()
            self.plot()
        ax = self.fig.gca()
        ims = [[ax.imshow(im, cmap = self.colorMap)] for im in self.ims]
        self.Anima = ani.ArtistAnimation(self.fig, ims, interval = self.speed,
                                         blit = True, repeat = False)
        
        
    def bitmap(self):
        INTP = C.POINTER(C.c_int)
        B = (INTP*self.h)()
        for i in range(self.h):
            B[i] = (C.c_int*self.w)()
            for j in range(self.w):
                B[i][j]=0

        start = time.time()
        a = self.lib_c.bitmap(self.w,self.h,self.deph,
                         C.c_double(self.a),C.c_double(self.b),
                         C.c_double(self.c),C.c_double(self.d),
                         C.c_double(self.const.real),C.c_double(self.const.imag),
                         B)
        B = np.array([[B[i][j] for j in range(self.w)] for i in range(self.h)])
        print("{0:.2f} sec".format(time.time()-start))
        
        return B

    def ani_bitmap(self):
        exec('''global G
G = lambda c: {0}'''.format(self.parent.delta.text()),globals())
        ims=[]
        c = self.const
        for i in range(self.fps):
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

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

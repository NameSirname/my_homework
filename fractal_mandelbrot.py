import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QComboBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt

import numpy as np
import random

import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.image as img
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
        self.title = 'Mandelbrot'

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
        self.deph.setRange(1,200)
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
             'gist_ncar','gist_rainbow','jet',
             'hsv','cubehelix','rainbow'])        
        self.CMap.addItems(A)                  
        self.CMap.addItems(list(map(lambda x: x+'_r',A)))   
        self.CMap.addItems(my_cmaps.A)  
        self.CMap.setCurrentText('hot')
        grid.addWidget(self.CMap,4,0,1,2)
        self.CMap.activated.connect(self.CMap_act)

        self.CMap.l = QLabel('cmap')
        self.CMap.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.CMap.l,4,2,1,-1)

 ###
        Enter = QPushButton('Draw', self)
        Enter.clicked.connect(self.Enter)
        grid.addWidget(Enter,5,0,1,-1)
 ###       
        self.Width = QSpinBox(self)
        self.Width.setRange(900,1400)
        self.Width.setValue(900)
        self.Width.setSingleStep(10)
        grid.addWidget(self.Width,6,0,1,2)
        
        self.Height = QSpinBox(self)
        self.Height.setRange(700,900)
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

        self.Mp = Mplot(self)
        self.Mp.move(0,0)

        lg = QPushButton('lg', self)
        lg.clicked.connect(self.lg)
        grid.addWidget(lg,11,0,1,-1)
###
        Save = QPushButton('Save', self)
        Save.clicked.connect(self.Save)
        grid.addWidget(Save,12,0,1,-1)
        
        self.show()


    def Enter(self):
        self.Mp = Mplot(self)
        self.Mp.move(0,0)

    def Resize(self):
        self.resize(self.Width.value(),self.Height.value())
        self.move(0,0)
        self.win.resize(200,self.size().height())
        self.win.move(self.size().width()-200,0)
        
        self.Mp = Mplot(self)
        self.Mp.move(0,0)

    def Save(self):
        filename = QFileDialog.getSaveFileName(self,
                                               directory = '/home/mister/Изображения/fractals/',
                                               caption = 'save_fractal')[0]
        if filename!='':
            self.Mp.fig.savefig(filename, format='png')

    def CMap_act(self):
        self.Mp = Mplot(self, B = self.Mp.B)
        self.Mp.move(0,0)

        
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
    def __init__(self, parent,B=[]):
        self.parent = parent
        self.deph = parent.deph.value()
        self.w = parent.Width.value()-200
        self.h = parent.Height.value()

        self.a = float(parent.a.text())
        self.c = float(parent.c.text())
        self.b = round(float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)
        self.d = round(-float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)

        self.D = [self.a,self.b]
        self.B = B
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

        self.plot()

    def plot(self):
        if len(self.B)==0:
            c = self.const
            exec('''global F
F = lambda z,c:'''+ self.parent.func.text(),globals())
            #globals()['c']=c
            
            A1 = np.linspace(self.a,self.c, self.w)
            A2 = np.linspace(self.d,self.b, self.h)

            A = np.array([[complex(i,e) for i in A1] for e in A2])
                
            self.B = np.array([[0 for i in range(self.w)] for e in range(self.h)])
                
            for i in range(len(A)):
                for e in range(len(A[i])):
                    C = A[i][e]
                    N = c
                    for j in range(self.deph):
                        N = F(N,C)
                        if abs(N)>5:
                            break
                    self.B[i][e]= j#abs(N)
         
                
        self.fig.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0)
        ax = self.fig.add_subplot(111)
        ax.axis('scaled')
        ax.axis([0,self.w,0,self.h])
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.yaxis.set_major_formatter(plt.NullFormatter())
        ax.imshow(self.B, cmap = self.colorMap)
        
        self.show()

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

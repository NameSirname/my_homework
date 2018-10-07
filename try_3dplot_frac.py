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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticks

import my_cmaps

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 900
        self.height = 700
        self.title = '3D plot'

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

        self.func = QLineEdit(self)
        self.func.setText('x*x+c')
        grid.addWidget(self.func,0,0,1,-1)
        
 ###
        self.CMap = QComboBox(self)
        self.CMap.addItems(my_cmaps.A)
                            
        self.CMap.setCurrentText('hot')
        grid.addWidget(self.CMap,1,0,1,2)
        self.CMap.activated.connect(self.CMap_act)

        self.CMap.l = QLabel('cmap')
        self.CMap.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.CMap.l,1,2,1,-1)

 ###
        Enter = QPushButton('Draw', self)
        Enter.clicked.connect(self.Enter)
        grid.addWidget(Enter,2,0,1,-1)
 ###       
        self.Width = QSpinBox(self)
        self.Width.setRange(900,1400)
        self.Width.setValue(900)
        self.Width.setSingleStep(10)
        grid.addWidget(self.Width,3,0,1,2)
        
        self.Height = QSpinBox(self)
        self.Height.setRange(700,900)
        self.Height.setValue(700)
        self.Height.setSingleStep(10)
        grid.addWidget(self.Height,4,0,1,2)
        
        self.Width.l = QLabel('width')
        self.Width.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.Width.l,3,2,1,-1)
        
        self.Height.l = QLabel('height')
        self.Height.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.Height.l,4,2,1,-1)

 ###        
        Resize = QPushButton('Resize', self)
        Resize.clicked.connect(self.Resize)
        grid.addWidget(Resize,5,0,1,-1)
###
        self.a = QLineEdit('-1.5',self)
        grid.addWidget(self.a,6,0,1,1)

        self.b = QLineEdit('1.5',self)
        grid.addWidget(self.b,6,1,1,2)

        self.c = QLineEdit('-1.5',self)
        grid.addWidget(self.c,7,0,1,1)

        self.d = QLineEdit('1.5',self)
        grid.addWidget(self.d,7,1,1,2)

        self.e = QLineEdit('0',self)
        grid.addWidget(self.e,8,0,1,1)

        self.f = QLineEdit('5',self)
        grid.addWidget(self.f,8,1,1,2)

###
        Save = QPushButton('Save', self)
        Save.clicked.connect(self.Save)
        grid.addWidget(Save,9,0,1,-1)
###

        self.const_re = QSpinBox(self)
        self.const_re.setRange(-1000,1000)
        self.const_re.setValue(-745)
        grid.addWidget(self.const_re,10,0,1,2)

        self.const_im = QSpinBox(self)
        self.const_im.setRange(-1000,1000)
        self.const_im.setValue(-110)
        grid.addWidget(self.const_im,11,0,1,2)

        self.const_re.l = QLabel('real')
        self.const_re.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.const_re.l,10,2,1,-1)

        self.const_im.l = QLabel('imag')
        self.const_im.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.const_im.l,11,2,1,-1)
        
###
        self.deph = QSpinBox(self)
        self.deph.setValue(2)
        self.deph.setRange(1,1000)
        grid.addWidget(self.deph,12,0,1,2)

        self.deph.l = QLabel('deph')
        self.deph.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.deph.l,12,2,1,-1)


###
        self.Mp = Mplot(self)
        self.Mp.move(0,0)
        
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
                                               caption = 'save_function')[0]
        if filename!='':
            self.Mp.fig.savefig(filename, format='png')

    def CMap_act(self):
        self.Mp = Mplot(self, Z = self.Mp.Z)
        self.Mp.move(0,0)

        


##____________________________________________________________________________


class Mplot(FCanvas):
    def __init__(self, parent,Z=None):
        self.parent = parent
        self.w = parent.Width.value()-200
        self.h = parent.Height.value()
        self.deph = parent.deph.value()
        self.const = complex(self.parent.const_re.value()/1000
                             ,self.parent.const_im.value()/1000)        

        self.coords = [float(parent.a.text()),float(parent.b.text()),
                       float(parent.c.text()),float(parent.d.text()),
                       float(parent.e.text()),float(parent.f.text())]
        
        self.l = round(self.h*(self.coords[5]-self.coords[4])/(self.coords[3]-self.coords[2]))

        self.Z = Z
        self.colorMap = parent.CMap.currentText()

###
        self.fig = Figure(figsize = (self.w//50,self.h//50),dpi=50)

        FCanvas.__init__(self,self.fig)
        self.setParent(parent)

        FCanvas.setSizePolicy(self,
                              QSizePolicy.Expanding,
                              QSizePolicy.Expanding)
        FCanvas.updateGeometry(self)

        self.plot()

    def plot(self):
        if self.Z is None:
            global c
            c = self.const
            exec('''global F
F = lambda x:'''+ self.parent.func.text(),globals())

            
            A = np.linspace(self.coords[0],self.coords[1], self.w)
            B = np.linspace(self.coords[2],self.coords[3], self.h)
            C = np.linspace(self.coords[4],self.coords[5], self.l)

            comp = np.array([[complex(i,e) for i in A] for e in B])

            self.Z = np.array([[0 for i in range(self.w)] for e in range(self.h)])
            
            for i in range(len(comp)):
                for e in range(len(comp[i])):
                    N = comp[i][e]
                    for j in range(self.deph):
                        N = F(N)
                        if abs(N)>5:
                            break
                    self.Z[i][e] = j
            self.Z = self.Z*2.5/self.Z.max()
            self.Z = [self.Z,A,B,C]
             
        X,Y = np.meshgrid(self.Z[1],self.Z[2])      
        self.fig.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0)
        ax = self.fig.add_subplot(111, projection='3d')
        ax.axis('scaled')
        ax.axis([self.coords[0],self.coords[1],self.coords[2],self.coords[3]])
        ax.set_zlim(self.coords[4],self.coords[5])
        ax.set_xticks(self.Z[1][::50])
        ax.set_yticks(self.Z[2][::50])
        ax.set_zticks(self.Z[3][::50])

        ax.set_xlabel('real',fontsize=18)
        ax.set_ylabel('imaginary',fontsize=18)
        ax.set_zlabel('absolute',fontsize=18)
        ax.plot_surface(X,Y,self.Z[0],cmap = self.colorMap)
        
        self.show()

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel,QLineEdit
from PyQt5.QtWidgets import QGridLayout, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QComboBox
#from PyQt5.QtGui import QPainter, QColor, QPen
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

import matplotlib.cm as cm
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
 ###
        self.func = QLineEdit(self)
        self.func.setText('z*z')
        grid.addWidget(self.func,3,0,1,-1)
        
 ###
        self.CMap = QComboBox(self)
        A = ['hot','viridis','plasma','inferno',
             'flag','prism','nipy_spectral','RdYlBu',
             'BuPu','YlGnBu','ocean','gist_earth',
             'gist_ncar','gist_rainbow','jet',
             'hsv','cubehelix','rainbow',
             'Greens']
        self.CMap.addItems(A)
        self.CMap.addItems(my_cmaps.A)
        #self.CMap.addItems(['my_colormap#'])
                            
        self.CMap.setCurrentText('hot')
        grid.addWidget(self.CMap,4,0,1,2)
        self.CMap.activated.connect(self.CMap_act)

        self.CMap.l = QLabel('cmap')
        self.CMap.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.CMap.l,4,2,1,-1)

 ###
        self.dens = QSpinBox(self)
        self.dens.setRange(10,100)
        self.dens.setValue(25)
        self.dens.setSingleStep(5)
        grid.addWidget(self.dens,6,0,1,2)

        self.dens.l = QLabel('1/density')
        self.dens.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.dens.l,6,2,1,-1)
## ###
##        self.num_l = QLineEdit('60',self)
##        grid.addWidget(self.num_l,7,0,1,2)
##
##        self.width_l = QLineEdit('15',self)
##        grid.addWidget(self.width_l,7,2,1,-1)
## ###
##        Enter2 = QPushButton("Draw'", self)
##        Enter2.clicked.connect(self.CMap_act)
##        grid.addWidget(Enter2,8,0,1,-1)
 ###
        Enter = QPushButton('Draw', self)
        Enter.clicked.connect(self.Enter)
        grid.addWidget(Enter,9,0,1,-1)
 ###       
        self.Width = QSpinBox(self)
        self.Width.setRange(900,1400)
        self.Width.setValue(900)
        self.Width.setSingleStep(10)
        grid.addWidget(self.Width,10,0,1,2)
        
        self.Height = QSpinBox(self)
        self.Height.setRange(700,900)
        self.Height.setValue(700)
        self.Height.setSingleStep(10)
        grid.addWidget(self.Height,11,0,1,2)

        self.Width.l = QLabel('width')
        self.Width.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.Width.l,10,2,1,-1)
        
        self.Height.l = QLabel('height')
        self.Height.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.Height.l,11,2,1,-1)
 ###        
        Resize = QPushButton('Resize', self)
        Resize.clicked.connect(self.Resize)
        grid.addWidget(Resize,12,0,1,-1)
###
        self.a = QLineEdit('-1.5',self)
        grid.addWidget(self.a,13,0,1,1)

        self.c = QLineEdit('1.5',self)
        grid.addWidget(self.c,14,0,1,1)
        
        self.d = QLineEdit('0',self)
        grid.addWidget(self.d,14,2,1,1)

        self.d.l = QLabel('offset')
        self.d.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.d.l,13,2,1,-1)
###
        self.Mp = Mplot(self)
        self.Mp.move(0,0)

        lg = QPushButton("Lupa'n'Pupa", self)
        lg.clicked.connect(self.lg)
        grid.addWidget(lg,15,0,1,-1)

 ###
        Save = QPushButton('Save', self)
        Save.clicked.connect(self.Save)
        grid.addWidget(Save,16,0,1,-1)
        
        self.show()


    def Enter(self):
        self.Mp = Mplot(self)
        self.Mp.move(0,0)
        
    def keyPressEvent(self,e):
        if e.key()+1 == Qt.Key_Enter: ##not fixed key_events
            self.Enter()
        
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
        self.w = parent.Width.value()-200
        self.h = parent.Height.value()

        self.a = float(parent.a.text())
        self.c = float(parent.c.text())
        self.b = round(float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)
        self.d = round(-float((self.c-self.a)/2*self.h/self.w)+float(parent.d.text()),6)

        self.D = [self.a,self.b]
        self.B = B
        self.colorMap = parent.CMap.currentText()
        self.dens = parent.dens.value()
##        self.num_l = int(parent.num_l.text())
##        self.width_l = float(parent.width_l.text())

###
        self.fig = Figure(figsize = (self.w//10,self.h//10),dpi=10)

        FCanvas.__init__(self,self.fig)
        self.setParent(parent)

        FCanvas.setSizePolicy(self,
                              QSizePolicy.Expanding,
                              QSizePolicy.Expanding)
        FCanvas.updateGeometry(self)

        self.plot()

    def plot(self):
        if len(self.B)==0:
            exec('''global F
F = lambda z:'''+ self.parent.func.text(),globals())
            
            A1 = np.linspace(self.a,self.c, self.w//self.dens)
            A2 = np.linspace(self.d,self.b, self.h//self.dens)

            A = np.array([[complex(i,e) for i in A1] for e in A2])
                
            self.B = [F(A),A1,A2]
                    
                
        self.fig.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0)
        ax = self.fig.add_subplot(111)
        A1,A2 = np.meshgrid(self.B[1],self.B[2])
##        col = colors.Normalize()
##        col.autoscale(A1/sum(A1))
        ax.quiver(A1,A2,self.B[0].real,self.B[0].imag, abs(self.B[0]))#,
##                  color = cm.jet(col(1)))


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


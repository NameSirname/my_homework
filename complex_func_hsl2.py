import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel,QLineEdit,QTextEdit
from PyQt5.QtWidgets import QGridLayout, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtWidgets import QFileDialog, QComboBox
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
        self.func = QTextEdit(self)
        self.func.setText('')
        grid.addWidget(self.func,3,0,1,-1)
        
        self.func2 = QLineEdit(self)
        self.func2.setText('x')
        grid.addWidget(self.func2,4,0,1,-1)
        
 ###
        self.CMap = QComboBox(self)
        self.CMap.addItems(my_cmaps.A1)
##        A = ['hot','viridis','plasma','inferno',
##             'flag','prism','nipy_spectral','RdYlBu',
##             'BuPu','YlGnBu','ocean','gist_earth',
##             'gist_ncar','gist_rainbow','jet',
##             'hsv','cubehelix','rainbow',
##             'Greens']
##        self.CMap.addItems(A)
                            
        self.CMap.setCurrentText('WB1')
        grid.addWidget(self.CMap,5,0,1,2)
        self.CMap.activated.connect(self.CMap_act)

        self.CMap.l = QLabel('cmap')
        self.CMap.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.CMap.l,5,2,1,-1)
###

        self.alpha = QSpinBox(self)
        self.alpha.setRange(0,100)
        self.alpha.setValue(100)
        self.alpha.setSingleStep(5)
        grid.addWidget(self.alpha,6,0,1,2)

        self.alpha.l = QLabel('alpha%')
        self.alpha.l.setStyleSheet("color: rgba(255,255,255)")
        grid.addWidget(self.alpha.l,6,2,1,-1)
 ###
        self.alpha_cm = QLineEdit('0,0,0|0.5,0,0|1,0,0',self)
        grid.addWidget(self.alpha_cm,7,0,1,2)

        self.wb = QComboBox(self)
        self.wb.addItems(['wb','bw','none'])
        self.wb.setCurrentText('none')
        grid.addWidget(self.wb,7,2,1,-1)
 ###
        Enter2 = QPushButton("Draw'", self)
        Enter2.clicked.connect(self.CMap_act)
        grid.addWidget(Enter2,8,0,1,-1)
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
        
##    def keyPressEvent(self,e):
##        if e.key()+1 == Qt.Key_Enter: ##not fixed key_events
##            self.Enter()
        
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
        self.alpha = parent.alpha.value()/100
        self.wb = parent.wb.currentText()
        self.alpha_cm = parent.alpha_cm.text().split('|')


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
            func_text = '\n    '.join(self.parent.func.toPlainText().split('\n'))

            exec('''global F
def F(z):
    '''+ func_text +'''
    return z''',globals())
            
            A1 = np.linspace(self.a,self.c, self.w)
            A2 = np.linspace(self.d,self.b, self.h)

            A = np.array([[complex(i,e) for i in A1] for e in A2])
                
            self.B = F(A)#np.array([[F(A[i][j]) for j in range(len(A[i]))] for i in range(len(A))])
                    
                
        self.fig.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0)
        ax = self.fig.add_subplot(111)
        ax.axis('scaled')
        ax.axis([0,self.w,0,self.h])
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.yaxis.set_major_formatter(plt.NullFormatter())
        
###
        if self.wb=='wb':
            self.alpha_cm = [tuple(map(float,e.split(','))) for e in self.alpha_cm]
            cm. register_cmap(name = 'new', 
                  data = {'red': [(0.,0.,0.),(1.,1.,1.)],
                          'blue': [(0.,0.,0.),(1.,1.,1.)],
                          'green': [(0.,0.,0.),(1.,1.,1.)],
                          'alpha': self.alpha_cm})
        elif self.wb=='bw':
            self.alpha_cm = [tuple(map(float,e.split(','))) for e in self.alpha_cm]
            cm. register_cmap(name = 'new', 
                  data = {'red': [(0.,1.,1.),(1.,0.,0.)],
                          'blue': [(0.,1.,1.),(1.,0.,0.)],
                          'green': [(0.,1.,1.),(1.,0.,0.)],
                          'alpha': self.alpha_cm})

###
        exec('''global G
G = lambda x:'''+ self.parent.func2.text(),globals())
        
        color_func = (np.arcsin(self.B.imag/abs(self.B))-np.pi*(self.B.real<0))*((-1)**(self.B.real<0))
###
        color_func[-1][0],color_func[-1][-1] = np.pi*1.5, -np.pi*0.5
        #print(np.amax(color_func),np.amin(color_func))
        
        ax.imshow(color_func, cmap = 'rainbow_comp')
        ax.imshow(G(abs(self.B)), cmap = self.colorMap, alpha = self.alpha)
               

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


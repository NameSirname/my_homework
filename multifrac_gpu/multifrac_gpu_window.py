import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QGridLayout, QFileDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QPoint

from multifrac_gpu_make import new_F,new_G,new_H
from multifrac_gpu_widgets import *

from multifrac_gpu_plot import PLOT, reload

import multifrac_gpu_H as f_H
import multifrac_gpu_F as f_F
import multifrac_gpu_G as f_G
import multifrac_gpu_bitmap as f_bitmap

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 925
        self.height = 700
        self.toolbar_width = 225
        self.title = 'Fractal'
        
        self.zooming = False
        self.zoom_point = QPoint(0,0)
        
        self.initGUI()
                
    def initGUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0,0,self.width, self.height)

        self.toolbar = QWidget(self)
        self.toolbar.resize(self.toolbar_width,self.height)
        self.toolbar.move(self.width-self.toolbar_width,0)

        self.toolbar.setStyleSheet(".QWidget {background-color: #123;}")        
        self.palette().setColor(self.backgroundRole(), Qt.white)
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.toolbar.setLayout(self.grid)

        self.row = 5
        COLORS = sorted(['hot','viridis','plasma','inferno',
             'flag','prism','nipy_spectral','RdYlBu',
             'BuPu','YlGnBu','ocean','gist_earth',
             'gist_ncar','jet','cubehelix','rainbow'])
        COLORS.extend(list(map(lambda x: x+'_r',COLORS)))

        self.TYPES = {"Julia":'''for k in range(deph):
        z = F(z,c)
        if (abs(z)>5):
            break''',
                      "Mandelbrot":'''for k in range(deph):
        c = F(c,z)
        if (abs(c)>5):
            break
    z=c''',
                      "Spider":'''for k in range(deph):
        z = F(z,c)
        c = z+c/2
        if (abs(z)>5):
            break''',
                      "Spider2":'''c=z
    for k in range(deph):
        z = F(z,c)
        c = z+c/2
        if (abs(z)>5):
            break''',
                      "other":'''for k in range(deph):\n\t\tz = F(z,c)\n\t\tif (abs(z)>5):\n\t\t\tbreak'''}

        SIZE(self,0,3,MaxWidth = 25200, MaxHeight = 25000)
        DRAW(self,2)
        DEPH(self,4,3,MaxDeph = 10000)
        CONSTANT(self,5,3, DefaultConst = '-0.745+0.115j')
        BOUNDS(self,6,3, DefaultBounds = ['-1.5','1.5','0'])
        ZOOM(self,8)
        FUNCTIONS(self,9,
                  DefaultF = "z*z+c",
                  DefaultG = "k+np.angle(z)*deph/10/(k+2)",
                  DefaultFractalTypes = self.TYPES.keys(),
                  DefaultH = "Julia")
        EDIT(self,300,200)
        COLORMAP(self,12, DefaultMap = 'p2',DefaultColorMaps = COLORS)
        ANIMATE(self,13,3, DefaultSpeed = '250',DefaultDelta = "c*1j**0.05")
        SAVE(self,15)

#PLOT
        self.CANVAS = PLOT(self)
        self.CANVAS.move(0,0)
        self.state = 0
        
        new_F(self.F.text())
        new_G(self.G.text())
        new_H(self.TYPES[self.H.currentText()])
        reload(f_F)
        reload(f_G)
        reload(f_H)
        reload(f_bitmap)
        
        self.show()


    def Enter(self):
        self.recompile()
        self.CANVAS.ax.cla()
        self.CANVAS.pic = []
        self.CANVAS.Build()
        self.CANVAS.plot()
        self.state = 1
        if self.plot.checkState():
            self.CANVAS.draw()
        #print(self.CANVAS.ax.get_images())

    def Resize(self):
        self.width = self.Width.value()
        self.height = self.Height.value()
        self.resize(self.width,self.height)
        self.toolbar.resize(self.toolbar_width,self.height)
        self.toolbar.move(self.width-self.toolbar_width,0)

        self.CANVAS.resize(self.width-self.toolbar_width,self.height)
        self.CANVAS.move(0,0)
        self.CANVAS.w = self.width-self.toolbar_width
        self.CANVAS.h = self.height
        self.CANVAS.fig.set_size_inches(self.CANVAS.w/8,self.CANVAS.h/8)
            
        #self.move(0,0)
        
    def Animate(self):
        self.recompile()
        self.CANVAS.ax.cla()
        self.CANVAS.ims = []
        self.CANVAS.Build()
        self.CANVAS.animate()
        self.state = 2
        if self.plot.checkState():
            self.CANVAS.show()
            
    def Change_colormap(self):
        self.CANVAS.ax.cla()
        self.CANVAS.colorMap = self.CMap.currentText()
        self.CANVAS.ax.axis([0,self.CANVAS.w-1,0,self.CANVAS.h-1])
        if self.state == 1:
            self.CANVAS.plot()
            if self.plot.checkState():
                self.CANVAS.draw()
        elif self.state == 2:
            self.CANVAS.animate()
            if self.plot.checkState():
                self.CANVAS.show()

    def Change_type(self):
        if self.H.currentText() == "other":
            self.win.show()
        
    def Zoom(self):
        self.zooming = not self.zooming
        if self.zooming:
            self.CANVAS.setCursor(Qt.CrossCursor)
        else:
            self.CANVAS.unsetCursor()

    def Save(self):
        filename = QFileDialog.getSaveFileName(self,
                            directory = '/home/mister/Изображения/fractals/',
                            caption = 'save_fractal')[0]
        if filename!='':
            self.CANVAS.fig.savefig(filename, format='png')

    def SaveAnimation(self):
        filename = QFileDialog.getSaveFileName(self,
                            directory = '/home/mister/Изображения/animated_fractals/',
                            caption = 'save_animated_fractal')[0]
        if filename!='':
            self.CANVAS.Anima.save(filename, bitrate=-1)
    
    def recompile(self):
        if self.g.checkState():
            new_G(self.G.text())
            reload(f_G)
            
        if self.f.checkState():
            new_F(self.F.text())
            reload(f_F)
            
        if self.h.checkState():
            self.TYPES["other"] = "\n    ".join(self.other.toPlainText().replace('\t',"    ").split('\n'))
            new_H(self.TYPES[self.H.currentText()])
        if self.f.checkState() or self.g.checkState() or self.h.checkState():
            reload(f_H)
            reload(f_bitmap)
        return None

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    
    sys.exit(app.exec_())

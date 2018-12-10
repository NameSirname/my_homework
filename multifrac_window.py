import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QGridLayout, QFileDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from multifrac_make import new_F,new_G,new_H, comp_le
from multifrac_widgets import *
from multifrac_plot import PLOT

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 925
        self.height = 700
        self.toolbar_width = 225
        self.title = 'Fractal'
        
        self.initGUI()
                
    def initGUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.toolbar = QWidget(self)
        self.toolbar.resize(self.toolbar_width,self.size().height())
        self.toolbar.move(self.width-self.toolbar_width,0)

        self.toolbar.setStyleSheet("""
            .QWidget {
                background-color: #123;}""")
        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(pal)
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.toolbar.setLayout(self.grid)

        self.row = 5
        A = sorted(['hot','viridis','plasma','inferno',
             'flag','prism','nipy_spectral','RdYlBu',
             'BuPu','YlGnBu','ocean','gist_earth',
             'gist_ncar','jet','cubehelix','rainbow'])
        A.extend(list(map(lambda x: x+'_r',A)))

        SIZE(self,0,3,MaxWidth = 25200, MaxHeight = 25000)
        DRAW(self,2)
        DEPH(self,4,3,MaxDeph = 10000)
        CONSTANT(self,5,3, DefaultConst = '-0.745+0.115j')
        BOUNDS(self,6,3, DefaultBounds = ['-1.5','1.5','0'])
        LUPA(self,8)
        FUNCTIONS(self,9,
                  DefaultF = 'z*z+c',
                  DefaultG = 'i+cabs(z)*(deph/10/(i+1))',
                  DefaultH = '''int k;
for (k=1;k<=deph;k++){
z = F(z,c);
if (cabs(z)>5) break;
}''')
        COLORMAP(self,12, DefaultMap = 'p2',DefaultColorMaps = A)
        ANIMATE(self,13,3, DefaultSpeed = '250',DefaultDelta = 'c-0.01j')
        SAVE(self,15)

#PLOT
        self.CANVAS = PLOT(self)
        self.CANVAS.move(0,0)
        self.i=False
        self.state = 0
        
        
        new_F(self.F.text())
        new_G(self.G.text())
        new_H('\n\t'.join(self.H.toPlainText().split('\n')))
        comp_le()
        
        self.show()


    def Enter(self):
        self.recompile()
        self.CANVAS.close()
        self.CANVAS = PLOT(self, ims = self.CANVAS.ims)
        self.CANVAS.move(0,0)
        self.CANVAS.plot()
        self.state = 1
        if self.plot.checkState():
            self.CANVAS.show()

    def Resize(self):
        self.resize(self.Width.value(),self.Height.value())
        self.move(0,0)
        self.toolbar.resize(self.toolbar_width,self.Height.value())
        self.toolbar.move(self.Width.value()-self.toolbar_width,0)

        self.CANVAS.close()
        self.CANVAS = PLOT(self)
        self.CANVAS.move(0,0)
        self.state = 0
            
    def Animate(self):
        self.recompile()
        self.CANVAS.close()
        self.CANVAS = PLOT(self, pic = self.CANVAS.pic)
        self.CANVAS.move(0,0)
        self.CANVAS.animate()
        self.state = 2
        if self.plot.checkState():
            self.CANVAS.show()
            
    def Change_colormap(self):
        self.CANVAS.close()
        self.CANVAS = PLOT(self, pic = self.CANVAS.pic, ims = self.CANVAS.ims)
        self.CANVAS.move(0,0)
        if self.state == 1:
            self.CANVAS.plot()
        elif self.state == 2:
            self.CANVAS.animate()
        if self.plot.checkState():
            self.CANVAS.show()
        
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
            self.CANVAS.Anima.save(filename)

        
    def lupa(self):
        self.i = not self.i
        if self.i:
            QApplication.setOverrideCursor(Qt.CrossCursor)
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
    
    def find(self,a,b,c,d):       
        self.a.setText(str(round(a,6)))
        self.c.setText(str(round(c,6)))
        self.d.setText(str(round((b+d)/2,6)))

    def recompile(self):
        if self.g.checkState():
            new_G(self.G.text())
            comp_le()
            
        if self.f.checkState():
            new_F(self.F.text())
            comp_le()
            
        if self.h.checkState():
            new_H('\n\t'.join(self.H.toPlainText().split('\n')))
            comp_le()
        return None


        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    
    sys.exit(app.exec_())

#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QGridLayout, QFileDialog

from widgetsNew import *
from time import sleep


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 950
        self.height = 750
        self.tbwidth = 250
        self.side = 40
        self.wL = 10
        self.hL = 15
        self.title = 'labirint'

        self.state = False
        self.finish = False
        self.edit = False
        self.counter = 0
        self.moves = 0

        self.Lab = []
        self.exit = (0,self.wL,0)
        self.x = self.hL-1
        self.y = 0
        self.z = 0
        
        self.var = [-1,-1]
        self.tip = [(-1,0),(-1,0)]
        self.prev = -1
        
        self.initGUI()
                
    def initGUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.win = QWidget(self)
        self.win.resize(self.tbwidth,self.height)
        self.win.move(self.width-self.tbwidth,0)
        self.win.setObjectName("window")

        QSS = '''
        .QLabel {
            color: white;
            font-weight: bold;
        }
        .QWidget#window {
            background-color: #123;
        }
        '''
        self.win.setStyleSheet(QSS)
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.win.setLayout(self.grid)
        self.row = 5

        self.icons = [u"↑",u"↖",u"↗",u"A",u"B",u"*"]
        self.func = [lambda x,y,z,t=1: (t*(x+(z%2-1)*(-1)**(z//2%2)) + (t-1),
                                        t*(y-(z%2)*(-1)**(z//2%2)) + (t-1), z),
                     lambda x,y,z,t=1: (x,y,(z+1)%4),
                     lambda x,y,z,t=1: (x,y,(z-1)%4),
                     lambda x,y,z,t=1: (x,y,z),
                     lambda x,y,z,t=1: (x,y,z)]
        self.N = len(self.icons) - 3
        self.proc = [0]*(self.N+2)
        self.buttons = []
                
        SIZE(self,0,3,MaxWidth = 25200, MaxHeight = 25000)
        LAB_SIZE(self,3,3)
        ACTIONS(self,7)
        START(self,11,2)
        GRAPHICS(self)
        LAB_EDIT(self,15,3)

        self.show()
        
    def Resize(self):
        self.width = self.Width.value()
        self.height = self.Height.value()
        
        self.resize(self.width,self.height)
##        self.move(0,0)
        self.win.resize(self.tbwidth,self.height)
        self.win.move(self.width-self.tbwidth,0)
        
        self.view.resize(self.width-self.tbwidth,self.height)
        self.view.move(0,0)
        return None

    def ResizeLab(self):
        if not self.state:
            self.hL = self.LabHeight.value()
            self.wL = self.LabWidth.value()

            self.startX.setRange(0,self.hL-1)
            self.startY.setRange(0,self.wL-1)
            self.dens0.setRange(0,self.wL*(self.hL-1)//2)
            self.dens1.setRange(0,(self.wL-1)*self.hL//2)

            self.scene.clear()
            self.view.Generate()
##            self.view.fitInView(10,10,700,700,Qt.KeepAspectRatio)
##            self.view.setAlignment(Qt.AlignCenter)
##            self.view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        return None

    def RandLab(self):
        if not self.state:
##            self.scene.clear()
            self.view.Generate()                
            B = smp(range(0,self.wL*(self.hL-1)-1),self.dens0.value())
            for i in range(self.dens0.value()):
                repaintL(self,B[i]//self.wL+1,B[i]%self.wL,
                         self.hL,self.wL,0)
                
            B = smp(range(0,(self.wL-1)*self.hL-1),self.dens1.value())
            for i in range(self.dens1.value()):
                repaintL(self,B[i]//(self.wL-1),B[i]%(self.wL-1)+1,
                         self.hL,self.wL,1)
        return None

    def LabEdit(self):
        if not self.state:
            self.edit = not self.edit
            if self.edit: self.lab_edit.setStyleSheet("color: red;")
            else: self.lab_edit.setStyleSheet("color: black;")
        return None

    def Load(self):
        if not self.state:
            filename = QFileDialog.getOpenFileName(self,
                                directory = '/home/mister_u/PyProj/game2/',
                                caption = 'load labirint')[0]
            if filename!='':
                file = open(filename,'r')
                self.wL,self.hL = map(int,file.readline().split())
                self.LabHeight.setValue(self.hL)
                self.LabWidth.setValue(self.wL)
                self.ResizeLab()

                self.scene.clear()
                self.view.Generate()
                for i in range(self.hL+1):
                    self.Lab[i] = list(map(lambda x: list(map(int,x.split('_'))),
                                           file.readline().split()))
                for i in range(1,self.hL):
                    for j in range(self.wL):
                        if self.Lab[i][j][0] == 1:
                            repaintL(self,i,j,self.hL,self.wL,0,0)
                for i in range(self.hL):
                    for j in range(1,self.wL):
                        if self.Lab[i][j][1] == 1:
                            repaintL(self,i,j,self.hL,self.wL,1,0)
                file.close()
        return None
    
    def Save(self):
        filename = QFileDialog.getSaveFileName(self,
                            directory = '/home/mister_u/PyProj/game2/',
                            caption = 'save labirint')[0]
        if filename!='':
            file = open(filename,'w')
            file.write(str(self.wL)+' '+str(self.hL)+'\n')
            for i in range(self.hL+1):
                for j in range(self.wL+1):
                    file.write(str(self.Lab[i][j][0])+'_'+str(self.Lab[i][j][1])+' ')
                file.write('\n')
            file.close()
        return None

    def Automat(self):
        if not self.state:
            moves = 0
            proc = np.zeros([self.N+2])
            for n in range(self.numGames.value()):
                self.Start()
                while self.finish == False:
                    for i in range(len(self.tip)):
                        for j in range(self.tip[i][1]):
                            self.Buttons(self.tip[i][0])
    ##                        self.buttons[self.tip[i][0]].pressed.emit()
    ##                    sleep(1)
                    self.Random()
                moves += self.moves-1
                proc += self.proc
                self.Start()
                print('\n')
            proc /= self.numGames.value()
            self.log.setText(str(round(moves/self.numGames.value(),3))+' ['+
                             '|'.join(list(map(lambda x: str(round(x,2)),proc)))+']')
        return None
        
    def Start(self):
        if self.state:
            x,y,z = self.startX.value(),self.startY.value(),self.startZ.value()
            self.state = not self.state
            self.log.setStyleSheet("color: black;")
            self.log.setText("#")
            self.moves = 0
            self.proc = [0]*(self.N+2)
            self.scene.items()[pos(self.x,self.y,self.hL,self.wL)].setBrush(self.brush)
            self.x = x
            self.y = y
            self.z = z
            self.scene.items()[pos(x,y,self.hL,self.wL)].setBrush(self.c_unit)
            self.point.setPos(y*self.side+(0.5-(z%2)*(-1)**(z//2%2))*self.side//2,
                              x*self.side+(0.5+(z%2-1)*(-1)**(z//2%2))*self.side//2)
        else:
            if self.edit:
                self.log.setStyleSheet("color: red;")
                self.log.setText("editing")
                return None
            
            if (self.A.checkState() and self.B.checkState() and
                check(self.selectA.text(),self.N) and check(self.selectB.text(),self.N+1)):
                self.func[self.N] = lambda x,y,z,t=1: self.Parse(x,y,z,self.selectA.text())
                self.func[self.N+1] = lambda x,y,z,t=1: self.Parse(x,y,z,self.selectB.text())
                self.state = not self.state
                self.finish = False
                self.log.setStyleSheet("color: black;")
                self.Random()
            else:
                self.log.setStyleSheet("color: red;")
                self.log.setText("select A and B")
        return None

    def Random(self):
        self.counter = 0
        self.var[0] = rnd(0,self.N+2)
        self.var[1] = rnd(0,self.N+2)
        if self.state: self.moves+=1
        self.log.setStyleSheet("color: black;")
        self.log.setText("")
        x,y = TIP(self,self.writer.checkState())
        if (x,y) == (-1,-1):
            self.Log.setText("no exit")
            return None
        self.Log.setText(self.icons[self.var[0]]+" | "+
                         self.icons[self.var[1]]+" ("+x+" "+y+")")
        return None
    
    def Buttons(self,i):
        if self.state:
            if self.counter<2 or self.N+2 in self.var:
                x,y,z = self.x,self.y,self.z
                t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
                x,y,z = self.func[i](self.x,self.y,self.z,t)
                if (0<=x<self.hL and 0<=y<self.wL and
                    ((i in self.var and self.N+2 not in self.var)
                     or (self.N+2 in self.var and
                         (i in self.var or self.prev in self.var or
                          self.var==[self.N+2,self.N+2] or self.counter==0)
                         and ((self.counter<6 and self.prev == i) or
                              (not(self.prev==i and self.var!=[i,i])
                               and self.counter<2))))):
                    self.log.setStyleSheet("color: black;")
                    self.log.setText("")
                    if self.counter>0:
                        if self.prev !=i : self.prev = -1
                    else: self.prev = i
                    self.counter+=1
                    self.proc[i]+=1
                    self.scene.items()[pos(self.x,self.y,self.hL,self.wL)].setBrush(self.brush)
                    self.x=x
                    self.y=y
                    self.z=z
                    self.scene.items()[pos(x,y,self.hL,self.wL)].setBrush(self.c_unit)
                    self.point.setPos(y*self.side+(0.5-(z%2)*(-1)**(z//2%2))*self.side//2,
                                      x*self.side+(0.5+(z%2-1)*(-1)**(z//2%2))*self.side//2)
                    if (x,y,z) == self.exit and not self.finish:
                        self.finish = True
                        print("\nwin in %d moves" % self.moves)
                        print(*self.proc)
                else:
                    self.log.setStyleSheet("color: red;")
                    self.log.setText("denied")
            else:
                self.log.setStyleSheet("color: red;")
                self.log.setText("max 2 moves")
        elif self.A.checkState() and not self.B.checkState() and i<self.N:
            self.selectA.setText(self.selectA.text()+str(i+1))
        elif self.B.checkState() and not self.A.checkState() and i<=self.N:
            self.selectB.setText(self.selectB.text()+str(i+1))
        return None

    def Parse(self,x,y,z,string):
        for i in string:
            t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
            x,y,z = self.func[int(i)-1](x,y,z,t)
            if (x,y,z) == self.exit: return (x,y,z)
            if not (0<=x<self.hL and 0<=y<self.wL): return (-1,-1,-1)
        return (x,y,z)

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())


from PyQt5.QtWidgets import QLineEdit, QTextEdit, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QGridLayout, QSpinBox, QComboBox, QCheckBox
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView
from PyQt5.QtGui import QCursor, QPen, QBrush, QColor

from random import randint as rnd
from random import sample as smp

from labirint2 import *

class QGraphicsView(QGraphicsView):
    def __init__ (self, scene, parent=None):
        super(QGraphicsView, self).__init__(scene,parent)
        self.p = parent
        self.s = scene

    def Generate(self):
        self.p.Lab = ([[-1]*(self.p.wL+2)]+
                      [([-1]+[0]*self.p.wL+[-1])for j in range(self.p.hL)]+
                      [[-1]*(self.p.wL+2)])
##        self.p.x, self.p.y, self.p.z = self.p.hL-1,0,0
        self.p.x, self.p.y, self.p.z = (self.p.startX.value(),
                                        self.p.startY.value(),
                                        self.p.startZ.value())
        self.p.exit = (0,self.p.wL)
        self.p.Lab[self.p.exit[0]][self.p.exit[1]] = 0
##        x,y = 0,1+rnd(0,self.p.wL-1)
##        self.p.Lab[x][y] = 0
##        self.p.exit = (x,y)

##
##        side1 = (self.p.width-self.p.tbwidth)//(self.p.wL+2)
##        side2 = self.p.height//(self.p.hL+2)
        for i in range(self.p.hL+2):
            for j in range(self.p.wL+2):
                if self.p.Lab[i][j]==-1: self.p.brush.setColor(self.p.c_wall)
                else: self.p.brush.setColor(self.p.c_def)
                self.s.addRect(j*self.p.side,i*self.p.side,self.p.side,self.p.side,
                                   self.p.pen, self.p.brush)
        self.s.items()[pos(self.p.x,self.p.y,self.p.hL,self.p.wL)].setBrush(self.p.c_unit)
        z = self.p.z
        self.p.point = QGraphicsTextItem("#")
        self.p.point.setPos((self.p.y+1)*self.p.side+(0.5-(z%2)*(-1)**(z//2%2))*self.p.side//2,
                          (self.p.x+1)*self.p.side+(0.5+(z%2-1)*(-1)**(z//2%2))*self.p.side//2)
        self.s.addItem(self.p.point)
        return None
    
    def mousePressEvent(self,event):
        if self.p.edit:
            x,y = self.mapToScene(event.pos()).x(),self.mapToScene(event.pos()).y()
            if 0<=x<(self.p.wL+2)*self.p.side and 0<=y<(self.p.hL+2)*self.p.side:
                x = int(x//self.p.side)
                y = int(y//self.p.side)
                if 0<x<self.p.wL+1 and 0<y<self.p.hL+1 and self.p.Lab[y][x]==-1:
                    self.p.Lab[y][x] = 0;
                    self.s.items()[pos(y-1,x-1,self.p.hL,self.p.wL)+1].setBrush(self.p.c_def)
                elif y!=0 and (y-1,x-1)!=(self.p.x,self.p.y) and self.p.Lab[y][x]==0:
                    self.p.Lab[y][x] = -1;
                    self.s.items()[pos(y-1,x-1,self.p.hL,self.p.wL)+1].setBrush(self.p.c_wall)
        return None

def SIZE(self,position, rows, MaxWidth = 50000,MaxHeight = 50000):
    self.Width = QSpinBox(self)
    self.Width.setRange(self.width,MaxWidth)
    self.Width.setValue(self.width)
    self.Width.setSingleStep(10)
    self.grid.addWidget(self.Width,position,0,1,rows)
    
    self.Height = QSpinBox(self)
    self.Height.setRange(self.height,MaxHeight)
    self.Height.setValue(self.height)
    self.Height.setSingleStep(10)
    self.grid.addWidget(self.Height,position+1,0,1,rows)

    self.Width.l = QLabel('width')
    self.grid.addWidget(self.Width.l,position,rows,1,self.row-rows)
    
    self.Height.l = QLabel('height')
    self.grid.addWidget(self.Height.l,position+1,rows,1,self.row-rows)
    
    Resize = QPushButton('Resize', self)
    Resize.clicked.connect(self.Resize)
    self.grid.addWidget(Resize,position+2,0,1,self.row)
    return None

def LAB_SIZE(self,position, rows, MaxSize = 100):
    self.LabWidth = QSpinBox(self)
    self.LabWidth.setValue(self.wL)
    self.LabWidth.setRange(1,MaxSize)
    self.grid.addWidget(self.LabWidth,position,0,1,rows)

    self.LabWidth.l = QLabel('lab_width')
    self.grid.addWidget(self.LabWidth.l,position,rows,1,self.row-rows)
    
    self.LabHeight = QSpinBox(self)
    self.LabHeight.setValue(self.hL)
    self.LabHeight.setRange(1,MaxSize)
    self.grid.addWidget(self.LabHeight,position+1,0,1,rows)

    self.LabHeight.l = QLabel('lab_height')
    self.grid.addWidget(self.LabHeight.l,position+1,rows,1,self.row-rows)
    
    self.startX = QSpinBox(self)
    self.startX.setValue(self.hL-1)
    self.startX.setRange(0,self.hL-1)
    self.grid.addWidget(self.startX,position+2,0,1,1)

    self.startY = QSpinBox(self)
    self.startY.setValue(0)
    self.startY.setRange(0,self.wL-1)
    self.grid.addWidget(self.startY,position+2,1,1,1)

    self.startZ = QSpinBox(self)
    self.startZ.setValue(0)
    self.startZ.setRange(0,3)
    self.grid.addWidget(self.startZ,position+2,2,1,1)

    startL = QLabel('start_pos')
    self.grid.addWidget(startL,position+2,3,1,self.row-3)
    
    ResizeLab = QPushButton('ResizeLab', self)
    ResizeLab.clicked.connect(self.ResizeLab)
    self.grid.addWidget(ResizeLab,position+3,0,1,self.row)
    return None

def ACTIONS(self,position):
    for i in range(self.N):
        self.buttons.append(QPushButton(self.icons[i],self))
        self.buttons[i].pressed.connect(lambda x=i: self.Buttons(x))
        self.grid.addWidget(self.buttons[i],position,i,1,1)

    self.buttons.append(QPushButton("A",self))
    self.buttons[self.N].pressed.connect(lambda x=self.N: self.Buttons(x))
    self.grid.addWidget(self.buttons[self.N],position+1,0,1,1)
    self.A = QCheckBox(self)
    self.A.setCheckState(0);
    self.grid.addWidget(self.A,position+1,1,1,1)

    self.buttons.append(QPushButton("B",self))
    self.buttons[self.N+1].pressed.connect(lambda x=self.N+1: self.Buttons(x))
    self.grid.addWidget(self.buttons[self.N+1],position+1,2,1,1)
    self.B = QCheckBox(self)
    self.B.setCheckState(0);
    self.grid.addWidget(self.B,position+1,3,1,1)

    self.selectA = QLineEdit("",self)
    self.grid.addWidget(self.selectA,position+2,0,1,self.row)
    
    self.selectB = QLineEdit("",self)
    self.grid.addWidget(self.selectB,position+3,0,1,self.row)
    return None    

def START(self,position,rows):
    Random = QPushButton('Random', self)
    Random.clicked.connect(self.Random)
    self.grid.addWidget(Random,position,0,1,self.row)

    Start = QPushButton('(Re)Start', self)
    Start.clicked.connect(self.Start)
    self.grid.addWidget(Start,position+1,0,1,self.row)

    Automat = QPushButton('Automat', self)
    Automat.clicked.connect(self.Automat)
    self.grid.addWidget(Automat,position+2,0,1,self.row-rows)

    self.numGames = QSpinBox(self)
    self.numGames.setRange(1,100)
    self.numGames.setValue(1)
    self.numGames.setSingleStep(1)
    self.grid.addWidget(self.numGames,position+2,self.row-rows,1,rows)
    
    self.Log = QLineEdit("-1 | -1",self)
    self.grid.addWidget(self.Log,position+3,0,1,rows)

    self.log = QLineEdit("#",self)
    self.grid.addWidget(self.log,position+3,rows,1,self.row-rows)
    return None

def GRAPHICS(self):
    self.scene = QGraphicsScene(self)
    self.view = QGraphicsView(self.scene, self)
    self.view.resize(self.width-self.tbwidth,self.height)
    self.view.move(0,0)
    
    self.c_wall = QColor(111,222,000)
    self.c_def = QColor(205,205,205)
    self.c_unit = QColor(0,255,255)
    self.pen = QPen(QColor(11,22,33),3)
    self.brush = QBrush(self.c_wall)
    self.view.Generate()
    return None

def LAB_EDIT(self,position, rows):
    RandLab = QPushButton('RandLab', self)
    RandLab.clicked.connect(self.RandLab)
    self.grid.addWidget(RandLab,position,0,1,self.row-2)
    
    self.dens = QSpinBox(self)
    self.dens.setValue(20)
    self.dens.setRange(1,self.wL*self.hL//4)
    self.grid.addWidget(self.dens,position,self.row-2,1,2)

    self.lab_edit = QPushButton('LabEdit', self)
    self.lab_edit.clicked.connect(self.LabEdit)
    self.grid.addWidget(self.lab_edit,position+1,0,1,rows)
    
    Clear = QPushButton('Clear', self)
    Clear.clicked.connect(self.ResizeLab)
    self.grid.addWidget(Clear,position+1,rows,1,self.row-rows)

    Load = QPushButton('Load', self)
    Load.clicked.connect(self.Load)
    self.grid.addWidget(Load,position+2,0,1,rows)
    
    Save = QPushButton('Save', self)
    Save.clicked.connect(self.Save)
    self.grid.addWidget(Save,position+2,rows,1,self.row-rows)
    return None

from PyQt5.QtWidgets import QLineEdit, QTextEdit, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QGridLayout, QSpinBox, QComboBox, QCheckBox
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView
from PyQt5.QtGui import QCursor, QPen, QBrush, QColor

from random import randint as rnd
from random import sample as smp

from labirintNew import *

class QGraphicsView(QGraphicsView):
    def __init__ (self, scene, parent=None):
        super(QGraphicsView, self).__init__(scene,parent)
        self.p = parent
        self.s = scene

    def Generate(self):
        h = self.p.hL
        w = self.p.wL
        side = self.p.side
        wP = self.p.wP
        self.s.setSceneRect(-wP,-wP,2*wP+w*side,2*wP+h*side)
        
        self.p.Lab = np.zeros([h+1,w+1,2],dtype = int)
        for i in range(w):
            self.p.Lab[0][i][0] = 1
            self.p.Lab[h][i][0] = 1
            
        for i in range(h):
            self.p.Lab[i][0][1] = 1
            self.p.Lab[i][w][1] = 1
            
        self.p.xyz = [self.p.coords[i].value() for i in range(3)]
        self.p.exit = [0,self.p.coords[3].value(),0]
        self.p.Lab[self.p.exit[0]][self.p.exit[1]][self.p.exit[2]] = 0 ###

        
        for i in range(h):
            for j in range(w):
                self.s.addRect((w-j-1)*side,(h-i-1)*side,side,side,self.p.pen,self.p.brush)

        for i in range(h): ## vertical lines
            for j in range(w+1):
                x,y = h-i-1, w-j
                if self.p.Lab[x][y][1] == 1: 
                    self.p.pen.setColor(self.p.c_wall)
                else:
                    self.p.pen.setColor(self.p.c_def)
                self.s.addLine(y*side,x*side,y*side,(x+1)*side,self.p.pen)

        for i in range(h+1): ## horizontal lines
            for j in range(w):
                x,y = h-i,w-j-1
                if self.p.Lab[x][y][0] == 1: 
                    self.p.pen.setColor(self.p.c_wall)
                else:
                    self.p.pen.setColor(self.p.c_def)
                self.s.addLine(y*side,x*side,(y+1)*side,x*side,self.p.pen)

        x,y,z = self.p.xyz
        self.p.point = QGraphicsTextItem("#")
        self.p.point.setPos(y*side+(0.5-(z%2)*(-1)**(z//2%2))*side//2,
                          x*side+(0.5+(z%2-1)*(-1)**(z//2%2))*side//2)
        self.s.addItem(self.p.point)

        self.s.items()[pos(x,y,h,w)].setBrush(self.p.c_unit)
        return None
    
    def mousePressEvent(self,event):
        if self.p.edit:
            h = self.p.hL
            w = self.p.wL
            side = self.p.side
            x,y = self.mapToScene(event.pos()).x(),self.mapToScene(event.pos()).y()
            if 0<=x<=(w+1)*side and 0<=y<=(h+1)*side:
                Y,X = (x%side)/side,(y%side)/side
                y,x = int(x//side),int(y//side)
                if X>Y and (X+Y<1) and y>0:
                    repaintL(self.p,x,y,h,w,1) #this vertical
                elif X<=Y and (X+Y<1) and x>0:
                    repaintL(self.p,x,y,h,w,0) #this horizontal
                elif X<=Y and (X+Y>=1) and y<w-1:
                    repaintL(self.p,x,y+1,h,w,1) #that vertical
                elif X>Y and (X+Y>=1) and x<h-1:
                    repaintL(self.p,x+1,y,h,w,0) #that horizontal
        return None

def repaintL(self,x,y,h,w,i,k=1):
    if k:
        if self.Lab[x][y][i] == 1:
            self.pen.setColor(self.c_def)
        else:
            self.pen.setColor(self.c_wall)
    else:
        if self.Lab[x][y][i] == 0:
            self.pen.setColor(self.c_def)
        else:
            self.pen.setColor(self.c_wall)
    self.scene.items()[x*(w+i)+y+1+i*(h+1)*w].setPen(self.pen)
    if k: self.Lab[x][y][i] = 1-self.Lab[x][y][i]
    return None

def SIZE(self,position, rows, MinWidth = 750,MinHeight = 750,
         MaxWidth = 50000,MaxHeight = 50000):
    self.Width = QSpinBox(self)
    self.Width.setRange(MinWidth,MaxWidth)
    self.Width.setValue(self.width)
    self.Width.setSingleStep(10)
    self.grid.addWidget(self.Width,position,0,1,rows)
    
    self.Height = QSpinBox(self)
    self.Height.setRange(MinHeight,MaxHeight)
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

    DefaultValues = [self.hL-1,0,0,self.wL-1]
    DefaultRanges = [self.hL-1,self.wL-1,3,self.wL-1]
    for i in range(3):
        self.coords[i] = QSpinBox(self)
        self.coords[i].setValue(DefaultValues[i])
        self.coords[i].setRange(0,DefaultRanges[i])
        self.grid.addWidget(self.coords[i],position+2,i,1,1)

    startL = QLabel('st/fin')
    self.grid.addWidget(startL,position+2,3,1,self.row-4)

    self.coords[3] = QSpinBox(self)
    self.coords[3].setValue(DefaultValues[3])
    self.coords[3].setRange(0,DefaultRanges[3])
    self.grid.addWidget(self.coords[3],position+2,self.row-1,1,1)
    
    ResizeLab = QPushButton('ResizeLab', self)
    ResizeLab.clicked.connect(self.ResizeLab)
    self.grid.addWidget(ResizeLab,position+3,0,1,self.row)
    return None

def ACTIONS(self,position):
    for i in range(self.N):
        self.buttons[i] = QPushButton(self.icons[i],self)
        self.buttons[i].pressed.connect(lambda x=i: self.Buttons(x))
        self.grid.addWidget(self.buttons[i],position,i,1,1)

    self.buttons[self.N] = QPushButton("A",self)
    self.buttons[self.N].pressed.connect(lambda x=self.N: self.Buttons(x))
    self.grid.addWidget(self.buttons[self.N],position+1,0,1,1)
    self.A = QCheckBox(self)
    self.A.setCheckState(0);
    self.grid.addWidget(self.A,position+1,1,1,1)

    self.buttons[self.N+1] = QPushButton("B",self)
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
    self.grid.addWidget(self.numGames,position+2,self.row-rows,1,rows-1)

    self.writer = QCheckBox(self)
    self.writer.setCheckState(0);
    self.grid.addWidget(self.writer,position+2,self.row-1,1,1)
    
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
    
    self.c_wall = QColor(11,22,33) #QColor(111,222,000)
    self.c_def = QColor(195,195,195)
    self.c_unit = QColor(0,255,255)
    self.pen = QPen(self.c_def,self.wP*2)
    self.brush = QBrush(QColor(225,225,225))
    self.view.Generate()
    return None

def LAB_EDIT(self,position, rows):
    RandLab = QPushButton('RandLab', self)
    RandLab.clicked.connect(self.RandLab)
    self.grid.addWidget(RandLab,position,0,1,self.row-2)
    
    self.dens0 = QSpinBox(self)
    self.dens0.setValue(20)
    self.dens0.setRange(0,self.wL*(self.hL-1)//2)
    self.grid.addWidget(self.dens0,position,self.row-2,1,1)
    
    self.dens1 = QSpinBox(self)
    self.dens1.setValue(20)
    self.dens1.setRange(0,(self.wL-1)*self.hL//2)
    self.grid.addWidget(self.dens1,position,self.row-1,1,1)

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

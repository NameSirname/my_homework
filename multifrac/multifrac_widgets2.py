from PyQt5.QtWidgets import QLineEdit, QTextEdit, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QGridLayout, QSpinBox, QComboBox, QCheckBox

import my_cmaps


def DRAW(self,position):
    Resize = QPushButton('Resize', self)
    Resize.clicked.connect(self.Resize)
    self.grid.addWidget(Resize,position,0,1,self.row)
    
    Enter = QPushButton('Draw', self)
    Enter.clicked.connect(self.Enter)
    self.grid.addWidget(Enter,position+1,0,1,self.row-1)

    self.plot = QCheckBox(self)
    self.plot.setCheckState(2);
    self.grid.addWidget(self.plot,position+1,self.row-1,1,1)
    return None

def LUPA(self,position):
    Lupa = QPushButton("Lupa'n'Pupa", self)
    Lupa.clicked.connect(self.lupa)
    self.grid.addWidget(Lupa,position,0,1,self.row)
    return None

def SAVE(self,position):
    Save = QPushButton('Save', self)
    Save.clicked.connect(self.Save)
    self.grid.addWidget(Save,position,0,1,self.row)
    
    SaveAnim = QPushButton('SaveAnimation', self)
    SaveAnim.clicked.connect(self.SaveAnimation)
    self.grid.addWidget(SaveAnim,position+1,0,1,self.row)
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
    self.Width.l.setStyleSheet("color: rgba(255,255,255)")
    self.grid.addWidget(self.Width.l,position,rows,1,self.row-rows)
    
    self.Height.l = QLabel('height')
    self.Height.l.setStyleSheet("color: rgba(255,255,255)")
    self.grid.addWidget(self.Height.l,position+1,rows,1,self.row-rows)
    return None

def DEPH(self,position, rows, MaxDeph = 10000):
    self.deph = QSpinBox(self)
    self.deph.setValue(2)
    self.deph.setRange(1,MaxDeph)
    self.grid.addWidget(self.deph,position,0,1,rows)

    self.deph.l = QLabel('deph')
    self.deph.l.setStyleSheet("color: rgba(255,255,255)")
    self.grid.addWidget(self.deph.l,position,rows,1,self.row-rows)
    return None

def CONSTANT(self,position,rows, DefaultConst = '-0.745+0.115j'):
    self.const = QLineEdit(DefaultConst,self)
    self.grid.addWidget(self.const,position,0,1,rows)
    
    self.const_l = QLabel('constant')
    self.const_l.setStyleSheet("color: rgba(255,255,255)")
    self.grid.addWidget(self.const_l,position,rows,1,self.row-rows)
    return None

def FUNCTIONS(self,position,
              DefaultF = "z*z+c",
              DefaultG = "i+cabs(z)*(deph/10/(i+1))",
              DefaultFractalTypes = ["Julia", "Mandelbrot",
                                     "Spider","other"],
              DefaultH = "Julia"):
    self.F = QLineEdit(self)
    self.F.setText(DefaultF)
    self.grid.addWidget(self.F,position,0,1,self.row-1)

    self.f = QCheckBox(self)
    self.f.setCheckState(0);
    self.grid.addWidget(self.f,position,self.row-1,1,1)

    self.G = QLineEdit(self)
    self.G.setText(DefaultG)
    self.grid.addWidget(self.G,position+1,0,1,self.row-1)

    self.g = QCheckBox(self)
    self.g.setCheckState(0);
    self.grid.addWidget(self.g,position+1,self.row-1,1,1)

    self.H = QComboBox(self)
    self.H.addItems(DefaultFractalTypes)
    self.H.setCurrentText(DefaultH)
    self.H.activated.connect(self.Change_type)
    self.grid.addWidget(self.H,position+2,0,1,self.row-1)

    self.h = QCheckBox(self)
    self.h.setCheckState(0);
    self.grid.addWidget(self.h,position+2,self.row-1,1,1)
    return None

def BOUNDS(self,position,rows, DefaultBounds = ['-1.5','1.5','0']):
    self.a = QLineEdit(DefaultBounds[0],self)
    self.grid.addWidget(self.a,position,0,1,rows)

    self.c = QLineEdit(DefaultBounds[1],self)
    self.grid.addWidget(self.c,position+1,0,1,rows)
    
    self.d = QLineEdit(DefaultBounds[2],self)
    self.grid.addWidget(self.d,position+1,rows,1,self.row-rows)

    self.d.l = QLabel('offset')
    self.d.l.setStyleSheet("color: rgba(255,255,255)")
    self.grid.addWidget(self.d.l,position,rows,1,self.row-rows)
    return None

def COLORMAP(self,position,DefaultMap = 'p2', DefaultColorMaps = []):
    self.CMap = QComboBox(self)
    self.CMap.addItems(DefaultColorMaps)
    self.CMap.addItems(my_cmaps.A)
                        
    self.CMap.setCurrentText(DefaultMap)
    self.CMap.activated.connect(self.Change_colormap)
    self.grid.addWidget(self.CMap,position,0,1,self.row-1)

    self.CMap.l = QLabel('cmap')
    self.CMap.l.setStyleSheet("color: rgba(255,255,255)")
    self.grid.addWidget(self.CMap.l,position,self.row-1,1,1)
    return None

def ANIMATE(self,position,rows, DefaultSpeed = '250',
            DefaultDelta = 'c-0.01j'):
    Animate = QPushButton('Animate', self)
    Animate.clicked.connect(self.Animate)
    self.grid.addWidget(Animate,position,0,1,rows)
    
    self.frames = QLineEdit('2',self)
    self.grid.addWidget(self.frames,position,rows,1,self.row-rows)

    self.delta = QLineEdit(DefaultDelta,self)
    self.grid.addWidget(self.delta,position+1,0,1,rows)

    self.speed = QLineEdit(DefaultSpeed,self)
    self.grid.addWidget(self.speed,position+1,rows,1,self.row-rows)
    return None

def EDIT(self, width, height):
    self.win = QWidget()
    self.win.setWindowTitle("other")
    self.win.resize(width, height)
    self.win.move(0,0)
    self.win.setStyleSheet(".QWidget {background-color: #123;}")
    self.win.grid = QGridLayout(self.win)
    self.win.grid.setSpacing(10)

    self.other = QTextEdit(self.win)
    self.other.setText('\n'.join(self.TYPES["other"].split("\n\t")))
    self.win.grid.addWidget(self.other,0,0,1,1)

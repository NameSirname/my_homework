from PyQt5.QtWidgets import QLineEdit, QTextEdit, QLabel, QWidget, QPushButton, QAbstractItemView
from PyQt5.QtWidgets import QSpinBox, QComboBox, QCheckBox, QFileSystemModel, QTreeView

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QDir

def DIR_TREE(self):
    self.model = QFileSystemModel()
    self.model.setRootPath(self.musicDir)
    
    self.tree = QTreeView(self)
    self.tree.setModel(self.model)
    self.tree.setRootIndex(self.model.index(self.musicDir))
    self.tree.clicked.connect(self.getFile)
    
    self.tree.setAnimated(False)
    self.tree.setIndentation(20)
    self.tree.setSortingEnabled(True)
    
    self.tree.setWindowTitle("Dir View")
    self.tree.resize(self.width - self.tbwidth, self.height)
    self.tree.move(0,0)
    self.tree.setColumnWidth(0,(self.width - self.tbwidth)//2)
    for i in range(3):
        self.tree.resizeColumnToContents(i+1)

##    self.tree.setSelectionMode(QAbstractItemView.MultiSelection)

    return None

def SIZE(self,pos, row, MinWidth = 700,MinHeight = 700,
         MaxWidth = 50000,MaxHeight = 50000):
    self.Width = QSpinBox(self)
    self.Width.setRange(MinWidth,MaxWidth)
    self.Width.setValue(self.width)
    self.Width.setSingleStep(10)
    self.grid.addWidget(self.Width, pos, row,1,self.row//2-row)
    self.grid.addWidget(QLabel('width:'), pos,0,1,row)
    
    self.Height = QSpinBox(self)
    self.Height.setRange(MinHeight,MaxHeight)
    self.Height.setValue(self.height)
    self.Height.setSingleStep(10)
    self.grid.addWidget(self.Height, pos, self.row//2+row,1,self.row//2-row)
    self.grid.addWidget(QLabel('height:'), pos, self.row//2,1,row)
    
    Resize = QPushButton('Resize', self)
    Resize.clicked.connect(self.Resize)
    self.grid.addWidget(Resize,pos+1,0,1,self.row)
    
    return 2

def METADATA(self,pos,row):
    x = 1
    self.oldMetadata = QTextEdit()
    self.grid.addWidget(self.oldMetadata,pos,0,x,self.row)
    
    text = QTextEdit()
    self.grid.addWidget(text,pos + x,0,1,self.row)
    
    self.grid.addWidget(QLabel("New Metadata"),pos + x+1,0,1,self.row)
    
    self.track = QLineEdit('',self)
    self.grid.addWidget(self.track,pos + x+2,1,row,self.row-row)
    self.grid.addWidget(QLabel("Track:"),pos + x+2,0,1,row)
    
    self.artist = QLineEdit('',self)
    self.grid.addWidget(self.artist,pos + x+3,row,1,self.row-row)
    self.grid.addWidget(QLabel("Artist:"),pos + x+3,0,1,row)
    
    self.album = QLineEdit('',self)
    self.grid.addWidget(self.album,pos + x+4,row,1,self.row-row)
    self.grid.addWidget(QLabel("Album:"),pos + x+4,0,1,row)
    
    self.title = QLineEdit('',self)
    self.grid.addWidget(self.title,pos + x+5,1,row,self.row-row)
    self.grid.addWidget(QLabel("Title:"),pos + x+5,0,1,row)

    return x + 6

def APPLY(self,pos,row):
    Apply = QPushButton('Set metadata', self)
    Apply.clicked.connect(self.Apply)
    self.grid.addWidget(Apply,pos,0,1,row)

    self.cover  = QCheckBox(self)
    self.cover.setCheckState(2)
    self.grid.addWidget(self.cover,pos,self.row-2,1,1)    
    self.grid.addWidget(QLabel("Hide"),pos,row,1,self.row-row-2)

    self.cover2  = QCheckBox(self)
    self.cover2.setCheckState(0)
    self.grid.addWidget(self.cover2,pos,self.row-1,1,1)    
    
    Delete = QPushButton('Remove file', self)
    Delete.clicked.connect(self.Delete)
    self.grid.addWidget(Delete,pos+1,0,1,row)
    
    Cover = QPushButton('Select Cover', self)
    Cover.clicked.connect(self.Cover)
    self.grid.addWidget(Cover,pos+1,row,1,self.row-row)
    
    Play = QPushButton('Play', self)
    Play.clicked.connect(self.Play)
    self.grid.addWidget(Play,pos+2,0,1,self.row)

    return 3

#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess as sp

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QGridLayout, QFileDialog

from musicE_widgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 925
        self.height = 700
        self.tbwidth = 325
        self.title = 'Edit'

        self.meta = False
        self.fileName = ''
        self.filePath = ''
        self.outPath = ''
        self.covPath = ''
        
##        self.musicDir = QDir.currentPath()
        self.musicDir = u'/home/mister_u/Music'
##        self.musicDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dir = os.path.dirname(os.path.abspath(__file__))
##        self.covDir = os.path.dirname(os.path.dirname(
##                                os.path.dirname(os.path.abspath(__file__))))
        self.covDir = u'/home/mister_u/Music'
        
        self.initGUI()
                
    def initGUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0,0,self.width, self.height)

        self.toolbar = QWidget(self)
        self.toolbar.resize(self.tbwidth,self.height)
        self.toolbar.move(self.width-self.tbwidth,0)
        self.toolbar.setObjectName("toolbar")
        
        QSS = '''
        .QLabel {
            color: white;
            font-weight: bold;
        }
        .QWidget#toolbar {
            background-color: #123;
        }
        '''
        self.toolbar.setStyleSheet(QSS)
        self.row = 6
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.toolbar.setLayout(self.grid)

        self.formats = ["mp3", "wav"]
        self.covFormats = ["png", "jpg"]

        DIR_TREE(self)
        x = 0
        x += SIZE(self,x,2)
        x += METADATA(self,x,1)
        x += APPLY(self,x,self.row//2)
        
        self.show()
        
    def Resize(self):
        self.width = self.Width.value()
        self.height = self.Height.value()
        
        self.resize(self.width,self.height)
##        self.move(0,0)
        self.toolbar.resize(self.tbwidth,self.height)
        self.toolbar.move(self.width-self.tbwidth,0)
        
        self.tree.resize(self.width-self.tbwidth,self.height)
        self.tree.move(0,0)
        self.tree.setColumnWidth(0,(self.width - self.tbwidth)//2)
        for i in range(3):
            self.tree.resizeColumnToContents(i+1)
        return None

    def Apply(self):
        if self.meta:
            self.outPath = (self.filePath[: -len(self.fileName)]
                            + self.title.text().replace(' ', '_'))
            
            command = 'ffmpeg -i '+ '"' + self.filePath + '" ' + '-c copy '
            if self.cover.checkState():
                command += '-map a '
            elif self.cover2.checkState() and self.covPath != '':
                command += ('-i ' + '"' + self.covPath + '" '
                            + '-map 0 -map 1 ' + '-c:a -c:v ')
            if self.changeMeta.checkState():
                command += ('-map_metadata -1 ' +
                            '-metadata title="'+self.track.text()+'" ' +
                            '-metadata artist="'+self.artist.text()+'" ' +
                            '-metadata album="'+self.album.text()+'" ')

            command += '"' + self.outPath + '"'

            sp.run(command, shell=True, check=True)
##            print(sp.run(command, shell=True, check=True, capture_output=True))
        return None

    def Delete(self):
        if len(self.fileName)>0:
            remove(self.filePath)
        return None

    def Cover(self):
        self.covPath = QFileDialog.getOpenFileName(self,
                            directory = self.covDir,
                            caption = 'select_cover')[0]
        if self.covPath.split('.')[-1] not in self.covFormats:
            self.covPath = ''
        return None
    
    def Play(self):
        if self.meta:
            sp.run(['vlc', self.filePath])
            #(shell=True, check=True, capture_output=True)
        return None
   
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def getFile(self,index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        print(indexItem)

        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)

        if len(self.fileName)>3 and self.fileName.split('.')[-1] in self.formats:
            self.title.setText(self.fileName)
            self.meta = True

            if self.showMeta.checkState():
                command = ['ffmpeg', '-i', self.filePath, '-f',
                           'ffmetadata', self.dir + '/metadata.txt', '-y']
                sp.run(command)
                file = open(self.dir + '/metadata.txt', 'r')
                self.oldMetadata.setText(file.read())
                file.close()
##            remove(self.dir + '/metadata.txt')
##            command = ('rm ' + '"' + self.dir + '/metadata.txt' + '" && ' +
##                'ffmpeg -i ' + '"' + self.filePath + '"' +
##                ' -f ffmetadata ' + '"' + self.dir + '/metadata.txt' + '"')
##            sp.run(command, shell=True, check=True)
##            print(sp.run(command, shell=True, check=True, capture_output=True))
            
        else:
            self.title.setText('')
            self.meta = False
            
        return None

def remove(filePath):
    sp.run(['rm', filePath])
    #(shell=True, check=True)
    #print(sp.run(command, shell=True, check=True, capture_output=True)
    return None

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    
    sys.exit(app.exec_())

    

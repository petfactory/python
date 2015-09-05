#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PySide import QtGui, QtCore

class Button(QtGui.QPushButton):
  
    fileDropped = QtCore.Signal(list)

    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)
        
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        #print(event.mimeData())

        if event.mimeData().hasImage():
            image = QtGui.QImage(event.mimeData().imageData())
            print('Dropped an image', image)

        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
                print (12, url.path())

            self.fileDropped.emit(links)

        else:
            event.ignore()

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
    
        qe = QtGui.QLineEdit('', self)
        qe.setDragEnabled(True)
        qe.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)

        button.fileDropped.connect(self.pictureDropped)

        self.setGeometry(50, 50, 300, 150)
        self.setWindowTitle('Simple Drag & Drop')
        self.show()    

    def pictureDropped(self, l):

        print(l)

        for url in l:

            print(type(url))

            if os.path.exists(url):

                print(12)
                picture = Image.open(url)
                picture.thumbnail((72, 72), Image.ANTIALIAS)

                icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                print(icon)
                #item = QListWidgetItem(os.path.basename(url)[:20] + "...", self.pictureListWidget)
                #item.setStatusTip(url)
                #item.setIcon(icon)
                print(os.path.basename(url)[:20])


        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
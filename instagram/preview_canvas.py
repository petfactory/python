import sys, random
from PySide import QtGui, QtCore

class PreviewCanvas(QtGui.QWidget):
    
    def __init__(self):
        super(PreviewCanvas, self).__init__()

        self.setMinimumSize(500,500)
        self.rect_list = None
        self.initUI()
        
    def initUI(self):      

        self.setWindowTitle('Points')
        #self.show()

    def set_rect_list(self, rect_list):
        self.rect_list = rect_list
        self.update()

    def paintEvent(self, e):

        if self.rect_list is not None:
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawPoints(qp)
            qp.end()
        
    def drawPoints(self, qp):
      
        qp.setPen(QtCore.Qt.red)
        size = self.size()
        
        qp.drawRect(0,0,500,500)

        for rect in self.rect_list:
            qp.drawRect(rect)


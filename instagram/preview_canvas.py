import sys, random
from PySide import QtGui, QtCore

class PreviewCanvas(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(PreviewCanvas, self).__init__(parent)

        #self.setGeometry(50, 50, 500, 500)
        self.setMinimumSize(500,500)
        self.rect_list = None
        self.setWindowTitle('Preview')
        self.show()

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
      
        qp.setPen(QtGui.QColor(60, 60, 60))
        size = self.size()
        
        qp.fillRect(0, 0, 500, 500, QtCore.Qt.white)
        color = QtGui.QColor(220, 220, 220)

        for rect in self.rect_list:
            qp.fillRect(rect, color)

def main():
    
    app = QtGui.QApplication(sys.argv)
    a = PreviewCanvas()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


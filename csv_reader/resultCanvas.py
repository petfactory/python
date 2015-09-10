# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
import sys

class MyResultCanvas(QtGui.QWidget):

    def __init__(self, pos, info_list, parent=None):
        super(MyResultCanvas, self).__init__(parent)

        self.col_list = [QtCore.Qt.red, QtCore.Qt.white, QtGui.QColor(70, 90, 120)] 

        self.info_list = info_list
        self.chart_base_y = 300
        self.chart_width = 120
        self.num_month = len(info_list)
        self.chart_offset_edge_x = 10
        self.chart_spacing = 10
        self.width = self.chart_width * self.num_month + self.chart_spacing * (self.num_month-1) + self.chart_offset_edge_x*2
        self.height = 400
        self.height_scale = .3

        print(self.width, self.height)

        self.setGeometry(pos[0], pos[1], self.width, self.height )
        self.setWindowTitle('Result Canvas')
        self.show()

    def mousePressEvent(self, event):
        #print(dir(event))
        x, y = event.pos().toTuple()
        print(x, y)


    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
        
        for i, info in enumerate(self.info_list):

            y = self.chart_base_y

            for j, val in enumerate(info):
                
                x = self.chart_offset_edge_x + (self.chart_width + self.chart_spacing) * i
                v = val * -self.height_scale
                qp.fillRect(x, y, self.chart_width, v, self.col_list[j])
                y += v

def main():
    
    app = QtGui.QApplication(sys.argv)
    pos = 20,100
    info_list = [[100, 100, 100], [100, 200, 100], [100, 200, 300], [50,50,400], [100, 100, 100], [100, 200, 100]]
    w = MyResultCanvas(pos, info_list)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
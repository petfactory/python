import os
import sys
from PySide import QtGui, QtCore

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        
        self.num_col = 4
        self.v_box = QtGui.QVBoxLayout(self)

        self.scrollarea = QtGui.QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.v_box.addWidget(self.scrollarea)

        self.btn_widget = QtGui.QWidget()
        grid_layout = QtGui.QGridLayout(self.btn_widget)
        self.scrollarea.setWidget(self.btn_widget)

        self.img_fold = r"pics"

        for index, img in enumerate(os.listdir(self.img_fold)):

            img_path = os.path.join(self.img_fold, img)

            pixmap = QtGui.QPixmap(img_path)

            lbl = QtGui.QPushButton(pixmap, "")
            
            lbl.setCheckable(True)
            size = pixmap.size()
            w, h = size.toTuple()
            lbl.setIconSize(size)
            lbl.setFixedSize(w+30, h+30)
            
            row = index % self.num_col
            col = index / self.num_col
            print(row, col)
            grid_layout.addWidget(lbl, col, row)
            

        self.setGeometry(50, 50, 400, 400)
        self.setWindowTitle('Image viewer')
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
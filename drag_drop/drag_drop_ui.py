from PySide import QtGui, QtCore
import sys

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        outer_vbox = QtGui.QVBoxLayout(self)
        #outer_vbox.setContentsMargins(0,0,0,0)


        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle('Drag drop')

        self.image_widget = QtGui.QPushButton()
        self.image_widget.setFixedSize(300,300)
        outer_vbox.addWidget(self.image_widget)

        pixmap = QtGui.QPixmap()
        pixmap.fill(fillColor=QtCore.Qt.red)
        #self.image_widget.setPixmap(pixmap)
        self.image_widget.update()
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
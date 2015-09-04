# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class InstagramDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(InstagramDialog, self).__init__(parent)

        self.setGeometry(50, 50, 250, 100)
        self.setWindowTitle('Print PDF')

        label = QtGui.QLabel()
        label.setText(u"<span style='font-family:Avenir Next; font-style:Ultra Light; font-size:50pt; color:#999999;'>23 Maj </span><span style='font-family:Avenir Next; font-size:50pt; font-style:Regular; color:#333333;'>Hejsan lilla fåret</span>")
        main_vbox = QtGui.QVBoxLayout(self)

        pixmap = QtGui.QPixmap.grabWidget(label)

        f = QtCore.QFile("yourFile.png")
        f.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(f, "PNG", 4)

        main_vbox.addWidget(label)
        self.show()

def main():
    
    app = QtGui.QApplication(sys.argv)
    a = InstagramDialog()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

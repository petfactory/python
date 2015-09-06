#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PySide import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        #font_db = QtGui.QFontDatabase()
        #font_db.addApplicationFont('/System/Library/Fonts/Apple Color Emoji.ttf')

        te = QtGui.QTextEdit(self)
        font = QtGui.QFont("Menlo", 18)
        te.setFont(font)

        t = u'Cherries åäö \ud83c\udf52\ud83d\ude0d'
        #t.enccode('utf-8')
        te.setText(t)
        #print(dir(te))

        self.setGeometry(50, 50, 300, 150)
        self.setWindowTitle('Unicode')
        self.show()

        #a = te.toPlainText()
        #print(a.encode('utf-8'))

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
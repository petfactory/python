from PySide import QtGui, QtCore

import sys


def do_print():
    #set up printer
    printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
    printer.setOutputFileName('test.pdf')
    printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
    printer.setPaperSize(QtCore.QSizeF(2000,2000), QtGui.QPrinter.Unit.DevicePixel)

    #set up image
    image = QtGui.QImage()
    image.load('highres/11379787_969363229761322_1240199567_n.jpg')
    w, h = image.size().toTuple()
    #print(w, h)
    #paint & print
    painter = QtGui.QPainter()
    painter.begin(printer)
    
    #left, top, width, height
    dest_rect = QtCore.QRect(0,0,1000,1000 )
    painter.drawImage(dest_rect, image)
    painter.end()

def main():

    app = QtGui.QApplication(sys.argv)
    do_print()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()




# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
import os, sys, json
#from datetime import date
import datetime

def set_font(name, style, size):

    font = QtGui.QFont(name)
    fontStyle = style
    fontDatabase = QtGui.QFontDatabase()
    oldStrategy = font.styleStrategy()
    font = fontDatabase.font(font.family(),fontStyle, font.pointSize())
    font.setStyleStrategy(oldStrategy)
    fontinfo = QtGui.QFontInfo(font)
    font.setPixelSize(size)

    #print(fontinfo.family(), fontinfo.styleName())
    return font

def do_print():

    #dpi = 72
    dpi = 300
    dpmm = dpi / 25.4
    #dpmm = 2.8
    print(dpmm)
    #28.3464566929
    #28

    page_width_mm = 200
    page_height_mm = 200

    page_width_pixel = page_width_mm * dpmm
    page_height_pixel = page_height_mm * dpmm

    img_width_pixel = page_width_pixel * .8
    img_height_pixel = page_height_pixel * .8

    edge_offet = (page_width_pixel - img_width_pixel) * .5


    # get the fonts
    font_light = set_font(name='Avenir Next', style='Ultra Light', size=14)
    font_regular = set_font(name='Avenir Next', style='Regular', size=14)

    printer = QtGui.QPrinter()
    printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
    printer.setOutputFileName('text.pdf')
    printer.setResolution(dpi)
    #printer.setOutputToFile(True)
    #printer.setPaperSize(QtCore.QSizeF(500,500), QtGui.QPrinter.Unit.DevicePixel)
    printer.setPaperSize(QtCore.QSizeF(page_width_pixel,page_height_pixel), QtGui.QPrinter.Unit.DevicePixel)
    printer.setPageMargins(0,0,0,0,QtGui.QPrinter.Unit.DevicePixel)
    #printer.setPageMargins(0,0,0,0,QtGui.QPrinter.Unit.DevicePixel)
 
    painter = QtGui.QPainter()
    painter.begin(printer)

    painter.setFont(font_light)
        
    painter.drawText(QtCore.QRect(10, 450, 400, 60), QtCore.Qt.AlignLeft, u'24 Maj');

    painter.setFont(font_regular)  
    #painter.drawText(100,480,u'Hejsan fåret!')

    painter.drawText(QtCore.QRect(10, 450, 400, 60), QtCore.Qt.TextWordWrap, u"              Hejsan lilla fåret. Nu ska vi testa var detta stycke exempelvis byter rad. Det ska bli spännande!")

    # draw image
    image = QtGui.QImage()
    image.load('../highres/11379787_969363229761322_1240199567_n.jpg')
    dest_rect = QtCore.QRect(edge_offet,edge_offet,img_width_pixel,img_height_pixel )
    painter.drawImage(dest_rect, image)

    painter.end()
    print('Created a pdf')

def main():

    app = QtGui.QApplication(sys.argv)
    do_print()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

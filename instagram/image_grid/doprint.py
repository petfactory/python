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

def do_print(json_path, dest_dir=None):

    json_data = None
    with open(json_path, 'r') as f:
        data = f.read()
        json_data = json.loads(data)

    if json_data:
        media_list = json_data.get('media')

    else:
        print('Could not load json data')
        return

    # get the fonts
    font_light = set_font(name='Avenir Next', style='Ultra Light', size=14)
    font_regular = set_font(name='Avenir Next', style='Regular', size=14)

    printer = QtGui.QPrinter()
    printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
    #dest = os.path.join(dest_dir, 'instagram_python.pdf')
    #print(dest)
    printer.setOutputFileName('instagram_python.pdf')
    #printer.setOutputToFile(True)
    printer.setPaperSize(QtCore.QSizeF(500,500), QtGui.QPrinter.Unit.DevicePixel)
    printer.setPageMargins(0,0,0,0,QtGui.QPrinter.Unit.DevicePixel)
 
    painter = QtGui.QPainter()
    painter.begin(printer)


    for index, media in enumerate(media_list):
        if index > 0: printer.newPage()
        painter.drawRect(2,2,496,496)

        painter.setFont(font_light)
        
        date_string = media.get('date') 
        d = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        month_names = ['Jan','Feb','Mar','Aprl','Maj','Jun','Jul','Aug','Sep','Okt','Nov','Dec']
        painter.drawText(50,480,'{} {}'.format(d.day, month_names[d.month]));

        painter.setFont(font_regular)  
        painter.drawText(100,480,media.get('text'));

        # draw image
        image = QtGui.QImage()
        image.load(os.path.join('highres/', media.get('filename')))
        #w, h = image.size().toTuple()
        dest_rect = QtCore.QRect(10,10,400,400 )
        painter.drawImage(dest_rect, image)

    painter.end()
    print('Created a pdf')

def main():

    app = QtGui.QApplication(sys.argv)

    json_path = 'highres/instagram.json'
    #dest_dir = 'Users/johan/Desktop'
    do_print(json_path)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

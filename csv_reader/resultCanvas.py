# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
import sys

class MyResultCanvas(QtGui.QWidget):

    def __init__(self, pos, result_list=[], search_labels=[], parent=None):
        super(MyResultCanvas, self).__init__(parent)

        MyResultCanvas.col_list = [ QtGui.QColor(118, 165, 208),
                                    QtGui.QColor(172, 185, 60),
                                    QtGui.QColor(231, 109, 67),
                                    QtGui.QColor(246, 197, 26),
                                    QtGui.QColor(127, 210, 135)]

        MyResultCanvas.month_names = ('jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sept', 'okt', 'now', 'dec')


        self.result_list = result_list
        self.search_labels = search_labels
        self.text_spacing = 20
        self.text_offset = 20
        self.chart_line_color = QtGui.QColor(200, 200, 200)
        self.month_name_y = 20

        self.chart_base_y = 300
        self.chart_width = 90
        self.num_month = len(result_list)
        self.chart_offset_edge_x = 10
        self.chart_spacing = 10
        self.width = self.chart_width * self.num_month + self.chart_spacing * (self.num_month-1) + self.chart_offset_edge_x*2
        self.height = 400
        self.height_scale = .1

        print(self.width, self.height)

        self.setGeometry(pos[0], pos[1], self.width, self.height )
        self.setWindowTitle('Result Canvas')
        self.show()

    def mousePressEvent(self, event):
        #print(dir(event))
        x, y = event.pos().toTuple()
        print(x, y)


    def paintEvent(self, e):

        if len(self.result_list) > 0:
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawPoints(qp)
            qp.end()
        
    def drawPoints(self, qp):
        
        #key_list = self.result_list[0].keys()

        for index, result in enumerate(self.result_list):

            y = self.chart_base_y

            text_y = y + self.text_offset
            month_total = 0
            month_total_x = 0

            color_index = 0
            for key in self.search_labels:

                data_list = result.get(key)

                month_total_x = x = self.chart_offset_edge_x + (self.chart_width + self.chart_spacing) * index

                qp.setPen(self.chart_line_color)
                qp.drawLine(self.chart_spacing*.5, self.chart_base_y, self.width-self.chart_spacing*.5, self.chart_base_y)
                qp.drawLine(x-self.chart_spacing*.5, self.chart_spacing*.5, x-self.chart_spacing*.5, self.height-self.chart_spacing*.5)

                qp.setFont(QtGui.QFont('Decorative', 16))
                qp.drawText(month_total_x, self.month_name_y, MyResultCanvas.month_names[index])

                

                color = MyResultCanvas.col_list[color_index]
                color_index += 1

                if not data_list:
                    print('Could not get the data: {}'.format(key.encode('utf-8')))

                    continue

                total = 0
                for data in data_list:
                    total += data[3]

                #print('{} Total:{}'.format(key, total))
                qp.setPen(color)

                
                v = total * self.height_scale
                qp.fillRect(x, y, self.chart_width, v, color)
                y += v

                text_y += self.text_spacing

                qp.setFont(QtGui.QFont('Decorative', 16))
                qp.drawText(x, text_y, str(total))

                
                
                month_total += total
                #print(total)

            qp.setPen(QtGui.QColor(0, 0, 0))
            qp.drawText(month_total_x, self.chart_base_y + self.text_offset, str(month_total))

            
        last_x = month_total_x+self.chart_width + self.chart_spacing*.5
        qp.setPen(self.chart_line_color)
        qp.drawLine(last_x, self.chart_spacing*.5,+ last_x, self.height-self.chart_spacing*.5)


def main():
    
    app = QtGui.QApplication(sys.argv)
    pos = 20,100
    data = [{'test':[['','','',-100]]},
            {'test':[['','','',-200]]},
            {'test':[['','','',-300]]},
            {'test':[['','','',-400]]},
            {'test':[['','','',-500]]},
            {'test':[['','','',-600]]},
            {'test':[['','','',-600]]},
            {'test':[['','','',-500]]},
            {'test':[['','','',-400]]},
            {'test':[['','','',-300]]},
            {'test':[['','','',-200]]},
            {'test':[['','','',-100]]}]


    labels = ['test']
    w = MyResultCanvas(pos, data, labels)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
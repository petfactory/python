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

        self.v_box = QtGui.QVBoxLayout(self)

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
        self.height_scale = 0.1

        #self.canvas_widget = QtGui.QWidget()
        #self.canvas_widget.setFixedSize(self.width, self.height)
        #self.v_box.addWidget(self.canvas_widget)


        self.v_box.addStretch()

        self.scale_spinbox = QtGui.QDoubleSpinBox()
        self.scale_spinbox.setMaximumWidth(100)
        self.v_box.addWidget(self.scale_spinbox)
        self.scale_spinbox.setValue(self.height_scale)
        self.scale_spinbox.setSingleStep(.005)
        self.scale_spinbox.valueChanged.connect(self.scale_changed)


        #print(self.width, self.height)

        self.setGeometry(pos[0], pos[1], self.width, self.height )
        self.setWindowTitle('Result Canvas')
        self.show()

    def redraw(self, result_list=[], search_labels=[]):

        self.result_list = result_list
        self.search_labels = search_labels
        print(self.search_labels)
        self.update()

    def scale_changed(self, value):
        self.height_scale = value
        self.update()

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
        
    def add_amount_widget(self, x, y):

        print(x, y)
        w = QtGui.QPushButton('text')
        #self.v_box.addWidget(w)

    def drawPoints(self, qp):

        for index, result in enumerate(self.result_list):

            y = self.chart_base_y

            text_y = y + self.text_offset
            month_total = 0
            month_total_x = 0

            #color_index = 0

            for i, key in enumerate(self.search_labels):

                #print(index, key)
                data_list = result.get(key)

                month_total_x = x = self.chart_offset_edge_x + (self.chart_width + self.chart_spacing) * index

                qp.setPen(self.chart_line_color)
                qp.drawLine(self.chart_spacing*.5, self.chart_base_y, self.width-self.chart_spacing*.5, self.chart_base_y)
                qp.drawLine(x-self.chart_spacing*.5, self.chart_spacing*.5, x-self.chart_spacing*.5, self.height-self.chart_spacing*.5)

                qp.setFont(QtGui.QFont('Decorative', 16))
                qp.drawText(month_total_x, self.month_name_y, MyResultCanvas.month_names[index])

                

                #color = MyResultCanvas.col_list[color_index]
                #color_index += 1
                color = MyResultCanvas.col_list[i % len(MyResultCanvas.col_list)]

                if not data_list:
                    #print('Could not get the data: {}'.format(key.encode('utf-8')))
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

                # draw the amount per search label
                qp.setFont(QtGui.QFont('Decorative', 16))
                qp.drawText(x, text_y, str(total))
                #self.add_amount_widget(x, text_y)

                
                
                month_total += total
                #print(total)

            qp.setPen(QtGui.QColor(0, 0, 0))
            qp.drawText(month_total_x, self.chart_base_y + self.text_offset, str(month_total))

            
        last_x = month_total_x+self.chart_width + self.chart_spacing*.5
        qp.setPen(self.chart_line_color)
        qp.drawLine(last_x, self.chart_spacing*.5,+ last_x, self.height-self.chart_spacing*.5)


def main():
    
    app = QtGui.QApplication(sys.argv)
    pos = 0,0
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
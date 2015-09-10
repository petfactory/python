# -*- coding: utf-8 -*-
import os, sys, pprint
from datetime import datetime
from PySide import QtGui, QtCore
import locale, csv
import resultCanvas, tableviewModel

class MyTableView(QtGui.QWidget):

    def __init__(self):
        super(MyTableView, self).__init__()

        self.setGeometry(0, 50, 700, 500)
        self.setWindowTitle('Tableview')
        main_vbox = QtGui.QVBoxLayout(self)

        self.result_canvas = None
        self.tableview = QtGui.QTableView()
        self.tableview.setAlternatingRowColors(True)
        main_vbox.addWidget(self.tableview)

        #self.model.append_item(Item('2015-03-22', 'Ica', '', '-1,256.60', '1,231.21'))

        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

        self.search_lineedit = QtGui.QLineEdit()
        main_vbox.addWidget(self.search_lineedit)

        search_button = QtGui.QPushButton('Search')
        search_button.clicked.connect(self.search_button_clicked)
        main_vbox.addWidget(search_button)

        self.show()

    def load_data(self, path):

        #path = r'/Users/johan/Desktop/export.csv'
        header_list, row_list = self.get_csv_file(path)

        self.model = tableviewModel.MyModel([], header_list)
        self.tableview.setModel(self.model)

        for row_data in row_list:

            if len(row_data) != 5:
                print('The row does not have length of 5')
                continue

            datestring, transaction, category, amount, balance = row_data
            self.model.append_item(tableviewModel.Item(datestring, transaction, category, amount, balance))


    def search_button_clicked(self):

        text = self.search_lineedit.text()
        self.search(search_list=text.split(','))

    def search(self, search_list=None, year=None, month=None, day=None):

        ret_dict = {}

        for label in search_list:
            ret_dict[label.strip()] = []

        rows = self.model.rowCount()

        match_rows = []
        for row in range(rows):

            date = self.model.getDate(row)

            if search_list:

                trans = self.model.getTransaction(row)

                for label in search_list:

                    l = label.strip()
                    if l.lower() in trans.lower():
                        ret_dict[l].append([row, date.toString(QtCore.Qt.ISODate), trans, self.model.getAmount(row)])

        pprint.pprint(ret_dict)

        # show the result canvas
        x, y = self.pos().toTuple()

        info_list = [[100, 100, 100], [100, 200, 100], [100, 200, 300], [50,50,400], [100, 100, 100], [100, 200, 100]]

        self.result_canvas = resultCanvas.MyResultCanvas((x+50, y+50), info_list)
        self.result_canvas.show()

    def get_csv_file(self, path):

        if not os.path.isfile(path):
            print('Not a valid file')
            return

        row_list = []
        header_list = []
        with open(path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)

            for index, row in enumerate(spamreader):
                
                if index == 0:
                    header_list.extend(row)
                else:
                    row_list.append(row)

        return (header_list, row_list)


def main():
    
    app = QtGui.QApplication(sys.argv)
    a = MyTableView()
    a.load_data('example.csv')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


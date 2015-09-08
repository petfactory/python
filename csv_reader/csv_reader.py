# -*- coding: utf-8 -*-

import os, sys
import csv

from PySide import QtGui, QtCore

def build(path):

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

class CSVReader(QtGui.QWidget):

    def __init__(self):
        super(CSVReader, self).__init__()

        outer_vbox = QtGui.QVBoxLayout(self)
        outer_vbox.setContentsMargins(0,0,0,0)

        menubar = QtGui.QMenuBar()
        outer_vbox.addWidget(menubar)
        menubar.setNativeMenuBar(False)

        file_menu = menubar.addMenu('File')

        load_action = QtGui.QAction('Load', self)
        load_action.triggered.connect(self.load_btn_clicked)
        file_menu.addAction(load_action)


        main_hbox = QtGui.QHBoxLayout()
        outer_vbox.addLayout(main_hbox)
        main_hbox.setContentsMargins(7,7,7,7)
        
        # the main image viewer
        main_vbox = QtGui.QVBoxLayout()
        main_hbox.addLayout(main_vbox)

        self.table_view = QtGui.QTableView()
        main_vbox.addWidget(self.table_view)

        path = r'/Users/johan/Desktop/export.csv'
        header_list, row_list = build(path)



        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(header_list)
        self.table_view.setModel(self.model)

        self.add_items(row_list)

        self.setGeometry(0, 50, 400, 400)
        self.setWindowTitle('CSV Reader')
        self.show()


    def add_items(self, row_list):

        for row, row_data in enumerate(row_list):

            for col, col_data in enumerate(row_data):
                item = QtGui.QStandardItem(col_data.decode('utf8'))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.model.setItem(row, col, item)
        
    def load_btn_clicked(self):
        print(self.sender())

def main():

    app = QtGui.QApplication(sys.argv)
    csv_reader = CSVReader()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


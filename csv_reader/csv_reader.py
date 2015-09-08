# -*- coding: utf-8 -*-

import os, sys, pprint
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

class MyDelegate(QtGui.QItemDelegate):
    
    def __init__(self, parent=None):
        super(MyDelegate, self).__init__(parent)
        
    def createEditor(self, parent, option, index):
        
        col = index.column()
        
        if col == 0:

            #spinbox = QtGui.QDoubleSpinBox(parent)
            spinbox = QtGui.QDateEdit(parent)
            #spinbox.setRange(-99999, 99999)
            spinbox.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            return spinbox
        
        else:
            return QtGui.QLineEdit(parent)

class CSVReader(QtGui.QWidget):

    def __init__(self):
        super(CSVReader, self).__init__()

        outer_vbox = QtGui.QVBoxLayout(self)
        outer_vbox.setContentsMargins(0,0,0,0)
        self.row_list = None

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
        self.table_view.setItemDelegate(MyDelegate(self.table_view))

        path = r'/Users/johan/Desktop/export.csv'
        header_list, row_list = build(path)

        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(header_list)
        self.table_view.setModel(self.model)

        self.add_items(row_list)

        self.setGeometry(0, 50, 400, 400)
        self.setWindowTitle('CSV Reader')

        self.search_lineedit = QtGui.QLineEdit()
        main_vbox.addWidget(self.search_lineedit)

        search_button = QtGui.QPushButton('Search')
        search_button.clicked.connect(self.search_button_clicked)
        main_vbox.addWidget(search_button)

        

        self.show()

    def search_button_clicked(self):

        text = self.search_lineedit.text()
        self.search(string=text)

    def search(self, string=None, year=None, month=None, day=None):

        rows = self.model.rowCount()

        match_rows = []
        for row in range(rows):
            item = self.model.item(row, 0)
            date = item.text()
            date_split = date.split('-')

            if string:

                transaction = self.model.item(row, 1).text()

                if string in transaction.lower():
                    date = self.model.item(row, 0).text()
                    belopp = self.model.item(row, 3).text()
                    saldo = self.model.item(row, 4).text()
                    match_rows.append([date, transaction, '', belopp, saldo])
                    #print(trans.encode('utf-8'))
                    

        pprint.pprint(match_rows)


    def add_items(self, row_list):

        self.row_list = row_list

        for row, row_data in enumerate(row_list):

            for col, col_data in enumerate(row_data):

                if col > 2:

                    item = QtGui.QStandardItem(col_data.decode('utf8'))

                else:
                    item = QtGui.QStandardItem(col_data.decode('utf8'))

                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                self.model.setItem(row, col, item)

        
    def load_btn_clicked(self):
        print(self.sender())

def main():

    app = QtGui.QApplication(sys.argv)
    csv_reader = CSVReader()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


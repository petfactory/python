# -*- coding: utf-8 -*-
import os, sys, pprint
from datetime import datetime
from PySide import QtGui, QtCore
import locale, csv


class Item(object):

    def __init__(self, datestring, transaction, category, amount, balance):

        #locale.setlocale(locale.LC_ALL, "es_ES")
        #locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        self.date = QtCore.QDate.fromString(datestring, QtCore.Qt.ISODate)
        self.transaction = transaction.decode('utf-8')
        self.category = category.decode('utf-8')

        # check for empty string
        #self.amount = locale.atof(amount) if amount else  0
        #self.balance = locale.atof(balance) if balance else  0

        # need to get back to using locale...
        if amount:
            amount = amount.replace(".", "")
            amount = amount.replace(",", ".")
            self.amount = float(amount)

        else: self.amount = 0

        if balance:
            balance = balance.replace(".", "")
            balance = balance.replace(",", ".")
            self.balance = float(balance)

        else: self.balance = 0


        #QtCore.QDate(datetime.strptime('2015-12-24', "%Y-%m-%d"))
        #QtCore.QDate.fromString('2015-12-24', QtCore.Qt.ISODate).toString(QtCore.Qt.ISODate)
        #QtCore.QDate.fromString(self._items[row][col], QtCore.Qt.ISODate).toString(QtCore.Qt.ISODate)
        #QtCore.QDate.fromString(self._items[row][col], QtCore.Qt.ISODate)

class MyModel(QtCore.QAbstractTableModel):

    def __init__(self, items, headers):
        '''Instantiates the model with a root item.'''
        super(MyModel, self).__init__()
        self._items = items
        self.headers = headers

    # Mandatory method implementations ---------------------------

    # the following 3 methods (rowCount(...), columnCount(...), data(...)) must be implemented
    # default implementation of index(...), parent(...) are provided by the QAbstractTableModel class
    # Well behaved models will also implement headerData(...)
    def rowCount(self, index=QtCore.QModelIndex()):
        '''Returns the number of children for the given QModelIndex.'''
        return len(self._items)

    def columnCount( self, index=QtCore.QModelIndex()):
        '''Retur the number of columns'''
        return 5

    def getAmount(self, row):
            return self._items[row].amount

    def getTransaction(self, row):
            return self._items[row].transaction

    def getDate(self, row):
            return self._items[row].date

    def data( self, index, role= QtCore.Qt.DisplayRole):
        '''Return the display name of the PyNode from the item at the given index.'''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            row = index.row()
            col = index.column()

            if col == 0:
                #print(self._items[row].date.year())
                return self._items[row].date

            elif col == 1:
                return self._items[row].transaction

            elif col == 2:
                return self._items[row].category

            elif col == 3:
                return self._items[row].amount

            elif col == 4:
                return self._items[row].balance


    # optional method implementations ---------------------------
    def flags( self, index ):
        '''Valid items are selectable, editable, and drag and drop enabled. Invalid indices (open space in the view)
        are also drop enabled, so you can drop items onto the top level.
        '''
        col = index.column()

        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            #return QtCore.Qt.ItemIsEnabled |  QtCore.Qt.ItemIsSelectable
            '''
            if col == 0:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            else:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            '''
    
    def setData(self, index, value, role=QtCore.Qt.EditRole):
    
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            col = index.column()

            if col == 0:
                self._items[row].date = value
            elif col == 1:
                self._items[row].transaction = value
            elif col == 2:
                self._items[row].category = value
            elif col == 3:
                self._items[row].amount = value
            elif col == 4:
                self._items[row].balance = value

            self.dataChanged.emit(index, index)

            return True

        return False
    
    def append_item(self, item, parent=QtCore.QModelIndex()):
        ''' this will append an item'''

        position = self.rowCount()
        self.beginInsertRows(QtCore.QModelIndex(), position, position)
        self._items.insert(position, item)
        self.endInsertRows()
        return True

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[col]
        return None



class MyTableView(QtGui.QWidget):

    def __init__(self):
        super(MyTableView, self).__init__()

        self.setGeometry(0, 50, 700, 500)
        self.setWindowTitle('Tableview')
        main_vbox = QtGui.QVBoxLayout(self)

        self.tableview = QtGui.QTableView()
        self.tableview.setAlternatingRowColors(True)
        main_vbox.addWidget(self.tableview)

        path = r'/Users/johan/Desktop/export.csv'
        header_list, row_list = self.get_csv_file(path)

        self.model = MyModel([], header_list)
        self.tableview.setModel(self.model)

        for row_data in row_list:

            if len(row_data) != 5:
                print('The row does not have length of 5')
                continue
            datestring, transaction, category, amount, balance = row_data
            self.model.append_item(Item(datestring, transaction, category, amount, balance))

        #self.model.append_item(Item('2015-03-22', 'Ica', '', '-1,256.60', '1,231.21'))

        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

        self.search_lineedit = QtGui.QLineEdit()
        main_vbox.addWidget(self.search_lineedit)

        search_button = QtGui.QPushButton('Search')
        search_button.clicked.connect(self.search_button_clicked)
        main_vbox.addWidget(search_button)

        self.show()

    def search_button_clicked(self):

        text = self.search_lineedit.text()
        self.search(search_list=text.split(','))

    def search(self, search_list=None, year=None, month=None, day=None):

        ret_dict = {}

        for label in search_list:
            ret_dict[label] = []

        rows = self.model.rowCount()

        match_rows = []
        for row in range(rows):

            date = self.model.getDate(row)

            if search_list:

                trans = self.model.getTransaction(row)

                #if any(x.lower() in trans.lower() for x in search_list):
                for label in search_list:

                    if label.lower() in trans.lower():
                        ret_dict[label].append([date.toString(QtCore.Qt.ISODate), trans, self.model.getAmount(row)])

                        #print(trans.encode('utf-8'))
                    #match_rows.append([date.toString(QtCore.Qt.ISODate), trans])
                    #print(trans.encode('utf-8'))
                    

        #pprint.pprint(match_rows)
        pprint.pprint(ret_dict)


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
    
    #locale.setlocale(locale.LC_NUMERIC, 'sv_SE')

    #print(locale.THOUSEP)

    #print(locale.atof('1.000.1000,55'))

    #return
    #a =  '-1.000.000,23'.replace(".", "")
    #print a.replace(",", ".")

    app = QtGui.QApplication(sys.argv)
    a = MyTableView()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


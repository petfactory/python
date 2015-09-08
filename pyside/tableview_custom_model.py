# -*- coding: utf-8 -*-
import os, sys, pprint
from datetime import datetime
from PySide import QtGui, QtCore
import locale

class Item(object):

    def __init__(self, datestring, transaction, category, amount, balance):

        locale.setlocale(locale.LC_ALL, "en_US")

        self.date = QtCore.QDate.fromString(datestring, QtCore.Qt.ISODate)
        self.transaction = transaction
        self.category = category
        self.amount = locale.atof(amount)
        self.balance = locale.atof(balance)

        #QtCore.QDate(datetime.strptime('2015-12-24', "%Y-%m-%d"))
        #QtCore.QDate.fromString('2015-12-24', QtCore.Qt.ISODate).toString(QtCore.Qt.ISODate)
        #QtCore.QDate.fromString(self._items[row][col], QtCore.Qt.ISODate).toString(QtCore.Qt.ISODate)
        #QtCore.QDate.fromString(self._items[row][col], QtCore.Qt.ISODate)

class MyModel(QtCore.QAbstractTableModel):

    def __init__(self, items):
        '''Instantiates the model with a root item.'''
        super(MyModel, self).__init__()
        self._items = items

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

    def data( self, index, role= QtCore.Qt.DisplayRole):
        '''Return the display name of the PyNode from the item at the given index.'''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            row = index.row()
            col = index.column()

            if col == 0:
                print(self._items[row].date.year())
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

class MyTableView(QtGui.QWidget):

    def __init__(self):
        super(MyTableView, self).__init__()

        self.setGeometry(0, 50, 500, 300)
        self.setWindowTitle('Tableview')
        main_vbox = QtGui.QHBoxLayout(self)

        self.tableview = QtGui.QTableView()
        self.tableview.setAlternatingRowColors(True)
        main_vbox.addWidget(self.tableview)

        self.model = MyModel([])
        self.tableview.setModel(self.model)

        item1 = Item('2015-03-22', 'Ica', '', '-1,256.60', '1,231.21')
        item2 = Item('1978-03-22', 'Willys', '', '1,256.00', '-42.21')
        item3 = Item('1978-03-22', 'Guldhedens vattentorn', '', '1,256.00', '-42.00')

        self.model.append_item(item1)
        self.model.append_item(item2)
        self.model.append_item(item3)
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    a = MyTableView()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


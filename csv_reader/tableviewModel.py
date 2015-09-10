# -*- coding: utf-8 -*-
#import sys
from PySide import QtGui, QtCore

class Item(object):

    def __init__(self, datestring, transaction, category, amount, balance):

        self.date = QtCore.QDate.fromString(datestring, QtCore.Qt.ISODate)
        self.transaction = transaction.decode('utf-8')
        self.category = category.decode('utf-8')

        # a bit weird to use the german locale,
        # but swedish will not pars the string
        german = QtCore.QLocale(QtCore.QLocale.German)

        self.amount, amount_ok = german.toDouble(amount)
        if not amount_ok:
            print('Could not parse amount string')
            self.amount = None

        self.balance, balance_ok = german.toDouble(balance)
        if not balance_ok:
            print('Could not parse balance string')
            self.balance = None

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

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[section]

        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return section

        else:
            return None
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
        #self.tableview.setAlternatingRowColors(True)
        main_vbox.addWidget(self.tableview)

        #self.model.append_item(Item('2015-03-22', 'Ica', '', '-1,256.60', '1,231.21'))

        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

        self.search_lineedit = QtGui.QLineEdit()
        self.search_lineedit.installEventFilter(self)
        main_vbox.addWidget(self.search_lineedit)

        search_button = QtGui.QPushButton('Search')
        search_button.clicked.connect(self.search_button_clicked)
        main_vbox.addWidget(search_button)



        self.show()

    def eventFilter(self, widget, event):

        if (event.type() == QtCore.QEvent.KeyPress and widget is self.search_lineedit):

            key = event.key()

            if key == QtCore.Qt.Key_Return:
                #print('return')
                self.search_button_clicked()
                return True
            else:
                return False

        #return QtGui.QWidget.eventFilter(self, widget, event)
        return False


    def load_data(self, path):

        load_data = self.get_csv_file(path)

        if not load_data:
            return

        header_list, row_list = load_data


        item_list = []
        for row_data in row_list:

            if len(row_data) != 5:
                print('The row does not have length of 5')
                continue

            datestring, transaction, category, amount, balance = row_data
            item_list.append(tableviewModel.Item(datestring, transaction, category, amount, balance))

        self.model = tableviewModel.MyModel(item_list, header_list)
        self.tableview.setModel(self.model)


    def search_button_clicked(self):

        text = self.search_lineedit.text()
        self.search(search_list=text.split(','))

    def search(self, search_list=None, year=None, month=None, day=None):

        # the dict containing all matches
        match_dict = {}

        # Initaiate the dict, strip away the white space for the keys and add empty list as value
        search_label_stripped = []
        for label in search_list:
            l = label.strip()
            search_label_stripped.append(l)
            match_dict[l] = []


        rows = self.model.rowCount()

        # loop through the rows
        match_rows = []
        for row in range(rows):

            date = self.model.getDate(row)

            if search_list:

                # get the transaction string
                trans = self.model.getTransaction(row)

                # loop through all the individual strings in the search list
                for label in search_list:

                    # remove the white space and convert to lower and see if the label string is present
                    # the transaction string, if it is append to the ret dict under corresponding key
                    l = label.strip()
                    if l.lower() in trans.lower():
                        #ret_dict[l].append([row, date.toString(QtCore.Qt.ISODate), trans, self.model.getAmount(row)])
                        match_dict[l].append([row, date, trans, self.model.getAmount(row)])

        #pprint.pprint(ret_dict)
        num_months = 12

        # build the result list that has the length of the num_monts, and that contains a dict with the search strings, which in
        # trun has a list of the transactions that occured during respective month
        # [ {'coop':[]
        #    'ica':[]},
        #   {'coop':[]
        #    'ica':[]}...]

        result_list = []
        for i in range(num_months):
            d = {}

            for key in match_dict.keys():
                d[key] = []

            result_list.append(d)

        
        # llop through the match_dict and place the data in the result list by month, and in 
        # each month list in the correct dictionary based on the label
        for label, data_list in match_dict.iteritems():

            for data in data_list:

                month_index = data[1].month()-1
                result_list[month_index][label].append(data)


        #pprint.pprint(result_list)
        # show the result canvas
        x, y = self.pos().toTuple()

        #info_list = [[100, 100, 100], [100, 200, 100], [100, 200, 300], [50,50,400], [100, 100, 100], [100, 200, 100]]

        x, y = 0,0
        self.result_canvas = resultCanvas.MyResultCanvas((x+50, y+50), result_list, search_label_stripped)
        self.result_canvas.show()

    def get_csv_file(self, path):

        if not os.path.isfile(path):
            print('Not a valid file')
            return None

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
    w = MyTableView()
    #w.load_data('example2.csv')
    w.load_data('/Users/johan/Desktop/export.csv')
    #w.search(search_list=['coop', 'ica'])
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class InstagramDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(InstagramDialog, self).__init__(parent)

        self.setGeometry(50, 50, 250, 100)
        self.setWindowTitle('Print PDF')

        main_vbox = QtGui.QVBoxLayout(self)

        grid_layout = QtGui.QGridLayout()
        main_vbox.addLayout(grid_layout)

        self.preview_widget = QtGui.QLabel()
        self.preview_widget.setMinimumSize(300,300)
        main_vbox.addWidget(self.preview_widget)

        main_vbox.addStretch()
        
        pivot_spacing_x_slider = QtGui.QDoubleSpinBox()
        pivot_spacing_x_slider.valueChanged.connect(self.pivot_spacing_x_change)
        main_vbox.addWidget(pivot_spacing_x_slider)



        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        
        main_vbox.addWidget(buttons)
        self.show()

    def pivot_spacing_x_change(self, value):
        print(value)

    def client_secret(self):
        return 12
        #return self.client_secret_lineedit.text()

    def access_token(self):
        return 23
        #return self.access_token_lineedit.text()

    @staticmethod
    def getInstagramInfo(parent = None):
        dialog = InstagramDialog(parent)
        result = dialog.exec_()
        
        client_secret = dialog.client_secret()
        access_token = dialog.access_token()

        return (client_secret, access_token, result == QtGui.QDialog.Accepted)

def main():
    
    app = QtGui.QApplication(sys.argv)
    a, b, result = InstagramDialog.getInstagramInfo()
    print("{} {} {}".format(a, b, result))
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

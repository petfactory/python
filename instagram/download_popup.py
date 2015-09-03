# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class InstagramDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(InstagramDialog, self).__init__(parent)

        self.setGeometry(50, 50, 250, 100)
        self.setWindowTitle('Download')

        main_vbox = QtGui.QVBoxLayout(self)

        grid_layout = QtGui.QGridLayout()
        main_vbox.addLayout(grid_layout)

        access_token_label = QtGui.QLabel('Access Token:')
        grid_layout.addWidget(access_token_label, 0, 0)
        self.access_token_lineedit = QtGui.QLineEdit()
        grid_layout.addWidget(self.access_token_lineedit, 0, 1)

        client_secret_label = QtGui.QLabel('Client Secret:')
        grid_layout.addWidget(client_secret_label, 1, 0)
        self.client_secret_lineedit = QtGui.QLineEdit()
        grid_layout.addWidget(self.client_secret_lineedit, 1, 1)


        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_vbox.addWidget(buttons)

        main_vbox.addStretch()
        self.show()

    def client_secret(self):
        return self.client_secret_lineedit.text()

    def access_token(self):
        return self.access_token_lineedit.text()

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

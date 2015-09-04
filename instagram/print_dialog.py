# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
import grid_setup
#from wand.image import Image
#from wand.color import Color
import preview_canvas

class InstagramDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(InstagramDialog, self).__init__(parent)

        self.setGeometry(50, 50, 250, 100)
        self.setWindowTitle('Print PDF')
        self.preview_canvas = preview_canvas.PreviewCanvas()

        main_vbox = QtGui.QVBoxLayout(self)

        grid_layout = QtGui.QGridLayout()
        main_vbox.addLayout(grid_layout)

        main_vbox.addWidget(self.preview_canvas)

        main_vbox.addStretch()
        
        self.pivot_spacing_x_slider = QtGui.QDoubleSpinBox()
        self.pivot_spacing_x_slider.setRange(0,1000)
        self.pivot_spacing_x_slider.setValue(220)
        self.pivot_spacing_x_slider.valueChanged.connect(self.slider_change)
        main_vbox.addWidget(self.pivot_spacing_x_slider)


        self.pivot_spacing_y_slider = QtGui.QDoubleSpinBox()
        self.pivot_spacing_y_slider.setRange(0,1000)
        self.pivot_spacing_y_slider.setValue(220)
        self.pivot_spacing_y_slider.valueChanged.connect(self.slider_change)
        main_vbox.addWidget(self.pivot_spacing_y_slider)


        self.size_slider = QtGui.QDoubleSpinBox()
        self.size_slider.setRange(0,1000)
        self.size_slider.setValue(130)
        self.size_slider.valueChanged.connect(self.slider_change)
        main_vbox.addWidget(self.size_slider)



        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        
        main_vbox.addWidget(buttons)
        self.show()

        self.slider_change()

    def slider_change(self):
        rect_list = grid_setup.test_layout(self.pivot_spacing_x_slider.value(), self.pivot_spacing_y_slider.value(), self.size_slider.value(), 4, 2, 2)
        self.preview_canvas.set_rect_list(rect_list)


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

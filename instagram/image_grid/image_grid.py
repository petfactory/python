import os
import sys
from PySide import QtGui, QtCore

class IconButton(QtGui.QPushButton):

    def __init__(self, pixmap, name, parent=None):
        QtGui.QPushButton.__init__(self, pixmap, parent)
        self.name = name
        self.pixmap = pixmap

        self.off_pixmap = QtGui.QPixmap()
        self.off_pixmap.fill(fillColor=QtCore.Qt.white)

        self.is_off = False

    def toggle_me(self, val):
        self.is_off = not self.is_off
        pm = self.off_pixmap if self.is_off else self.pixmap
        self.setIcon(pm)


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.exclude_list = []

    def initUI(self):
        
        num_col = 1
        v_box = QtGui.QVBoxLayout(self)
        h_box = QtGui.QHBoxLayout()
        v_box.addLayout(h_box)

        
        self.image_widget = QtGui.QLabel()
        pixmap = QtGui.QPixmap('highres/11325467_827835693952267_1145886703_n.jpg')
        self.image_widget.setPixmap(pixmap)
        h_box.addWidget(self.image_widget)


        h_box.addStretch()
        
        scrollarea = QtGui.QScrollArea()
        scrollarea.setFixedWidth(130)
        scrollarea.setWidgetResizable(True)
        scrollarea.setFrameStyle(QtGui.QFrame.NoFrame)
        h_box.addWidget(scrollarea)

        btn_widget = QtGui.QWidget()
        scroll_vbox = QtGui.QVBoxLayout(btn_widget)
        scrollarea.setWidget(btn_widget)

        thumbs_dir = r"thumbs"

        for img in os.listdir(thumbs_dir):

            img_path = os.path.join(thumbs_dir, img)
            #print(os.path.splitext(img)[1] is '')
            if img.split('.')[-1] not in ('jpeg'):
                continue

            pixmap = QtGui.QPixmap(img_path)

            #btn = QtGui.QPushButton(pixmap, "")
            btn = IconButton(pixmap, img)
            btn.clicked.connect(self.thumb_clicked)
            
            
            #btn.setCheckable(True)
            size = pixmap.size()
            w, h = size.toTuple()
            btn.setIconSize(size)
            btn.setFixedSize(w+30, h+30)
            
            scroll_vbox.addWidget(btn)


        self.setGeometry(50, 50, 400, 400)
        self.setWindowTitle('Image viewer')
        self.show()

    def thumb_clicked(self):

        modifiers = QtGui.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ControlModifier:

            if self.sender().is_off:
                self.exclude_list.remove(self.sender().name)
            else:
                self.exclude_list.append(self.sender().name)
                
            self.sender().toggle_me(False)
            
        else:
            print('Number of excluded images: {}'.format(len(self.exclude_list)))
            print(self.sender().name)
            #pixmap = QtGui.QPixmap('highres/{}'.format(self.sender().name))
            pixmap = QtGui.QPixmap('highres/{}'.format('11379787_969363229761322_1240199567_n.jpg'))
            self.image_widget.setPixmap(pixmap)

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
import os, sys, json, pprint, copy
from PySide import QtGui, QtCore
from wand.image import Image

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
        self.exclude_list = []
        self.thumb_size = 64
        self.json_data = None
        self.initUI()

    def initUI(self):

        main_hbox = QtGui.QHBoxLayout(self)

        # the main image viewer
        viewer_vbox = QtGui.QVBoxLayout()
        main_hbox.addLayout(viewer_vbox)
        self.image_widget = QtGui.QLabel()
        self.image_widget.setMinimumSize(640,640)
        viewer_vbox.addWidget(self.image_widget)

        button_hbox = QtGui.QHBoxLayout()
        viewer_vbox.addLayout(button_hbox)
        load_btn = QtGui.QPushButton('Load')
        load_btn.clicked.connect(self.load_btn_clicked)
        button_hbox.addWidget(load_btn)

        save_btn = QtGui.QPushButton('Save')
        save_btn.clicked.connect(self.save_btn_clicked)
        button_hbox.addWidget(save_btn)

        print_pdf_btn = QtGui.QPushButton('Print PDF')
        print_pdf_btn.clicked.connect(self.print_pdf_btn_clicked)
        button_hbox.addWidget(print_pdf_btn)

        scrollarea = QtGui.QScrollArea()
        scrollarea.setFixedWidth(130)
        scrollarea.setWidgetResizable(True)
        scrollarea.setFrameStyle(QtGui.QFrame.NoFrame)
        main_hbox.addWidget(scrollarea)

        scroll_widget = QtGui.QWidget()
        self.scroll_vbox = QtGui.QVBoxLayout(scroll_widget)
        scrollarea.setWidget(scroll_widget)

        self.setGeometry(50, 50, 400, 400)
        self.setWindowTitle('Image viewer')
        self.show()

    def create_thumb(self, img_path):

        img = Image(filename=os.path.join('highres', img_path))
        img.resize(self.thumb_size, self.thumb_size)

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(img.make_blob())

        btn = IconButton(pixmap, img_path)
        btn.clicked.connect(self.thumb_clicked)

        size = pixmap.size()
        w, h = size.toTuple()
        btn.setIconSize(size)
        btn.setFixedSize(w+20, h+20)

        
        self.scroll_vbox.addWidget(btn)

    def add_images(self, json_data):

        media_list = json_data.get('media')

        if not media_list:
            print('Could not get media list from json')
            return None

        for media in media_list:
            self.create_thumb(media.get('filename'))

        self.scroll_vbox.addStretch()
        pixmap = QtGui.QPixmap(os.path.join('highres', media_list[0].get('filename')))
        self.image_widget.setPixmap(pixmap)

        return json_data

    def load_btn_clicked(self):

        file_name, selected_filter = QtGui.QFileDialog.getOpenFileName(None, 'Load image json', None, filter='JSON (*.json)')
    
        if file_name:

            # clear the scroll layout
            while self.scroll_vbox.count():
                child = self.scroll_vbox.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()

            data = None
            with open(file_name, 'r') as f:
                data = f.read()
            
            if data:
                json_data = json.loads(data)
                self.json_data = json_data
                self.add_images(json_data)
        else:
            return None


    def save_btn_clicked(self):

        if not self.json_data:
            print('No json data loaded')
            return

        media_list = self.json_data.get('media')
        if not media_list:
            print('No media found')
            return

        # copy the json_dict, clear the media list
        save_dict = copy.deepcopy(self.json_data)
        save_media_list = []
        save_dict['media'] = save_media_list

        for media in media_list:
            filename = media.get('filename')

            if filename in self.exclude_list:
                print('skipping... {}'.format(filename))
                continue

            save_media_list.append(media)

        file_name, selected_filter = QtGui.QFileDialog.getSaveFileName(None, 'Save image json', None, filter='JSON (*.json)')

        json_data = json.dumps(save_dict, indent=4)
        
        if file_name:
            with open(file_name, 'w') as f:
                f = open(file_name,'w')
                f.write(json_data)
                f.close()
                print('Data saved to file: {0}'.format(file_name))       

        else:
            print('Could not save file')

    def thumb_clicked(self):

        modifiers = QtGui.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ControlModifier:

            if self.sender().is_off:
                self.exclude_list.remove(self.sender().name)
            else:
                self.exclude_list.append(self.sender().name)

            self.sender().toggle_me(False)

        else:
            #print('Number of excluded images: {}'.format(len(self.exclude_list)))
            pixmap = QtGui.QPixmap('highres/{}'.format(self.sender().name))
            self.image_widget.setPixmap(pixmap)

    def print_pdf_btn_clicked(self):
        print('Printing pdf')

        if not self.json_data:
            print('No json data loaded')
            return

        media_list = self.json_data.get('media')
        if not media_list:
            print('No media found')
            return

        for media in media_list:
            filename = media.get('filename')

            if filename in self.exclude_list:
                print('skipping... {}'.format(filename))
                continue

            else:
                print('Printing {}'.format(filename))

        print('pdf created!')

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

import os, sys, json, pprint, copy
from PySide import QtGui, QtCore
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import instagram_downloader
import download_popup
import print_dialog

class IconButton(QtGui.QPushButton):

    def __init__(self, pixmap_on, pixmap_off, name, date, text, parent=None):
        QtGui.QPushButton.__init__(self, pixmap_on, parent)
        self.name = name
        self.date = date
        self.text = text
        #print(text)

        self.pixmap_on = pixmap_on
        self.pixmap_off = pixmap_off

        #self.off_pixmap = QtGui.QPixmap()
        #self.off_pixmap.fill(fillColor=QtCore.Qt.white)

        self.is_off = False

    def toggle_me(self, val):
        self.is_off = not self.is_off
        pm = self.pixmap_off if self.is_off else self.pixmap_on
        self.setIcon(pm)


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.exclude_list = []
        self.thumb_size = 64
        self.json_data = None
        self.source_dir = None
        self.initUI()

    def initUI(self):

        outer_vbox = QtGui.QVBoxLayout(self)
        outer_vbox.setContentsMargins(0,0,0,0)

        menubar = QtGui.QMenuBar()
        outer_vbox.addWidget(menubar)
        menubar.setNativeMenuBar(False)

        file_menu = menubar.addMenu('File')

        load_json_action = QtGui.QAction('Load json', self)
        load_json_action.triggered.connect(self.load_btn_clicked)
        file_menu.addAction(load_json_action)

        save_json_action = QtGui.QAction('Save json', self)
        save_json_action.triggered.connect(self.save_btn_clicked)
        file_menu.addAction(save_json_action)

        print_pdf_action = QtGui.QAction('Print PDF', self)
        print_pdf_action.triggered.connect(self.print_pdf_btn_clicked)
        file_menu.addAction(print_pdf_action)

        download_action = QtGui.QAction('Download from Instagram', self)
        download_action.triggered.connect(self.download_from_instagram)
        file_menu.addAction(download_action)


        main_hbox = QtGui.QHBoxLayout()
        outer_vbox.addLayout(main_hbox)
        main_hbox.setContentsMargins(7,7,7,7)
        
        # the main image viewer
        viewer_vbox = QtGui.QVBoxLayout()
        main_hbox.addLayout(viewer_vbox)
        self.image_widget = QtGui.QLabel()
        self.image_widget.setMinimumSize(640,640)
        viewer_vbox.addWidget(self.image_widget)
        #viewer_vbox.addStretch()

        self.date_label = QtGui.QLabel()
        viewer_vbox.addWidget(self.date_label)

        self.caption_textedit = QtGui.QTextEdit()
        self.caption_textedit.setMaximumWidth(640)
        viewer_vbox.addWidget(self.caption_textedit)


        save_caption_button = QtGui.QPushButton('Save text')
        viewer_vbox.addWidget(save_caption_button)



        #fontDB = QtGui.QFontDatabase()
        #print(fontDB)
        #fontDB.addApplicationFont("/Library/Fonts/Apple Color Emoji.ttf")
        sansFont = QtGui.QFont("Menlo", 18)
        #sansFont = QtGui.QFont("Apple Color Emoji", 18)
        
        #print(sansFont)
        self.caption_textedit.setFont(sansFont)
        #print(a)
        #self.caption_lineedit.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)




        scrollarea = QtGui.QScrollArea()
        scrollarea.setFixedWidth(130)
        scrollarea.setWidgetResizable(True)
        scrollarea.setFrameStyle(QtGui.QFrame.NoFrame)
        main_hbox.addWidget(scrollarea)

        scroll_widget = QtGui.QWidget()
        self.scroll_vbox = QtGui.QVBoxLayout(scroll_widget)
        scrollarea.setWidget(scroll_widget)

        self.setGeometry(0, 50, 400, 400)
        self.setWindowTitle('Image viewer')
        self.show()

    def download_from_instagram(self):

        client_secret, access_token, result = download_popup.InstagramDialog.getInstagramInfo(self)

        if result:
            dir_path = QtGui.QFileDialog.getExistingDirectory(None, 'Choose dir to download to', None, QtGui.QFileDialog.ShowDirsOnly)

            if dir_path:
                instagram_downloader.on_user_media_feed(dest_dir=dir_path, client_secret=client_secret, access_token=access_token, year=2015, max_count=10)

    def create_thumb(self, img_path, date, text):

        img = Image(filename=os.path.join(self.source_dir, img_path))
        img.resize(self.thumb_size, self.thumb_size)

        pixmap_on = QtGui.QPixmap()
        pixmap_on.loadFromData(img.make_blob())

        with Drawing() as draw:
            draw.stroke_color = Color('white')
            draw.stroke_width = 3
            draw.line((0, 0), (self.thumb_size, self.thumb_size))
            draw.line((0, self.thumb_size), (self.thumb_size , 0))
            draw(img)

        pixmap_off = QtGui.QPixmap()
        pixmap_off.loadFromData(img.make_blob())
        
        btn = IconButton(pixmap_on, pixmap_off, img_path, date, text)
        btn.clicked.connect(self.thumb_clicked)

        size = pixmap_on.size()
        w, h = size.toTuple()
        btn.setIconSize(size)
        btn.setFixedSize(w+20, h+20)

        self.scroll_vbox.addWidget(btn)

    def add_images(self, json_data):

        media_list = json_data.get('media')
        #print(media_list)
        #return

        if not media_list:
            print('Could not get media list from json')
            return None

        for media in media_list:
            self.create_thumb(media.get('filename'), media.get('date'), media.get('text'))

        self.scroll_vbox.addStretch()
        pixmap = QtGui.QPixmap(os.path.join(self.source_dir, media_list[0].get('filename')))
        self.image_widget.setPixmap(pixmap)

        self.date_label.setText(media_list[0].get('date'))
        text = media_list[0].get('text')
        #text = text.encode('UTF-8')
        #print(text)
        #print(type(text))

        #text = text.decode("utf-32")

        self.caption_textedit.setText(text)

        #return json_data

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

                self.source_dir = os.path.dirname(file_name)
                print(self.source_dir)

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
            pixmap = QtGui.QPixmap(os.path.join(self.source_dir, self.sender().name))
            self.image_widget.setPixmap(pixmap)

            self.date_label.setText(self.sender().date)
            text = self.sender().text
            #print(text)
            #text = text.encode('utf-8')
            print(text.encode('utf-8'))
            self.caption_textedit.setText(text)

    def print_pdf_btn_clicked(self):

        print_dialog.InstagramDialog.getInstagramInfo(self)
        return

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

    def debug_load(self, file_path):

        with open(file_path, 'r') as f:
            data = f.read()
            self.source_dir = os.path.dirname(file_path)
            print(self.source_dir)

        if data:
            json_data = json.loads(data)
            self.json_data = json_data
            self.add_images(json_data)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.debug_load('/Users/johan/Desktop/anna/instagram.json')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
#!/usr/bin/python

from PySide import QtCore, QtGui
import pprint
import sys
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from functools import partial


class CustomType(object):
    
    def __init__(self, node):
        self._node = node
        
    def getNode(self):
        return self._node

class ParentItem(QtGui.QStandardItem):
    pass
    
class ChildItem(QtGui.QStandardItem):
    pass

class DeselectableTreeView(QtGui.QTreeView):
    
    # deselect when clicked outside the items
    def mousePressEvent(self, event):
        self.clearSelection()
        QtGui.QTreeView.mousePressEvent(self, event)
        
    # disable doubleclick
    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)

class HierarchyTreeview(QtGui.QWidget):
 
    def __init__(self, parent=None):
 
        super(HierarchyTreeview, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        #self.hex_color_grey = '#dd0000'

        self.setGeometry(10, 50, 300, 400)
        self.setWindowTitle("TEST")
                
        vbox = QtGui.QVBoxLayout(self)
        vbox.setContentsMargins(0,0, 0, 0)

        # splitter
        splitter = QtGui.QSplitter()
        vbox.addWidget(splitter)


        treeview_parent_widget = QtGui.QWidget()
        treeview_vbox = QtGui.QVBoxLayout(treeview_parent_widget)

        # treeview
        self.treeview = QtGui.QTreeView() #DeselectableTreeView()
        self.treeview.setAlternatingRowColors(True)
        treeview_vbox.addWidget(self.treeview)

        refresh_button = QtGui.QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_button_clicked)

        treeview_vbox.addWidget(refresh_button)
        
        splitter.addWidget(treeview_parent_widget)
        self.treeview.setHeaderHidden(True)
        self.treeview.setExpandsOnDoubleClick(False)
        
        # model
        self.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.model)

        self.populateModel()


        self.treeview.setStyleSheet(
        ''' QTreeView {
                alternate-background-color: #AAAAAA;
                background: #A2A2A2;
                color: rgb(90, 90, 90);
                selection-background-color: #555555;
            }
            QTreeView::item:focus {
              background-color: #555555;
              color: #ffcc00;
            }

            QTreeView::branch::closed::has-children {
                image: url(branch_closed.png);
            }

            QTreeView::branch::open::has-children {
                image: url(branch_open.png);
            }
        '''
        )

        button_widget = QtGui.QWidget()
        self.button_vbox = QtGui.QVBoxLayout(button_widget)

        splitter.addWidget(button_widget)
        self.button_vbox.addStretch()

        splitter.setSizes([500, 300])

    def refresh_button_clicked(self):

        for name in ['Level 2 A', 'Level 4 A', 'Level 1 B']:
            self.add_button(name, self.button_vbox)

    def add_button(self, name, layout):

        path = None
        for dag_path in self.dag_path_list:
            if name in dag_path:
                path = dag_path
                break
            #break

        if path is None:
            print 'Did not find name in hierarchy, skip to add button'
            return

        button = QtGui.QPushButton(name)
        button.clicked.connect(partial(self.button_clicked, path))
        layout.addWidget(button)

    def button_clicked(self, name):
        print name

    def cleanModel(self):
         numRows = self.model.rowCount()
         for row in range(numRows):
             self.model.removeRow(0)

    def create_item_recurse(self, xml_node, parent_item):

        name = xml_node.get('name')
        #node = Node(name)

        item = ParentItem(name)
        #item.setSizeHint(QtCore.QSize(0,20))
        
        #customData = CustomType(node)
        #item.setData(customData, QtCore.Qt.UserRole + 1)
        parent_item.appendRow(item)

        xml_children = xml_node.getchildren()

        if xml_children:

            for xml_child in xml_children:

                self.create_item_recurse(xml_child, item)

    def populateModel(self):

        dirName = os.path.dirname(os.path.realpath(__file__))
        xmlPath = os.path.join(dirName, r'scenegraph.xml')

        if not os.path.isfile(xmlPath):
            print('The xml file does not exist: {}'.format(xmlPath))
            return

        xml_tree = ET.parse(xmlPath)
        xml_root = xml_tree.getroot()


        # recurse the treeview instead...
        self.dag_path_list = []
        full_dag_path_recurse(xml_root, self.dag_path_list)
        #pprint.pprint(self.dag_path_list)

        self.cleanModel()
        root_item = self.model.invisibleRootItem()

        self.create_item_recurse(xml_root, root_item)


def full_dag_path_recurse(xml_node, dag_path_list, parent_list=None):

    if parent_list is None:
        parent_list = []

    name = xml_node.get('name')
    parent_list.append(name)
    full_path = ' | '.join(parent_list)
    #print full_path

    dag_path_list.append(full_path)

    xml_children = xml_node.getchildren()

    if xml_children:

        for xml_child in xml_children:

            full_dag_path_recurse(xml_child, dag_path_list, parent_list)

    parent_list.pop()


def main():
    
    app = QtGui.QApplication(sys.argv)
    win = HierarchyTreeview()
    win.show()
    win.treeview.expandAll()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

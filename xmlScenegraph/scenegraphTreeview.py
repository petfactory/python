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
        
        self.setGeometry(10, 50, 300, 400)
        self.setWindowTitle("TEST")
                
        vbox = QtGui.QVBoxLayout(self)

        # treeview
        self.treeview = DeselectableTreeView()
        vbox.addWidget(self.treeview)
        self.treeview.setHeaderHidden(True)
        self.treeview.setExpandsOnDoubleClick(False)
        
        # model
        self.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.model)

        self.populateModel()


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

        self.cleanModel()
        root_item = self.model.invisibleRootItem()

        self.create_item_recurse(xml_root, root_item)

def main():
    
    app = QtGui.QApplication(sys.argv)
    win = HierarchyTreeview()
    win.show()
    win.treeview.expandAll()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

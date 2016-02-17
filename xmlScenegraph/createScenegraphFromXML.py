import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

def createDefaultScenegraph():

    dirName = os.path.dirname(os.path.realpath(__file__))
    xmlPath = os.path.join(dirName, r'scenegraph.xml')

    if not os.path.isfile(xmlPath):
        print('The xml file does not exist: {}'.format(xmlPath))
        return

    tree = ET.parse(xmlPath)
    root = tree.getroot()

    for childNode in root:
        createScenegraphRecurse(childNode)

def createScenegraphRecurse(xmlNode, parent_list=None):

    if parent_list is None:
        parent_list = []

    name = xmlNode.get('name')
    parent_list.append(name)
    full_path = ' | '.join(parent_list)
    print full_path

    xmlChildren = xmlNode.getchildren()

    if xmlChildren:

        for xmlChild in xmlChildren:

            createScenegraphRecurse(xmlChild, parent_list)

    parent_list.pop()

createDefaultScenegraph()
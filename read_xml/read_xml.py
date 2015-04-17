import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()

for child in root:
   #print child.tag, child.attrib
   pass


for neighbor in root.iter('neighbor'):
   #print neighbor.attrib
   pass


n_list = root.findall("./country/neighbor")
for n in n_list:
    print(n.tag)
    print(n.attrib)

n_list = root.findall("./country/year")
for n in n_list:
    print(n.tag)
    print(n.text)
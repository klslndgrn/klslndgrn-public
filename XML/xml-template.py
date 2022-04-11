"""This is a template that can be used when working with XML files"""

# TODO: Add ".find()", ".findall()", ".remove()"

# Required library to be included.
import xml.etree.ElementTree as ET

# XML file to be read. 
file = r'C:\Users\klsln\Documents\GitHub\klslndgrn\XML\books.xml'

# Creating an XML tree from file.
tree = ET.parse(file)

# Accesssing root in XML tree.
root = tree.getroot()

# Print childs tag and attribute
for child in root:
    print (child.tag, child.attrib)

# Prints number of tags which is called "book".
booknum = 0
for child in root:
    if child.tag == 'book':
        booknum += 1
print(f'{booknum} number of books')


# Print a list of all book tags.
booktags = []
for child in root.iter('book'):
    for childx in child:
        if childx.tag not in booktags:
            booktags.append(childx.tag)
print(f'Book tags = {booktags}')

# Print a list of all tags.
tags = []
for child in root.iter():
    if child.tag not in tags:
        tags.append(child.tag)
print(f'All tags = {tags}')

# Prints a list of all attributes called "id", i.e. a list of all id-tags.
bookid = []
for idz in root:
    att = idz.attrib['id']
    bookid.append(att)
print(bookid)

# Prints a list of all book titles.
booktitles = []
for ti in root.iter('title'):
    booktitles.append(ti.text)
print(booktitles)

# Creating a dictionary with id and book titles
bookdict = dict(zip(bookid,booktitles))
print(bookdict)
    
# bookdict = {}
# for k,v in zip(root.iter('id'),root):
#     print(k.text)
#     print(v.text)
#     bookdict[k.attrib['id']] = v.text
# print(bookdict)

# Prints a list containing all books published in 2001. 
books2001 = []
for n,twok in enumerate(root.iter('publish_date')):
    if '2001' in twok.text: 
        books2001.append(booktitles[n])
print(books2001)
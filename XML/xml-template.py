import xml.etree.ElementTree as ET

file = r'C:\Users\klsln\Documents\GitHub\klslndgrn\XML\books.xml'
tree = ET.parse(file)

# Access root
root = tree.getroot()

# Print childs tag and attribute
for child in root:
    print (child.tag, child.attrib)

# NUMBER OF BOOKS
booknum = 0
for child in root:
    if child.tag == 'book':
        booknum += 1
print(f'{booknum} number of books')

# # TAGS UNDER BOOK 1
# booktags = []
# for child in root.iter():
#     for childx in child:
#         if childx.tag not in booktags:
#             booktags.append(childx.tag)
# print(f'Book tags = {booktags}')

# TAGS UNDER BOOK 2
booktags = []
for child in root.iter('book'):
    for childx in child:
        if childx.tag not in booktags:
            booktags.append(childx.tag)
print(f'Book tags = {booktags}')

# ALL TAGS
tags = []
for child in root.iter():
    if child.tag not in tags:
        tags.append(child.tag)
print(f'All tags = {tags}')

# EXTRACTING ID FROM XML
bookid = []
for idz in root:
    att = idz.attrib['id']
    bookid.append(att)
print(bookid)

# EXTRACTING TITLES FROM XML
booktitles = []
for ti in root.iter('title'):
    booktitles.append(ti.text)
print(booktitles)

# CREATING DICTIONARY
bookdict = dict(zip(bookid,booktitles))
print(bookdict)
    
# bookdict = {}
# for k,v in zip(root.iter('id'),root):
#     print(k.text)
#     print(v.text)
#     bookdict[k.attrib['id']] = v.text
# print(bookdict)

# EXTRACTING TITLES FROM XML
books2001 = []
for n,twok in enumerate(root.iter('publish_date')):
    if '2001' in twok.text: 
        books2001.append(booktitles[n])
print(books2001)
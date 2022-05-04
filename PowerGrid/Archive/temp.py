

# def tags_no_show():
#     ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
#           'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
#           'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}
#     return(ns)

# # GENERAL INFORMATION ------------------------------ #
# uniqueeq = xr.unique_equipment(root)
# # print('Unique equipment =')
# # print(uniqueeq)

# eqlist = []
# for trmnls in terminal_data:
#     eqlist.append(trmnls.CE)
# equipment = xr.find_connected_equipment(root, eqlist)
# # print('Equipment connected to terminals =')
# # print(equipment)

# # XML file input ----------------------------------- #
# xml_file = 'Assignment_EQ_reduced.xml'

# # Accessing root of XML file ----------------------- #
# root = xr.read_file(xml_file)

# # ALL DATA ----------------------------------------- #
# all_data = xr.all_data(root)
# print('All Data = ')
# print(all_data)

# # EXTRACTING DATA AND CREATING CLASSES ------------- #

# busbar_data = xr.busbar_data(root)
# # print('Busbars =')
# # print(busbar_data)

# breaker_data = xr.breaker_data(root)
# # print('Breaker Data =')
# # print(breaker_data)

# shunt_data = xr.shunt_data(root)
# # print('Shunt Data =')
# # print(shunt_data)

# transformer_data = xr.transformer_data(root)
# # print('Transformer Data =')
# # print(transformer_data)

# load_data = xr.load_data(root)
# # print('Load Data =')
# # print(load_data)

# line_data = xr.line_data(root)
# # print('Line Data = ')
# # print(line_data)

# generator_data = xr.generator_data(root)
# # print('Generator Data = ')
# # print(generator_data)

# # TERMINAL DATA ------------------------------------ #
# terminal_data = xr.terminal_data(root)
# # print('Terminals =')
# # print(terminal_data)

# # CN DATA ------------------------------------------ #
# cn_data = xr.connectivity_node_data(root)
# # print('Connectivity Nodes =')
# # print(cn_data)

# # CE DATA ------------------------------------------ #
# ce_data = xr.conducting_equipment_data(root)
# # print('Conduction Equipment Data = ')
# # print(ce_data)

# --------------------------------------------------------------------------- #
# ------------------------ Data --------------------------------------------- #
# --------------------------------------------------------------------------- #

# def unique_equipment(root):
#     unieq = []
#     for equipment in root:
#         if (ns['cim'] in equipment.tag):
#             eq = equipment.tag.replace("{" + ns['cim'] + "}", "")
#             if eq not in unieq:
#                 unieq.append(eq)
#     return(unieq)


# def find_connected_equipment(root, eqlist):
#     equipment = []
#     for id in eqlist:
#         for child in root:
#             tg = child.tag.replace("{" + ns['cim'] + "}", "")
#             attrID = child.attrib.get(ns['rdf'] + 'ID')

#             if id == attrID and tg not in equipment:
#                 equipment.append(tg)
#     return(equipment)


# def find_connected_equipment_CN(root, eqlist):
#     equipment = []
#     for id in eqlist:
#         for child in root:
#             tg = child.tag.replace("{" + ns['cim'] + "}", "")
#             attrID = child.attrib.get(ns['rdf'] + 'ID')

#             if id == attrID and tg not in equipment:
#                 equipment.append(tg)
#     return(equipment)

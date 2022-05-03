import xmlread as xr

# XML file input ----------------------------------- #
# xml_file = 'Assignment_EQ_reduced.xml'


def create_data_lists(xml_file):
    # Accessing root of XML file ----------------------- #
    root = xr.read_file(xml_file)
    # ALL DATA ----------------------------------------- #
    all_data = xr.all_data(root)
    return(all_data)


# # EXTRACTING DATA AND CREATING CLASSES ------------- #

# busbar_data = xr.busbar_data(root)
# print('Busbars =')
# print(busbar_data)

# breaker_data = xr.breaker_data(root)
# print('Breaker Data =')
# print(breaker_data)

# shunt_data = xr.shunt_data(root)
# print('Shunt Data =')
# print(shunt_data)

# transformer_data = xr.transformer_data(root)
# print('Transformer Data =')
# print(transformer_data)

# load_data = xr.load_data(root)
# print('Load Data =')
# print(load_data)

# line_data = xr.line_data(root)
# print('Line Data = ')
# print(line_data)

# generator_data = xr.generator_data(root)
# print('Generator Data = ')
# print(generator_data)

# TERMINAL DATA ------------------------------------ #
# terminal_data = xr.terminal_data(root)
# print('Terminals =')
# print(terminal_data)

# CN DATA ------------------------------------------ #
# cn_data = xr.connectivity_node_data(root)
# print('Connectivity Nodes =')
# print(cn_data)

# CE DATA ------------------------------------------ #
# ce_data = xr.conducting_equipment_data(root)
# print('Conduction Equipment Data = ')
# print(ce_data)

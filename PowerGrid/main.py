# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
import xmlread as xr
import gridcreator as gc
# import grid
# import psclasses as psc
# import ceclasses as cec

# --------------------------------------------------------------------------- #
# ------------------------ METHOD FOR SOLUTION ------------------------------ #
# --------------------------------------------------------------------------- #
'''
1. Read XML and create classes
    1a. How to find stuff
    1b. Figure out how topology works
2. Algorithm
        search for topology
        (inspiration can be found in the two papers)
    Find all connectivity nodes (a list)
        -> check terminals
        -> check equipment
        -> connectivity nodea
            Is this CN a new unique one?
3. Create a data base
4. Create panda power (+ Read SSH files for values)
    Lines
    Buses
    ...
'''

# --------------------------------------------------------------------------- #
# ------------------------ RETRIEVING XML-FILE ------------------------------ #
# --------------------------------------------------------------------------- #
xml_file = 'Assignment_EQ_reduced.xml'

# Accessing root of XML file
root = xr.read_file(xml_file)

# --------------------------------------------------------------------------- #
# ------------------------ EXTRACTING DATA ---------------------------------- #
# ------------------------------ AND ---------------------------------------- #
# ------------------------ CREATING CLASSES --------------------------------- #
# --------------------------------------------------------------------------- #

terminal_data = xr.terminal_data(root)
print('Terminals =')
print(terminal_data)

cn_data = xr.connectivity_node_data(root)
print('Connectivity Nodes =')
print(cn_data)

busbar_data = xr.busbar_data(root)
print('Busbars =')
print(busbar_data)

breaker_data = xr.breaker_data(root)
print('Breaker Data =')
print(breaker_data)

shunt_data = xr.shunt_data(root)
print('Shunt Data =')
print(shunt_data)

transformer_data = xr.transformer_data(root)
print('Transformer Data =')
print(transformer_data)

load_data = xr.load_data(root)
print('Load Data =')
print(load_data)

line_data = xr.line_data(root)
print('Line Data = ')
print(line_data)

generator_data = xr.generator_data(root)
print('Generator Data = ')
print(generator_data)

# --------------------------------------------------------------------------- #
# ------------------------ GENERAL INFORMATION ------------------------------ #
# --------------------------------------------------------------------------- #

uniqueeq = xr.unique_equipment(root)
print('Unique equipment =')
print(uniqueeq)

eqlist = []
for trmnls in terminal_data:
    eqlist.append(trmnls.CE)
equipment = xr.find_connected_equipment(root, eqlist)
print('Equipment connected to terminals =')
print(equipment)

# --------------------------------------------------------------------------- #
# ------------------------ CREATING THE GRID -------------------------------- #
# --------------------------------------------------------------------------- #

net = gc.grid_initializer
busbar = busbar_data[0]
print(busbar)
# bus = grid.create_bus(net, busbar)

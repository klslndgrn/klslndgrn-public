# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
import xmlread as xr
# import gridcreator as gc
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

# Accessing root of XML file ----------------------- #
root = xr.read_file(xml_file)

# --------------------------------------------------------------------------- #
# ------------------------ EXTRACTING DATA ---------------------------------- #
# --------------------------------------------------------------------------- #

# TERMINAL DATA ------------------------------------ #
terminal_data = xr.terminal_data(root)
print('Terminals =')
print(terminal_data)

# CONNECTIVY NODE DATA ----------------------------- #
cn_data = xr.connectivity_node_data(root)
print('Connectivity Nodes =')
print(cn_data)

# CONDUCTING EQUIPMENT DATA ------------------------ #
ce_data = xr.conducting_equipment_data(root)
print('Conduction Equipment Data = ')
print(ce_data)


# --------------------------------------------------------------------------- #
# ------------------------ CREATING THE GRID -------------------------------- #
# --------------------------------------------------------------------------- #

# net = gc.grid_initializer
# busbar = busbar_data[0]
# print(busbar)
# bus = grid.create_bus(net, busbar)

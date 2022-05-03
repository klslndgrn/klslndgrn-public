# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
# import xmlread as xr
# import gridcreator as gc
import gridcreator as gc
# import pandapower as pp
import grid as g
# from data import root
from data import all_data

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


# --------------------------------------------------------------------------- #
# ------------------------ EXTRACTING DATA ---------------------------------- #
# --------------------------------------------------------------------------- #

# # TERMINAL DATA ------------------------------------ #
# terminal_data = xr.terminal_data(root)
# print('Terminals =')
# print(terminal_data)

# # CONNECTIVY NODE DATA ----------------------------- #
# cn_data = xr.connectivity_node_data(root)
# print('Connectivity Nodes =')
# print(cn_data)

# # CONDUCTING EQUIPMENT DATA ------------------------ #
# ce_data = xr.conducting_equipment_data(root)
# print('Conduction Equipment Data = ')
# print(ce_data)

# # ALL DATA ----------------------------------------- #
# all_data = xr.all_data(root)
# print('All Data = ')
# print(all_data)

# --------------------------------------------------------------------------- #
# ------------------------ CREATING THE GRID -------------------------------- #
# --------------------------------------------------------------------------- #

grid_data = all_data
net, grid_data = gc.grid_initializer(grid_data)

print(net.bus)

net, grid_data = gc.grid_creator(net, grid_data)

# print(grid_data)

print(net)

g.plot_grid(net)

# --------------------------------------------------------------------------- #
# ------------------------ TESTING ------------------------------------------ #
# --------------------------------------------------------------------------- #


# def find_specific(data):
#     for i in data:
#         if i.Type == 'CE':
#             if i.CE_Type == 'BusBar':
#                 return(i)
#             else:
#                 pass
#         else:
#             pass


# busbar = find_specific(all_data)
# print(busbar)

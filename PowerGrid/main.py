# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
import gridcreator as gc
import grid as g
from data import all_data

# --------------------------------------------------------------------------- #
# ------------------------ CREATING THE GRID -------------------------------- #
# --------------------------------------------------------------------------- #

grid_data = all_data
net, grid_data = gc.grid_initializer(grid_data)

net, grid_data = gc.grid_creator(net, grid_data)

print(net)

g.plot_grid(net)

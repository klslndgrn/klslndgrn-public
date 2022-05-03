# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
import gridcreator as gc
import grid as g
import data


def main(xml_file):
    # Retreiving data from XML file ---------------- #
    grid_data = data.create_data_lists(xml_file)

    # CREATING THE GRID ---------------------------- #
    net, grid_data = gc.grid_initializer(grid_data)
    net, grid_data = gc.grid_creator(net, grid_data)

    print(net)

    g.plot_grid(net)


if __name__ == "__main__":
    xml_file = 'Assignment_EQ_reduced.xml'
    main(xml_file)

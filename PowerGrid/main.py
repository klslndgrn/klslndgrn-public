# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
import gridcreator as gc
import grid as g
import data


def main(xml_file):  # (eq_file, shh_file)
    # Retreiving data from XML file ---------------- #
    grid_data = data.create_data_lists(xml_file)

    # CREATING THE GRID ---------------------------- #
    net, grid_data = gc.grid_initializer(grid_data)
    net, grid_data = gc.grid_creator(net, grid_data)

    print(net)

    g.plot_grid(net)
    return(net)


if __name__ == "__main__":
    # xml_file = 'Assignment_EQ_reduced.xml'
    xml_file = 'MicroGridTestConfiguration_T1_BE_EQ_V2.xml'
    main(xml_file)

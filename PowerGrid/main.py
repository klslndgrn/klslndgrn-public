# MAIN FILE FOR ASSINGMENT 1:

# Needed Libaries
import gridcreator as gc
import grid as g
import eqread as eqr
import sshread as shr


def main(eq_file, ssh_file):  # (eq_file, shh_file)
    # Retreiving data from XML file ---------------- #
    # Creating equipment --------------------------- #
    eq_data = eqr.create_data_lists(eq_file)

    # Updating equipment data with SSH data -------- #
    grid_data = shr.update_data_lists(eq_data, ssh_file)

    # CREATING THE GRID ---------------------------- #
    net, grid_data = gc.grid_initializer(grid_data)
    net, grid_data = gc.grid_creator(net, grid_data)

    # print(grid_data)

    print(net)

    g.plot_grid(net)

    return(net)


if __name__ == "__main__":
    # eq_file = 'Assignment_EQ_reduced.xml'
    # ssh_file = 'Assignment_SSH_reduced.xml'
    eq_file = 'MicroGridTestConfiguration_T1_BE_EQ_V2.xml'
    ssh_file = 'MicroGridTestConfiguration_T1_BE_SSH_V2.xml'
    main(eq_file, ssh_file)

from matplotlib.pyplot import grid
import gridcreator as gc
import grid as g
import eqread as eqr
import sshread as shr


def main(eq_file, ssh_file):  # (eq_file, shh_file)
    '''
    Main function which reads EQ and SSH XML as well as creating the grid in
    PandaPower.
    '''
    # Retreiving data from XML file ---------------- #
    # and creating equipment ----------------------- #
    eq_data = eqr.create_data_lists(eq_file)

    # Updating equipment data with SSH data -------- #
    grid_data = shr.update_data_lists(eq_data, ssh_file)

    # Creating the grid ---------------------------- #
    net, grid_data = gc.grid_initializer(grid_data)
    net, grid_data = gc.grid_creator(net, grid_data)

    data_processed = gc.equipment_processed_check(grid_data)

    return(net, data_processed)


def main_plot(net):
    '''
    Plot created grid using PandaPower and SimplePlot.
    '''
    if __name__ == "__main__":
        print(net)
    # Plot the grid -------------------------------- #
    g.plot_grid(net)


def main_print(net, str):
    ''''
    Print output of created grid.
    '''
    output = gc.output_string(net, str)
    return(output)


if __name__ == "__main__":
    '''
    If main.py is ran without GUI, the following will occur.
    Please put files in the Files folder and reference them by name below.
    '''

    eq_file = 'Assignment_EQ_reduced.xml'
    ssh_file = 'Assignment_SSH_reduced.xml'

    # eq_file = 'MicroGridTestConfiguration_T1_BE_EQ_V2.xml'
    # ssh_file = 'MicroGridTestConfiguration_T1_BE_SSH_V2.xml'
    
    # eq_file = 'MicroGridTestConfiguration_T1_NL_EQ_V2.xml'
    # ssh_file = 'MicroGridTestConfiguration_T1_NL_SSH_V2.xml'

    net, status = main(eq_file, ssh_file)
    print(f'All XML-data processed = {status}')
    main_plot(net)

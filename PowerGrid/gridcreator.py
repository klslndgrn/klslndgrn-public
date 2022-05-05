import grid as g
import io
from contextlib import redirect_stdout


def flag_step(node):
    '''
    Flags PowerSystemEquipment as processed = True.
    '''
    node.Processed = True


def grid_initializer(grid_data):
    '''
    A function to initialize the creation of the grid.
    First an empty grid is created, then BusBars are created and thereafter
    are nodes created without duplicates of the busbars.
    '''
    # Creating an empty grid ----------------------- #
    net = g.create_grid()
    # Creating BusBars ----------------------------- #
    name_list = []
    for node in grid_data:
        if node.Type == 'CE':
            if node.CE_Type == 'BusBar':
                # print(i)
                name_list.append(node.Name)
                g.create_bus(net, node)
                flag_step(node)
            else:
                pass
        else:
            pass
    # Creating Nodes ------------------------------- #
    for node in grid_data:
        if node.Type == 'CN' and node.Name not in name_list:
            # print(i)
            g.create_node(net, node)
            flag_step(node)
        else:
            flag_step(node)
            pass
    # Returning grid and grid data ----------------- #
    # (with updated flags) ------------------------- #
    return(net, grid_data)


def grid_creator(net, grid_data):
    '''
    The conducting equipment is created in the grid. This includes breakers,
    shunts, transformers, lines, loads and generators.
    '''
    for node in grid_data:
        if node.Type == 'CE':
            if node.CE_Type == 'Breaker':
                # Creating Switches ---------------- #
                g.create_switch(net, node, grid_data)
                flag_step(node)
            elif node.CE_Type == 'Shunt':
                # Creating Shunts ------------------ #
                g.create_shunt(net, node, grid_data)
                flag_step(node)
            elif node.CE_Type == 'Transformer':
                # Creating Transformers ------------ #
                g.create_transformer(net, node, grid_data)
                flag_step(node)
            elif node.CE_Type == 'Line':
                # Creating Lines ------------------- #
                g.create_line(net, node, grid_data)
                flag_step(node)
            elif node.CE_Type == 'Load':
                # Creating Loads ------------------- #
                g.create_load(net, node, grid_data)
                flag_step(node)
            elif node.CE_Type == 'Generator':
                # Creating Generators -------------- #
                g.create_generator(net, node, grid_data)
                flag_step(node)
            else:
                # print(f'{node.Name} is not created')
                pass
        else:
            pass
    return(net, grid_data)


def output_string(net, string):
    '''
    A function to create strings from terminal output.
    This is used to print detailed data of the created grid.
    '''
    file = io.StringIO()
    with redirect_stdout(file):
        if string == 'all':
            print(net)
        elif string == 'bus':
            print(net.bus)
        elif string == 'load':
            print(net.load)
        elif string == 'gen':
            print(net.gen)
        elif string == 'switch':
            print(net.switch)
        elif string == 'shunt':
            print(net.shunt)
        elif string == 'line':
            print(net.line)
        elif string == 'trafo':
            print(net.trafo)
    output = file.getvalue()
    return(output)


def equipment_processed_check(grid_data):
    '''
    A function that checks whether all equipment is processed in the algorithm.
    '''
    status = True
    for equipment in grid_data:
        if equipment.Processed is False:
            status = False
        else:
            pass
    return(status)

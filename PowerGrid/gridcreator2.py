import grid as g


def flag_step(node):
    node.Processed = True


def grid_initializer(grid_data):
    # Creating an empty grid ----------------------- #
    net = g.create_grid()

    # Creating BusBars ----------------------------- #
    for node in grid_data:
        if node.Type == 'CE':
            if node.CE_Type == 'BusBar':
                # print(i)
                g.create_bus(net, node)
                flag_step(node)
            else:
                pass
        else:
            pass

    # Creating Nodes ------------------------------- #
    for node in grid_data:
        if node.Type == 'CN':
            # print(i)
            g.create_node(net, node)
            flag_step(node)
        else:
            pass

    # Returning grid and grid data ----------------- #
    # (with updated flags) ------------------------- #
    return(net, grid_data)


def find_initial(data):
    end_type = ['Generator', 'Shunt', 'Load']
    for end in data:
        if end.Type == 'CE':
            if end.CE_Type in end_type and end.Processed is False:
                return(end)
            else:
                pass
        else:
            pass


def grid_creator(net, grid_data):
    for node in grid_data:
        if node.Type == 'CE':
            if node.CE_Type == 'Breaker':
                g.create_switch(net, node)
                flag_step(node)
            elif node.CE_Type == 'Shunt':
                g.create_shunt(net, node)
                flag_step(node)
            elif node.CE_Type == 'Transformer':
                g.create_transformer
                flag_step(node)
            elif node.CE_Type == 'Line':
                g.create_line
                flag_step(node)
            elif node.CE_Type == 'Load':
                g.create_load
                flag_step(node)
            elif node.CE_Type == 'Generator':
                g.create_motor
                flag_step(node)
            else:
                print(f'{node} is not created')
        else:
            pass
    return(net, grid_data)


# def next_node(data):
#     type = find_initial(data)
#     for i in data:
#         iType = i.Type
#         if iType == type:
#             return(i)
#         else:
#             pass

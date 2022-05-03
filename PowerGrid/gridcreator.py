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
        if node.Type == 'CN' and 'Busbar' not in node.Name:
            # print(i)
            g.create_node(net, node)
            flag_step(node)
        else:
            pass
    # Returning grid and grid data ----------------- #
    # (with updated flags) ------------------------- #
    return(net, grid_data)


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
                g.create_transformer(net, node)
                flag_step(node)
            elif node.CE_Type == 'Line':
                g.create_line(net, node)
                flag_step(node)
            elif node.CE_Type == 'Load':
                g.create_load(net, node)
                flag_step(node)
            elif node.CE_Type == 'Generator':
                g.create_generator(net, node)
                flag_step(node)
            else:
                # print(f'{node.Name} is not created')
                pass
        else:
            pass
    return(net, grid_data)

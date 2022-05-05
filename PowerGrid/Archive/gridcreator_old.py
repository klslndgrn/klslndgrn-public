import grid


def grid_initializer():
    net = grid.create_grid()
    return(net)


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


def find_next_type(curr, prev=None):
    # INITIAL STEP --------------------------------- #
    if prev is None:
        next_node_type = 'Te'
        return(next_node_type)
    else:
        curr_type = curr.Type
        prev_type = prev.Type

    # IF current is TE and previous is CN ---------- #
    if curr_type == 'Te' and prev_type == 'CN':
        next_node_type = 'CE'

    # IF current is TE and previous is CE ---------- #
    elif curr_type == 'Te' and prev_type == 'CE':
        next_node_type = 'CN'

    # IF current is CN or CE ----------------------- #
    elif curr_type == 'CE' or 'CN':
        next_node_type = 'Te'

    return(next_node_type)


def find_next_ID(curr, prev=None):
    # FIXME:

    next_type = find_next_type(curr, prev)
    print('Next Type =')
    print(next_type)

    if next_type == 'CE':
        next_node_ID = curr.CE
    elif next_type == 'CN':
        next_node_ID = curr.CN
    elif next_type == 'Te':
        if curr.CE_Type == 'Transformer':
            pass
        elif curr.CE_Type == 'Line':
            pass
        elif curr.CE_Type == 'Breaker':
            pass
        else:
            pass

    return(next_node_ID)


def create_pp(node):
    # FIXME:    ADD TRANSFORMER + LINE
    #           ELSE (end...)
    if node.Type == 'CN':
        return(grid.create_node(node))
    elif node.Type == 'CE':
        if node.CE_Type == 'Transformer':
            pass

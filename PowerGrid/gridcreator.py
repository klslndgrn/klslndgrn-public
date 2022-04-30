import grid


def grid_initializer():
    net = grid.create_grid()
    return(net)


def find_initial():
    # Find initial TE that has Processed = False
    # to stand as an initial
    pass


def find_next(curr, cn_data, prev=None):

    curr_type = curr.Type
    prev_type = prev.Type

    if curr_type == 'Te' and prev_type == 'CN':

        next_node = 'CE'
        return(next_node)

    elif curr_type == 'Te' and prev_type == 'CE':
        next_node = 'CN'

        for node in cn_data:
            if node.Processed is False:
                next_node = node
                break
            else:
                pass
        return(next_node)

    elif curr_type == 'CE' or 'CN':
        next_node = 'Te'
        return(next_node)


def flag_step(input):
    input.Processed = True

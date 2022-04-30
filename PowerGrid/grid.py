# Importing PandaPower
import pandapower as pp
# import pandas as pd # import pandas


def create_grid():
    '''
    Grid:
        pp.create_empty_network(...)
    '''
    net = pp.create_empty_network()  # create an empty network
    return(net)


def create_terminal_connections(net, inputclass):
    # FIXME:!
    pass


def create_transformer(net, inputclass):
    '''
    Creating a Transformer (PowerTransformer) with pp.create_transformer(...)
    '''

    hv_bus = inputclass.TermID1
    lv_bus = inputclass.TermID2
    V_hv = inputclass.V_hv
    V_lv = inputclass.V_lv
    S_n = inputclass.S_n
    names = inputclass.Name

    transformer = pp.create_transformer(net, hv_bus, lv_bus, sn_mva=S_n,
                                        vn_hv_kv=V_hv, vn_lv_kv=V_lv,
                                        name=names)
    return(transformer)


def create_bus(net, inputclass):
    '''
    Creating a BusBarSection with pp.create_bus(...)
    '''

    names = inputclass.Name
    basevolt = inputclass.BaseVolt
    types = 'b'

    bus = pp.create_bus(net, vn_kv=basevolt, type=types, name=names)

    return(bus)


def create_node(net, inputclass):
    '''
    BusBarSection
    pp.create_bus(...)
    '''

    names = inputclass.Name
    types = 'n'

    bus = pp.create_bus(net, type=types, name=names)

    return(bus)


def create_line(net, inputclass):
    '''
    Line (ACLineSegment)::
    pp.create_line(...add())
    '''

    from_bus = inputclass.FromID
    to_bus = inputclass.ToID
    length = inputclass.Length
    names = inputclass.name

    line = pp.create_line(net, from_bus, to_bus, length_km=length, name=names)

    return(line)


def create_load(net, inputclass):
    '''
    Load (EnergyConsumer):
    pp.create_load(...)
    '''
    bus_idx = inputclass.ID
    p = inputclass.P_Load
    q = inputclass.Q_Load
    names = inputclass.Name

    load = pp.create_load(net, bus_idx, p_mw=p, q_mvar=q, name=names)

    return(load)


def create_shunt(net, inputclass):
    '''
    Shunt (LinearShuntCompensator):
    pp.create_shunt(net, bus, q_mvar, name=None, index=None)
    '''

    bus_idx = inputclass.ID
    p = inputclass.P_Load
    q = inputclass.Q_Load
    names = inputclass.Name

    shunt = pp.create_shunt(net, bus_idx, p_mw=p, q_mvar=q, name=names)

    return(shunt)


def create_switch(net, inputclass):
    '''
    Switch/Breaker (Breaker):
    pp.create_switch(...)
    '''

    from_bus = pp.get_element_index(net, 'terminal', 'bla')
    to_bus = pp.get_element_index(net, 'node', 'bla')
    state = not inputclass.OpenState
    names = inputclass.Name
    ettype = 'b'
    types = 'CB'

    switch = pp.create_switch(net, from_bus, to_bus, et=ettype,
                              closed=state, type=types,
                              name=names)
    return(switch)


def create_motor(net, inputclass):
    '''
    Motor (SynchronousMachine):
    pp.create_motor(...)
        or
    Generator:
    pp.create_gen(...)
    '''

    bus_idx = pp.get_element_index(net, 'terminal', 'bla')
    p_mw = inputclass.P_Gen
    cos_phi = inputclass.PF

    motor = pp.create_motor(net, bus_idx, p_mw, cos_phi)

    return(motor)

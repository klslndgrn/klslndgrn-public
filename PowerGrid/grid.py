import pandapower as pp
from pandapower.plotting import simple_plot
from pandapower.plotting import create_generic_coordinates


def create_grid():
    '''
    Creating an empty grid using pp.create_empty_network(...).
    '''
    net = pp.create_empty_network()  # create an empty network
    return(net)


def find_element_from_id(net, TermID, all_data):
    '''
    Find PandaPower network ID from TerminalID.
    '''
    type = 'bus'
    for i in all_data:
        if i.ID == TermID:
            cnID = i.CN
            for j in all_data:
                if j.ID == cnID:
                    name = j.Name
                    elementidx = pp.get_element_index(net, type, name)
                    return(elementidx)
                else:
                    pass
        else:
            pass


def create_transformer(net, inputclass, all_data):
    '''
    Creating a Transformer (PowerTransformer) with pp.create_transformer(...).
    '''

    hv_bus_ID = inputclass.TermID1
    lv_bus_ID = inputclass.TermID2

    hv_bus = find_element_from_id(net, hv_bus_ID, all_data)
    lv_bus = find_element_from_id(net, lv_bus_ID, all_data)

    # V_hv = inputclass.V_hv
    # V_lv = inputclass.V_lv
    # S_n = inputclass.S_n

    names = inputclass.Name
    std = '160 MVA 380/110 kV'

    transformer = pp.create_transformer(net, hv_bus, lv_bus, std, name=names)
    # sn_mva=S_n, vn_hv_kv=V_hv, vn_lv_kv=V_lv,
    return(transformer)


def create_transformer_3w(net, inputclass, all_data):
    '''
    Creating a Transformer (PowerTransformer) with pp.create_transformer(...).
    '''

    hv_bus_ID = inputclass.TermID1
    mv_bus_ID = inputclass.TermID2
    lv_bus_ID = inputclass.TermID3

    hv_bus = find_element_from_id(net, hv_bus_ID, all_data)
    mv_bus = find_element_from_id(net, mv_bus_ID, all_data)
    lv_bus = find_element_from_id(net, lv_bus_ID, all_data)

    # V_hv = inputclass.V_hv
    # V_lv = inputclass.V_lv
    # S_n = inputclass.S_n
    names = inputclass.Name
    std = '63/25/38 MVA 110/20/10 kV'

    transformer = pp.create_transformer3w(net, hv_bus, mv_bus, lv_bus, std,
                                          name=names)
    # sn_mva=S_n, vn_hv_kv=V_hv, vn_lv_kv=V_lv,
    return(transformer)


def create_bus(net, inputclass):
    '''
    Creating a BusBarSection with pp.create_bus(...).
    '''

    names = inputclass.Name
    basevolt = inputclass.BaseVolt
    types = 'b'
    In_Service = inputclass.InService

    bus = pp.create_bus(net, vn_kv=basevolt, type=types, name=names,
                        in_service=In_Service)

    return(bus)


def create_node(net, inputclass):
    '''
    Creating BusBarSection but set as NODE with pp.create_bus(...)
    '''

    names = inputclass.Name
    basevolt = inputclass.BaseVolt
    types = 'n'
    In_Service = inputclass.InService

    bus = pp.create_bus(net, vn_kv=basevolt, type=types, name=names,
                        in_service=In_Service)

    return(bus)


def create_line(net, inputclass, all_data):
    '''
    Creating lines (ACLineSegment) with pp.create_line(...)
    '''

    from_bus_ID = inputclass.FromID
    to_bus_ID = inputclass.ToID

    from_bus = find_element_from_id(net, from_bus_ID, all_data)
    to_bus = find_element_from_id(net, to_bus_ID, all_data)

    length = inputclass.Length
    names = inputclass.Name
    std = 'NAYY 4x50 SE'

    line = pp.create_line(net, from_bus, to_bus, length, std, name=names)

    return(line)


def create_load(net, inputclass, all_data):
    '''
    Creating loads (EnergyConsumer) with pp.create_load(...).
    '''

    bus_idx_ID = inputclass.TermID

    bus_idx = find_element_from_id(net, bus_idx_ID, all_data)

    p = inputclass.P_Load
    q = inputclass.Q_Load
    names = inputclass.Name

    load = pp.create_load(net, bus_idx, p_mw=p, q_mvar=q, name=names)

    return(load)


def create_shunt(net, inputclass, all_data):
    '''
    Creating shunts (LinearShuntCompensator) with pp.create_shunt(...).
    '''

    bus_idx_ID = inputclass.TermID

    bus_idx = find_element_from_id(net, bus_idx_ID, all_data)

    p = inputclass.P_Shunt
    q = inputclass.Q_Shunt
    names = inputclass.Name

    shunt = pp.create_shunt(net, bus_idx, p_mw=p, q_mvar=q, name=names)

    return(shunt)


def create_switch(net, inputclass, all_data):
    '''
    Creating switches/breakers with pp.create_switch(...).
    '''

    from_bus_ID = inputclass.FromID
    to_bus_ID = inputclass.ToID

    from_bus = find_element_from_id(net, from_bus_ID, all_data)
    to_bus = find_element_from_id(net, to_bus_ID, all_data)

    state = inputclass.OpenState
    names = inputclass.Name
    ettype = 'b'
    types = 'CB'

    switch = pp.create_switch(net, from_bus, to_bus, et=ettype,
                              closed=state, type=types,
                              name=names)
    return(switch)


def create_motor(net, inputclass, all_data):
    '''
    Creating motor (SynchronousMachine) with pp.create_motor(...).
    '''

    bus_idx_ID = inputclass.TermID

    bus_idx = find_element_from_id(net, bus_idx_ID, all_data)

    p_mw = inputclass.P_Gen
    cos_phi = inputclass.PF
    names = inputclass.Name

    motor = pp.create_motor(net, bus_idx, p_mw, cos_phi, name=names)

    return(motor)


def create_generator(net, inputclass, all_data):
    '''
    Creating generators with pp.create_gen(...).
    '''

    bus_idx_ID = inputclass.TermID

    bus_idx = find_element_from_id(net, bus_idx_ID, all_data)

    cos_phi = inputclass.PF
    sn = inputclass.Sn
    p_gen = int(float(sn)) * int(float(cos_phi))
    names = inputclass.Name

    motor = pp.create_gen(net, bus_idx, p_mw=p_gen, sn_mva=sn, name=names)

    return(motor)


def plot_grid(net):
    '''
    Using SimplePlot to plot generated network.
    '''
    net = create_generic_coordinates(net)
    plot = simple_plot(net,
                       plot_loads=True,
                       load_size=2,
                       plot_gens=True,
                       gen_size=2,
                       plot_line_switches=True,
                       switch_color='green',
                       line_color='red',
                       switch_size=1)
    return(plot)

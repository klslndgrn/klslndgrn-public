import pandapower as pp
from pandapower.plotting import simple_plot
from pandapower.plotting import create_generic_coordinates

# Grid data:
v_nom_kv = 110
line_length_km = 10
std_line_type = '149-AL1/24-ST1A 110.0'
slack_bus = '1'

buses = [[1, 'CLARK', 'Region 1'],
         [2, 'AMHERST', 'Region 1'],
         [3, 'WINLOCK', 'Region 1'],
         [4, 'BOWMAN', 'Region 2'],
         [5, 'TROY', 'Region 2'],
         [6, 'MAPLE', 'Region 2'],
         [7, 'GRAND', 'Region 3'],
         [8, 'WAUTAGA', 'Region 3'],
         [9, 'CROSS', 'Region 3']]

lines = [[1, 4, 'Line 1-4'],
         [4, 5, 'Line 4-5'],
         [5, 6, 'Line 5-6'],
         [6, 3, 'Line 6-3'],
         [6, 7, 'Line 6-7'],
         [7, 8, 'Line 7-8'],
         [8, 2, 'Line 8-2'],
         [8, 9, 'Line 8-9'],
         [9, 4, 'Line 9-4']]

generators = [[1, 0, 0, 'Gen Bus 1'],
              [2, 163, 0, 'Gen Bus 2'],
              [3, 85, 0, 'Gen Bus 3']]

loads = [[5, 90, 30, 'Load Bus 5'],
         [7, 100, 35, 'Load Bus 7'],
         [9, 125, 50, 'Load Bus 9']]


def grid_creator():
    print('\n------ Grid is created: ------\n')
    net = create_grid()
    net = create_buses(net)
    net = create_loads(net)
    net = create_gens(net)
    net = create_lines(net)
    net = create_line_switches(net)
    net = create_slack_bus(net)
    return(net)


def create_grid():
    net = pp.create_empty_network()  # create an empty network
    return(net)


def create_buses(net):
    for j in buses:
        bus_num = j[0]
        bus_name = j[1]
        bus_zone = j[2]
        pp.create_bus(net,
                      index=bus_num,
                      name=bus_name,
                      zone=bus_zone,
                      vn_kv=v_nom_kv,
                      type="b")
    return(net)


def create_loads(net):
    for j in loads:
        bus_idx = j[0]
        Pd = j[1]
        Qd = j[2]
        Name = j[3]
        pp.create_load(net,
                       bus_idx,
                       p_mw=Pd,
                       q_mvar=Qd,
                       name=Name)
    return(net)


def create_gens(net):
    for j in generators:
        bus_idx = j[0]
        Pg = j[1]
        Qg = j[2]
        Name = j[3]
        pp.create_sgen(net,
                       bus_idx,
                       p_mw=Pg,
                       q_mvar=Qg,
                       name=Name)
    return(net)


def create_lines(net):
    for j in lines:
        from_bus = j[0]
        to_bus = j[1]
        Name = j[2]
        pp.create_line(net,
                       from_bus,
                       to_bus,
                       length_km=line_length_km,
                       std_type=std_line_type,
                       name=Name)
    return(net)


def create_line_switches(net):
    ettype = 'l'
    types = 'CB'
    for j in lines:
        bus_idx = j[0]
        line_idx = pp.get_element_index(net, 'line', j[2])
        Name = f'CB {j[2]}'
        pp.create_switch(net,
                         bus_idx,
                         line_idx,
                         et=ettype,
                         type=types,
                         name=Name)
    return(net)


def create_slack_bus(net):
    Name = 'Slack (Ext. Grid)'
    pp.create_ext_grid(net,
                       bus=1,
                       vm_pu=1.0,
                       va_degree=0.0,
                       name=Name)
    return(net)


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
                       plot_sgens=True,
                       sgen_size=2,
                       plot_line_switches=True,
                       switch_color='green',
                       switch_size=2,
                       line_color='red',
                       ext_grid_size=1,
                       ext_grid_color='orange')
    return(plot)


def print_details(net):
    print('------------------------------------------------------------------')
    print('Bus information:')
    print(net.bus)
    print('------------------------------------------------------------------')
    print('Load information:')
    print(net.load)
    print('------------------------------------------------------------------')
    print('Generator information:')
    print(net.gen)
    print(net.sgen)
    print('------------------------------------------------------------------')
    print('Line information:')
    print(net.line)
    print('------------------------------------------------------------------')
    print('Switches information:')
    print(net.switch)
    print('------------------------------------------------------------------')

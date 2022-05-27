import pandas as pd
import numpy as np
import pandapower as pp
# import random
import output
from pandapower.control import ConstControl
from pandapower.timeseries import DFData
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.timeseries.output_writer import OutputWriter


# --------------------------------------------------------------------------- #
# Generating random stuff --------------------------------------------------- #
# --------------------------------------------------------------------------- #

def generate_high(samples):
    values = np.random.normal(1.2, 0.2*0.1, samples)
    return(values)


def generate_low(samples):
    values = np.random.normal(0.8, 0.2*0.1, samples)
    return(values)


def generate_status(samples):
    status = ['False'] * samples
    # status = np.empty(samples)
    # for i in range(samples):
    # status[i] = random.randint(0, 1)
    # status[i] = 'False'
    # print(status)
    return(status)


# --------------------------------------------------------------------------- #
# Generating dataframe ------------------------------------------------------ #
# --------------------------------------------------------------------------- #

def create_dataframe():
    df = pd.DataFrame()
    return(df)


def create_data_source(net, samples, test_sample):
    '''
    Main function to generate a data source from a different dataframes.
    '''
    print('\n------ DataFrames for simulation inputs are created! ------\n')
    # Create DataFrames
    df = create_dataframe()
    df = loads_high_low(net, samples, df)
    df = gens_high_low(net, samples, df)
    df = gens_status(net, samples, df)
    df = lines_status(net, samples, df)

    # Create DataFrames for LEARN and TEST.
    df_learn = df[:-test_sample]
    df_test = df[-test_sample:]

    # Generating a list of event categories
    datanames = df.columns.values.tolist()

    # Create DataSource for LEARN and TEST.
    ds_learn = DFData(df_learn)
    ds_test = DFData(df_test)

    return(ds_learn, ds_test, df, datanames)


def loads_high_low(net, samples, df):
    '''
    Generating a dataset for the LOADS. This dataset includes both high and low
    values compared to the nominal values for both the active (P) and reactive
    (Q) power.
    '''
    # CHANGING ACTIVE POWER FOR THE LOADS
    for nm, p_mw in zip(net.load.name, net.load.p_mw):
        loadname = f'{nm}-P-H'
        df[loadname] = p_mw * generate_high(samples)
    for nm, p_mw in zip(net.load.name, net.load.p_mw):
        loadname = f'{nm}-P-L'
        df[loadname] = p_mw * generate_low(samples)

    # CHANGING REACTIVE POWER FOR THE LOADS
    for nm, q_mvar in zip(net.load.name, net.load.q_mvar):
        loadname = f'{nm}-Q-H'
        df[loadname] = q_mvar * generate_high(samples)
    for nm, q_mvar in zip(net.load.name, net.load.q_mvar):
        loadname = f'{nm}-Q-L'
        df[loadname] = q_mvar * generate_low(samples)
    return(df)


def gens_high_low(net, samples, df):
    '''
    Generating a dataset for the GENERATORS. This dataset includes both high
    and low values compared to the nominal values for only the active (P)
    power.
    If generator has 0 power generation, the power is set to 20 MW with noise.
    '''
    # CHANGING ACTIVE POWER FOR THE GENERATORS
    for nm, p_mw in zip(net.sgen.name, net.sgen.p_mw):
        if p_mw == 0:
            p_mw = 20
            genname = f'{nm}-P-H'
            df[genname] = p_mw * generate_high(samples)
        else:
            genname = f'{nm}-P-H'
            df[genname] = p_mw * generate_high(samples)
    for nm, p_mw in zip(net.sgen.name, net.sgen.p_mw):
        if p_mw == 0:
            p_mw = -20
            genname = f'{nm}-P-L'
            df[genname] = p_mw * generate_low(samples)
        else:
            genname = f'{nm}-P-L'
            df[genname] = p_mw * generate_low(samples)
    return(df)


def gens_status(net, samples, df):
    '''
    Generating a dataset for the STATUS of the GENERATORS, and if they are ON
    or OFF.
    '''
    for nm in net.sgen.name:
        genname = f'{nm}-STATUS'
        df[genname] = generate_status(samples)
    return(df)


def lines_status(net, samples, df):
    '''
    Generating a dataset for whether the LINE CIRCUIT BREAKERS are CLOSED or
    OPEN.
    '''
    for nm in net.switch.name:
        if '-4' in nm:
            pass
        else:
            linename = f'{nm}-CLOSED'
            df[linename] = generate_status(samples)
    return(df)


# --------------------------------------------------------------------------- #
# Generating controllers ---------------------------------------------------- #
# --------------------------------------------------------------------------- #

def create_controller(net, ds, input_name):
    '''
    Creating PandaPower ConstControl(ers) for each event.
    '''
    # print(f'Input name = {input_name}')
    if 'Load' in input_name and '-P-' in input_name:
        net = p_load_controller(net, ds, input_name)
        return(net)
    elif 'Load' in input_name and '-Q-' in input_name:
        net = q_load_controller(net, ds, input_name)
        return(net)
    elif 'Gen' in input_name and '-P-' in input_name:
        net = p_gen_controller(net, ds, input_name)
        return(net)
    elif 'Gen' in input_name and 'STATUS' in input_name:
        net = status_gen_controller(net, ds, input_name)
        return(net)
    elif 'CB Line' in input_name:
        net = line_controller(net, ds, input_name)
        return(net)
    else:
        raise(ValueError('Controller cannot be created'))


def p_load_controller(net, ds, input_name):
    '''
    Modifying ACTIVE POWER for LOADS with "ConstControl".
    '''
    name = input_name[:-4]
    e_idx = pp.get_element_index(net, 'load', name)
    ConstControl(net,
                 element='load',
                 element_index=e_idx,
                 variable='p_mw',
                 data_source=ds,
                 profile_name=input_name)
    return(net)


def q_load_controller(net, ds, input_name):
    '''
    Modifying REACTIVE POWER for LOADS with "ConstControl".
    '''
    name = input_name[:-4]
    e_idx = pp.get_element_index(net, 'load', name)
    ConstControl(net,
                 element='load',
                 element_index=e_idx,
                 variable='q_mvar',
                 data_source=ds,
                 profile_name=input_name)
    return(net)


def p_gen_controller(net, ds, input_name):
    '''
    Modifying ACTIVE POWER for GENERATORS with "ConstControl".
    '''
    name = input_name[:-4]
    e_idx = pp.get_element_index(net, 'sgen', name)
    ConstControl(net,
                 element='sgen',
                 element_index=e_idx,
                 variable='p_mw',
                 data_source=ds,
                 profile_name=input_name)
    return(net)


def status_gen_controller(net, ds, input_name):
    '''
    Modifying the STATUS of "in_service" of the GENERATORS with "ConstControl".
    '''
    name = input_name[:-7]
    e_idx = pp.get_element_index(net, 'sgen', name)
    net.sgen.in_service.at[e_idx] = False

    # ConstControl(net,
    #              element='sgen',
    #              element_index=e_idx,
    #              variable='in_service',
    #              data_source=ds,
    #              profile_name=input_name)

    return(net)


def line_controller(net, ds, input_name):
    '''
    Modifying the STATUS of "CLOSED" of the SWITCHES with "ConstControl".
    '''
    name = input_name[:-7]
    e_idx = pp.get_element_index(net, 'switch', name)
    net.switch.closed.at[e_idx] = False

    # ConstControl(net,
    #              element='switch',
    #              element_index=e_idx,
    #              variable='closed',
    #              data_source=ds,
    #              profile_name=input_name)

    return(net)


# --------------------------------------------------------------------------- #
# Run time series ----------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def output_writer(net, samples):
    output_dir, data_dir_vm, data_dir_va = output.output_writer_directory()
    file_type = '.csv'
    ow = OutputWriter(net,
                      time_steps=samples,
                      output_path=output_dir,
                      output_file_type=file_type,
                      log_variables=list(),
                      csv_separator=',')
    ow.log_variable('res_bus', 'vm_pu')
    ow.log_variable('res_bus', 'va_degree')
    return(ow)


def run_time_series(net, samples):
    time_steps = range(0, samples)
    ts = run_timeseries(net, time_steps)
    return(ts)

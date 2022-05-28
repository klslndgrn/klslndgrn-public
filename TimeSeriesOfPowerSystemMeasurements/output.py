import csv
import data
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
import copy


# --------------------------------------------------------------------------- #
# Generating output --------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def create_output(net, ds, datanames, samples, events):
    create_csv()
    data.output_writer(net, samples)
    cluster_counter = 0
    print('\n------ Output from simulations are recorded: ------\n')
    for dtnm in datanames:
        if cluster_counter > events-1:
            break
        print(f'Algo name = {dtnm}')

        netx = copy.deepcopy(net)
        netx = data.create_controller(netx, ds, dtnm)

        # if 'STATUS' in dtnm:
        #     print(netx.sgen)
        # if 'CLOSED' in dtnm:
        #     print(netx.switch)

        data.run_time_series(netx, samples)

        append_csv_data(dtnm)

        cluster_counter += 1
    return(cluster_counter)


# --------------------------------------------------------------------------- #
# Writing to CSV ------------------------------------------------------------ #
# --------------------------------------------------------------------------- #

def output_writer_directory():
    fdir = 'Files'
    script_dir = Path(__file__).absolute().parent
    dir = script_dir / fdir
    data_dir_vm = dir / 'data_vm.csv'
    data_dir_va = dir / 'data_va.csv'
    # print(odir)
    return(dir, data_dir_vm, data_dir_va)


def create_csv():
    dir, data_dir_vm, data_dir_va = output_writer_directory()

    headers = ['Ts', 'Bus1', 'Bus2', 'Bus3', 'Bus4', 'Bus5', 'Bus6', 'Bus7',
               'Bus8', 'Bus9', 'Event']

    # CREATE EMTPY CSVs
    with open(data_dir_vm, 'w', newline='') as file:
        dw = csv.DictWriter(file,
                            delimiter=',',
                            fieldnames=headers)
        dw.writeheader()
    with open(data_dir_va, 'w', newline='') as file:
        dw = csv.DictWriter(file,
                            delimiter=',',
                            fieldnames=headers)
        dw.writeheader()


def create_event_csv(df):
    dir, data_dir_vm, data_dir_va = output_writer_directory()
    csv_file = dir / 'event_data.csv'
    df.to_csv(csv_file, mode='w', index=True, header=True, sep=',')


def append_csv_data(event_name):
    dir, data_dir_vm, data_dir_va = output_writer_directory()

    vmpu_file = r'res_bus\vm_pu.csv'
    vadegree_file = r'res_bus\va_degree.csv'

    vm_dir = dir / vmpu_file
    va_dir = dir / vadegree_file

    vm = pd.read_csv(vm_dir)
    va = pd.read_csv(va_dir)

    vm['Event'] = event_name
    va['Event'] = event_name

    vm.to_csv(data_dir_vm, mode='a', index=False, header=False, sep=',')
    va.to_csv(data_dir_va, mode='a', index=False, header=False, sep=',')


# --------------------------------------------------------------------------- #
# Creating dataframes from CSV ---------------------------------------------- #
# --------------------------------------------------------------------------- #

def retreive_dataframe():
    dir, data_dir_vm, data_dir_va = output_writer_directory()
    vm = pd.read_csv(data_dir_vm)
    vm.drop(vm.columns[len(vm.columns)-1], axis=1, inplace=True)
    vm.drop(vm.columns[0], axis=1, inplace=True)
    # print(vm)

    va = pd.read_csv(data_dir_va)
    va.drop(va.columns[len(va.columns)-1], axis=1, inplace=True)
    va.drop(va.columns[0], axis=1, inplace=True)
    # print(va)

    vm_norm, va_norm = normalize_dataframe(vm, va)

    events = pd.read_csv(data_dir_vm)
    events.drop(events.columns[0:-1], axis=1, inplace=True)
    # print(events)

    return(vm, va,
           vm_norm, va_norm,
           events)


def normalize_dataframe(vm, va):
    max_vm, max_va, = finding_max_min_values(vm, va)
    vm_norm = vm  # / max_vm
    va_norm = va  # / max_va
    return(vm_norm, va_norm)


def finding_max_min_values(vm, va):
    max_vm = vm.max().max()
    max_va = va.max().max()
    min_va = va.min().min()

    max_va = max([abs(max_va), abs(min_va)])

    return(max_vm, max_va)


# --------------------------------------------------------------------------- #
# Findning coordinate interval for cluster creation ------------------------- #
# --------------------------------------------------------------------------- #

def finding_coordinate_interval(vm_norm, va_norm):
    vm_max = vm_norm.max()
    vm_max_list = vm_max.values.tolist()
    vm_min = vm_norm.min()
    vm_min_list = vm_min.values.tolist()

    va_max = va_norm.max()
    va_max_list = va_max.values.tolist()
    va_min = va_norm.min()
    va_min_list = va_min.values.tolist()

    # print(vm_max_list)
    # print(vm_min_list)
    # print(va_max_list)
    # print(va_min_list)

    return(vm_max_list, vm_min_list,
           va_max_list, va_min_list)


# --------------------------------------------------------------------------- #
# Output to CSV ------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def algo_output_to_csv(input):
    df = create_output_df(input)
    create_output_csv(df)


def create_output_df(input):
    main_header = list(input.keys())
    frames = []
    for clstr_set in main_header:
        df_list = []
        clusters = input[clstr_set]
        for j, clstr in enumerate(clusters):
            df_list2 = []
            d1 = pd.DataFrame({'Vm': clstr.Y_coords})
            d2 = pd.DataFrame({'Va': clstr.X_coords})
            d3 = pd.DataFrame({'DPs': [clstr.DPs]})
            d4 = pd.DataFrame({'Cost': [clstr.Cost]})
            d5 = pd.DataFrame({'Events': clstr.DPtypes})
            df_list2.append(d1)
            df_list2.append(d2)
            df_list2.append(d3)
            df_list2.append(d4)
            df_list2.append(d5)
            # Create DataFrame for each cluster.
            df2 = pd.concat(df_list2, axis=1)
            df_list.append(df2)
        # Creating DataFrame for set of clusters.
        cluster_head = [f'Cluster {i}' for i in range(len(clusters))]
        df_s = pd.concat(df_list, axis=1, keys=cluster_head)
        frames.append(df_s)
    # Creating DataFrame for all set of clusters.
    main_head = [f'Cluster set {i}' for i in range(1, len(main_header)+1)]
    df = pd.concat(frames, axis=1, keys=main_head)
    return(df)


def create_output_csv(df):
    dir, data_dir_vm, data_dir_v = output_writer_directory()
    # XLSX:
    output_file = dir / 'output_data.xlsx'
    if os.path.exists(output_file):
        os.remove(output_file)  # Remove current file if it exists.
    df.to_excel(output_file, index=True, header=True)
    # CSV:
    output_file = dir / 'output_data.csv'
    df.to_csv(output_file, mode='w', index=True, header=True, sep=',')


# --------------------------------------------------------------------------- #
# Scatter plot (2D) --------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def plot_scatter():
    vm, va, vm_norm, va_norm = retreive_dataframe()

    vm = vm_norm
    va = va_norm

    ttl = 'Scatter Plot of Output Results'
    xlbl = 'Voltage Angles (norm)'
    ylbl = 'Voltage Magnitudes (p.u.)'

    # ---- PLOTTING ---- #
    plt.figure('PLOT X', figsize=(7, 5))
    # ---- PLOTS ---- #
    for vm_col, va_col in zip(vm.columns[0:], va.columns[0:]):
        # print(vm_col)
        plt.scatter(va[va_col], vm[vm_col], s=2, label=vm_col)
    # ---- AXIS ---- #
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.5)  # X-AXIS
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.5)  # Y-AXIS
    # ---- LEGEND ---- #
    plt.legend()
    # ---- FORMATTING ---- #
    plt.grid(b=True, which='major', color='k', linestyle='-',
             alpha=0.3)  # MAJOR GRID
    plt.grid(b=True, which='minor', color='k', linestyle='-',
             alpha=0.1)  # MINOR GRID
    plt.minorticks_on()
    # ---- LABELS ---- #
    plt.title(ttl, usetex=True)
    plt.xlabel(xlbl, usetex=True)
    plt.ylabel(ylbl, usetex=True)
    # ---- SHOW PLOT ---- #
    plt.show()

import data
import copy
import csv
import output
import pandas as pd
import kmc_data as md
import kclasses as kc
from pathlib import Path


def create_test_output(net, ds, datanames, samples_test, samples_learn):
    create_csv()
    data.output_writer(net, samples_test)
    print('\n------ Creating test datapoints for classifications. ------\n')
    for dtnm in datanames:
        print(f'Algo name = {dtnm}')

        netx = copy.deepcopy(net)
        netx = data.create_controller(netx, ds, dtnm)

        samples_start = samples_learn
        samples_end = samples_test + samples_learn

        data.run_time_series(netx, samples_end, samples_start)

        append_csv_data(dtnm)


def output_writer_directory():
    fdir = 'Files'
    script_dir = Path(__file__).absolute().parent
    dir = script_dir / fdir
    data_dir_vm = dir / 'test_vm.csv'
    data_dir_va = dir / 'test_va.csv'
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

    va = pd.read_csv(data_dir_va)
    va.drop(va.columns[len(va.columns)-1], axis=1, inplace=True)
    va.drop(va.columns[0], axis=1, inplace=True)

    vm_norm, va_norm = normalize_dataframe(vm, va)

    events = pd.read_csv(data_dir_vm)
    events.drop(events.columns[0:-1], axis=1, inplace=True)

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
# Creating datapoints ------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def create_test_datapoints(vm, va, events):
    md.generate_data_points(vm, va, events)


def datapoint_list():
    dp_list = copy.deepcopy(kc.DataPoint.datapoints)
    output.create_test_datapoints_pickle(dp_list)
    return(dp_list)

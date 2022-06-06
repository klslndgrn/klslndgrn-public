import copy
import random
import output
import kclasses as kc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


# --------------------------------------------------------------------------- #
# Main function to find best clusters --------------------------------------- #
# (Third layer of clustering algo) ------------------------------------------ #
# --------------------------------------------------------------------------- #

def lowest_cost_local_optima(iterations, num, vm_mx, vm_mn, va_mx, va_mn):
    '''
    Generating random clusters and finding their optimal locations in terms of
    the sum of the distance for each datapoint in each cluster. This is
    repeated 100 times to avoid any local optimas.
    '''
    pbar = tqdm(total=iterations)
    for i in range(iterations):
        generate_random_clusters(num, vm_mx, vm_mn, va_mx, va_mn)

        iter, tol2, clust_loop = loop2_prerequisistes()

        while clust_loop is True:
            kc.Cluster.prev_clusters = copy.deepcopy(kc.Cluster.temp_clusters)

            # Find distance between datapoints and every cluster centroid.
            find_distances()
            # pip install tqdm

            # Set datapoint to belong to the closest cluster.
            set_datapoint_to_cluster()

            # Loop through all datapoints and move the cluster centroid to the
            # center location of all connected datapoints.
            move_clusters()

            dist_error = find_distance_diff()

            iter += 1

            if dist_error < tol2:
                clust_loop = False
                find_distances()
                set_datapoint_to_cluster()
            elif iter > 100:
                clust_loop = False
                find_distances()
                set_datapoint_to_cluster()

        # Check total distance (cost) of all connected datapoints for each
        # cluster.
        check_cluster_cost()

        # Add all costs for each cluster to a single sum. If the total cost is
        # lower than the BEST cluster centroids, they replace and become the
        # current best clusters.
        compare_cluster_cost(num, i)

        # print(kc.Cluster.clusters)

        # Updating progress bar
        pbar.update()

    pbar.close()


# --------------------------------------------------------------------------- #
# Below are functions that are used to find clusters ------------------------ #
# --------------------------------------------------------------------------- #

def cluster_cost_sum(num):
    '''
    This function is repeated once when the number of clusters are increased
    and calculates the total cost for the whole set of clusters. This is then
    used to compare the previous scores and let the loop stop when the score is
    stabilized.
    '''
    cost_sum = 0
    for c in kc.Cluster.clusters[num]:
        cost_sum += c.Cost
    kc.ClusterClasses.cluster_scores[num] = cost_sum
    J = kc.ClusterClasses.cluster_scores[num]
    return(J)


def compare_cluster_cost(num, i):
    '''
    If the temporary set of cluster has a total cost lower than the previously
    best set of clusters, the temporary set of cluster replaces the previous
    cluster and becomes the main clusters to be utilized.
    '''
    sum_temp = 0
    sum = 0
    if i == 0:
        kc.Cluster.clusters[num] = kc.Cluster.temp_clusters
    else:
        for clstr_temp, clstr in zip(kc.Cluster.temp_clusters,
                                     kc.Cluster.clusters[num]):
            sum_temp += clstr_temp.Cost
            sum += clstr.Cost
        if sum_temp < sum:
            kc.Cluster.clusters[num] = copy.deepcopy(kc.Cluster.temp_clusters)
        else:
            pass


def check_cluster_cost():
    '''
    Finding the total distance (cost) between the cluster centroid and all the
    datapoints in this cluster.
    '''
    for clstr in kc.Cluster.temp_clusters:
        clstr.Cost = 0
        clstr.DPs = 0
        clstr.DPtypes = []
        for dtpnt in kc.DataPoint.datapoints:
            if clstr.Cnum == dtpnt.Cluster:
                clstr.DPs += 1
                clstr.Cost += dtpnt.MinClustDist
                datapoint_type = dtpnt.Ev_type
                if datapoint_type not in clstr.DPtypes:
                    clstr.DPtypes.append(datapoint_type)
            else:
                pass


def find_distance_diff():
    '''
    Finding the euclidean distance (L2-norm) between the previous cluster
    location and the new.
    This is then used as a measurement of when the cluster is at it's perfect
    center.
    '''
    dist_sum = 0
    for clstr, clstr_prev in zip(kc.Cluster.temp_clusters,
                                 kc.Cluster.prev_clusters):
        dist_sum += clstr.EucDist(clstr_prev)
    return(dist_sum)


def move_clusters():
    '''
    Moving cluster to the center of mass.
    This is done by looping through all datapoints and adding the location of
    each connected datapoint and then dividing by the amount of datapoints that
    are in each cluster.
    '''
    for clstr in kc.Cluster.temp_clusters:
        clstr.DPs = 0
        new_Va = np.empty(int(len(clstr.X_coords)))*0
        new_Vm = np.empty(int(len(clstr.Y_coords)))*0

        for dtpnt in kc.DataPoint.datapoints:
            if dtpnt.Cluster == clstr.Cnum:
                clstr.DPs += 1
                new_Va += np.array(dtpnt.X_coords)
                new_Vm += np.array(dtpnt.Y_coords)
            else:
                pass

        if clstr.DPs == 0:
            # clstr.X_coords unchanged!
            pass
        else:
            new_Va = new_Va / clstr.DPs
            new_Vm = new_Vm / clstr.DPs
            # print(np.linalg.norm(np.array(clstr.X_coords) - new_Va))
            # print(np.linalg.norm(np.array(clstr.X_coords) - new_Va))
            clstr.X_coords = new_Va.tolist()
            clstr.Y_coords = new_Vm.tolist()
            # print('Cluster moved!')


def set_datapoint_to_cluster():
    '''
    Finding the closest cluster for each datapoint and then setting the cluster
    index. Also sets the closest distance as an attribute to each datapoint.
    '''
    for dtpnt in kc.DataPoint.datapoints:
        list = dtpnt.Dist2Clust
        min_value = min(list)
        min_index = list.index(min_value)
        dtpnt.Cluster = min_index
        dtpnt.MinClustDist = min_value


def find_distances():
    '''
    Find distance between datapoints and every cluster centroid.
    '''
    for dtpnt in kc.DataPoint.datapoints:
        # Clearing lists for each datapoint.
        dtpnt.Dist2Clust = []

    # Loop through temporate clusters.
    for clstr in kc.Cluster.temp_clusters:

        # Loop through datapoints
        for dtpnt in kc.DataPoint.datapoints:
            # Calulcating distance from datapoint to cluster.
            dist = clstr.EucDist(dtpnt)

            # Appending this distance to a list of the distances to all
            # temporary clusters.
            dtpnt.Dist2Clust.append(dist)


# --------------------------------------------------------------------------- #
# Generating datapoints and random clusters --------------------------------- #
# --------------------------------------------------------------------------- #

def generate_random_clusters(num, vm_max, vm_min, va_max, va_min):
    '''
    Generate random clusters between inside an interval of the maximum and
    minimum value for each bus and their voltage magnitude and voltage angle.
    '''

    # Clearing list of temporary clusters.
    kc.Cluster.temp_clusters = []
    for i in range(num):
        x_vals = []
        y_vals = []
        for max, min in zip(va_max, va_min):
            x_val = random.uniform(min, max)
            x_vals.append(x_val)
        for max, min in zip(vm_max, vm_min):
            y_val = random.uniform(min, max)
            y_vals.append(y_val)
        # print(x_vals)
        # print(y_vals)

        k = kc.Cluster(x_vals, y_vals, Cnum=i)
        kc.Cluster.temp_clusters.append(k)

        df = pd.DataFrame({'Vm': k.Y_coords,
                           'Va': k.X_coords})

        kc.Cluster.rand_clusters = pd.concat([kc.Cluster.rand_clusters, df])


def generate_data_points(vm_norm, va_norm, events):
    '''
    Generate datapoints from normalized dataframe. Including coordinates,
    datapoint number and what type of event is occuring for each datapoint.
    '''

    # Clearing list of datapoints.
    kc.DataPoint.datapoints = []
    for vm, va, ev in zip(vm_norm.iterrows(),
                          va_norm.iterrows(),
                          events.iterrows()):
        y_vals = vm[1].to_list()
        x_vals = va[1].to_list()
        dp_number = vm[0]
        ev_type = ev[1].to_list()

        x = kc.DataPoint(x_vals, y_vals, DPnum=dp_number, Ev_type=ev_type)
        kc.DataPoint.datapoints.append(x)


def save_data_points():
    dp_list = copy.deepcopy(kc.DataPoint.datapoints)
    output.create_base_datapoints_pickle(dp_list)


# --------------------------------------------------------------------------- #
# Loop prerequisites -------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def loop_prerequisistes():
    '''
    "While-loop prerequisite data.
    '''
    num = 1
    J = 0
    Jprev = 1000
    tol = 1e-2
    loop = True
    enum = 0
    return(num, J, Jprev, tol, loop, enum)


def loop2_prerequisistes():
    '''
    "While-loop prerequisite data.
    '''
    iter = 0
    tol2 = 5e-2
    clust_loop = True
    return(iter, tol2, clust_loop)


# --------------------------------------------------------------------------- #
# Plotting the cluster scores ----------------------------------------------- #
# --------------------------------------------------------------------------- #

def plot_elbow(clstr_scores):
    x = list(range(1, len(clstr_scores)+1))
    y = clstr_scores

    xax = [0, len(clstr_scores)+1]
    yax = [0, 7000]

    ttl = 'Finding optimal number of clusters'
    xlbl = 'K (no. of clusters)'
    ylbl = 'Cost function J'

    # ---- PLOTTING ---- #
    plt.figure('CostPerCluster', figsize=(7, 5))
    # ---- PLOTS ---- #
    plt.plot(x, y, label='Cost per cluster')
    # ---- AXIS ---- #
    plt.xlim(xax)  # XLIM
    plt.ylim(yax)  # YLIM
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


def create_kmc_output(main_cluster):
    string_list = []
    for clstr in main_cluster:
        evlist = clstr.DPtypes
        if not evlist:
            pass
        else:
            evlist = sum(evlist, [])
            string1 = 'Cluster' + str(clstr.Cnum)
            string2 = ', '.join(evlist)
            string3 = string1 + ': ' + string2
            string_list.append(string3)
    string = '\n'.join(string_list)
    return(string)

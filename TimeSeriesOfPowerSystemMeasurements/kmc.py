import output
import kmc_data as md
import kclasses as kc


# --------------------------------------------------------------------------- #
# Main function ------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def k_means_clustering(cluster_count=3, iterations=3):
    '''
    The main k-Means clustering algorithm function. It is possible to change
    the number of iterations of which the randomizer created clusters. 100 is
    set as standard and acts as a prevention for local optimas.
    '''
    print('\n------ k-Means clustering algorithm is started: ------\n')
    # Retreiving ORIGINAL and NORMALIZED dataframes.
    vm, va, vm_norm, va_norm, events = output.retreive_dataframe()

    # Generating normalized datapoints
    md.generate_data_points(vm_norm, va_norm, events)
    md.save_data_points()

    num_dps = kc.DataPoint.datapoints[-1].DPnum + 1
    print(f'------ There are {num_dps} datapoints to be processed. ------\n')

    # Starting k-Means Clustering algorithm.
    cluster_score, cluster_dict, datapoint_list = k_means_algo(vm_norm,
                                                               va_norm,
                                                               iterations,
                                                               cluster_count)

    return(cluster_score, cluster_dict, datapoint_list)


# --------------------------------------------------------------------------- #
# Second layer -------------------------------------------------------------- #
# (Third layer is inside "ad.lowest_cost_local_optima()") ------------------- #
# --------------------------------------------------------------------------- #

def k_means_algo(vm_norm, va_norm, iterations, cluster_count):
    '''
    This function contains all the calculations for the k-Means clustering
    algorithm.
    '''
    # Finding coordinate interval for random centriod creation.
    vm_mx, vm_mn, va_mx, va_mn = output.finding_coordinate_interval(vm_norm,
                                                                    va_norm)

    # First while-loop data.
    num, J, Jprev, tol, loop, enum = md.loop_prerequisistes()

    while loop is True:

        print(f'New loop to create {num} out of {cluster_count+2} clusters \
({iterations} iterations).')
        Jprev = J

        # Finding clusters with lowest cost to avoid local optimas. This
        # involves creating new random clusters 100 times and using the best
        # clusters. (Contains the second "while-loop")
        md.lowest_cost_local_optima(iterations, num,
                                    vm_mx, vm_mn, va_mx, va_mn)

        # Cost function: finding sum of all costs for each cluster centroid
        # (which is the distance from each datapoint to the closest cluster).
        J = md.cluster_cost_sum(num)

        # Increasing the number of clusters by 1 each loop
        num += 1  # Number of clusters

        # Comparing the cost function between the previous set of clusters with
        # the current set of clusters. If the difference is small enough, the
        # loop is stopped.
        # (The elbow is found where the cost difference small.)
        if num == 2:
            error = 100
            # error_prev = 100
        else:
            # error_prev = error
            error = abs(J - Jprev)/Jprev
            print(f'Cost difference between clusters is {error*100:.2f} %')

        if error < tol:  # and error_prev < tol:
            enum += 1

        if enum > 1:
            loop = False
            print('----------------------------------------------------------')
            print('k-Means Clustering algorithm is stopped due to small \
decreases in cost.')
            print('----------------------------------------------------------')
        if num > cluster_count+2:
            loop = False
            print('----------------------------------------------------------')
            print('k-Means Clustering algorithm is stopped due to too many \
clusters.')
            print('----------------------------------------------------------')

    # print(kc.Cluster.clusters)
    # print(kc.ClusterClasses.cluster_scores)

    cluster_score = list(kc.ClusterClasses.cluster_scores.values())
    cluster_dict = kc.Cluster.clusters
    datapoint_list = kc.DataPoint.datapoints
    return(cluster_score, cluster_dict, datapoint_list)


# --------------------------------------------------------------------------- #
# If clustering algo is run from this file ---------------------------------- #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    cluster_score, cluster_dict, datapoint_list = k_means_clustering()
    print(datapoint_list[-1])
    print(cluster_dict)
    print(cluster_score)

    # print(kc.Cluster.rand_clusters)
    # print(kc.Cluster.rand_clusters.max())
    # print(kc.Cluster.rand_clusters.min())

    # output.algo_output_to_csv(kc.Cluster.clusters)
    md.plot_elbow(cluster_score)

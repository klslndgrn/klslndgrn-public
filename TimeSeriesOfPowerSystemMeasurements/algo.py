import output
import algo_data as ad
import kclasses as kc


# --------------------------------------------------------------------------- #
# Main function ------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def k_means_clustering(cluster_count=18, iterations=100):
    '''
    The main k-Means clustering algorithm function. It is possible to change
    the number of iterations of which the randomizer created clusters. 100 is
    set as standard and acts as a prevention for local optimas.
    '''
    # Retreiving ORIGINAL and NORMALIZED dataframes.
    vm, va, vm_norm, va_norm, events = output.retreive_dataframe()

    # Generating normalized datapoints
    ad.generate_data_points(vm_norm, va_norm, events)

    # Starting k-Means Clustering algorithm.
    clstr_score, kc.Cluster.clusters = k_means_algo(vm_norm,
                                                    va_norm,
                                                    iterations,
                                                    cluster_count)

    return(clstr_score, kc.Cluster.clusters)


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
    num, J, Jprev, tol, loop = ad.loop_prerequisistes()

    while loop is True:
        print(f'New loop to create {num} out of {cluster_count+2} clusters \
({iterations} iterations).')
        Jprev = J

        # Finding clusters with lowest cost to avoid local optimas. This
        # involves creating new random clusters 100 times and using the best
        # clusters. (Contains the second "while-loop")
        ad.lowest_cost_local_optima(iterations, num,
                                    vm_mx, vm_mn, va_mx, va_mn)

        # Cost function: finding sum of all costs for each cluster centroid
        # (which is the distance from each datapoint to the closest cluster).
        J = ad.cluster_cost_sum(num)

        # Increasing the number of clusters by 1 each loop
        num += 1  # Number of clusters

        # Comparing the cost function between the previous set of clusters with
        # the current set of clusters. If the difference is small enough, the
        # loop is stopped.
        # (The elbow is found where the cost difference small.)
        error = abs(J - Jprev)
        # print(f'Cost error = {error}')
        if error < tol:
            pass  # replace pass with: loop = False
        if num > cluster_count+2:
            loop = False

    # print(kc.Cluster.clusters)
    # print(kc.ClusterClasses.cluster_scores)

    clstr_score = list(kc.ClusterClasses.cluster_scores.values())
    return(clstr_score, kc.Cluster.clusters)


# --------------------------------------------------------------------------- #
# If clustering algo is run from this file ---------------------------------- #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    clstr_score, kc.Cluster.clusters = k_means_clustering()
    output.algo_output_to_csv(kc.Cluster.clusters)
    ad.plot_elbow(clstr_score)
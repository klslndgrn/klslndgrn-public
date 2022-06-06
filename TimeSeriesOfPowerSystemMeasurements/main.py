import grid
import kmc
import knn
import data
import output
import test_data as test
import kmc_data as md


# --------------------------------------------------------------------------- #
# Main functions ------------------------------------------------------------ #
# --------------------------------------------------------------------------- #

def main_run_all():
    cluster_score = main_run_kmc()
    kNN, Precision = main_run_knn()
    main_cluster = retrieve_clusters()
    return(kNN, Precision, cluster_score, main_cluster)


def main_run_kmc():
    cluster_count = main()
    cluster_score = main_clustering(cluster_count)
    return(cluster_score)


def main_run_knn():
    main_test_data()
    kNN, Precision, datapoints = main_knn_results()
    return(kNN, Precision)


# --------------------------------------------------------------------------- #
# k-Means-Custering functions ----------------------------------------------- #
# --------------------------------------------------------------------------- #

def main():
    # Main DataSource, DataFrame and Samples for time-series simulations.
    net, ds_lrn, smpls_lrn, ds_tst, smpls_tst, dtnms, df_l, df_t = main_data()

    cluster_count = output.create_output(net, ds_lrn, dtnms, smpls_lrn)

    print(f'\n{cluster_count} number of clusters expected.\n')

    return(cluster_count)


def main_data(samples=100, test_fraction=0.2):
    samples_learn = int(100-(100*test_fraction))
    samples_test = int((100*test_fraction))

    net = grid.grid_creator()
    print(net)

    ds_learn, ds_test, df_learn, df_test, datanames = data.create_data_source(
                                                                net,
                                                                samples,
                                                                samples_test)

    output.create_event_csv(df_learn)

    return(net, ds_learn, samples_learn, ds_test, samples_test, datanames,
           df_learn, df_test)


def main_clustering(cluster_count, iterations=100):
    # Starting the k-Means clustering algorithm:
    cluster_score, cluster_dict, datapoint_list = kmc.k_means_clustering(
                                                        cluster_count,
                                                        iterations)

    # Save output to PICKLE file:
    output.create_output_pickle(cluster_dict)
    output.create_score_pickle(cluster_score)

    # Save output to CSV and XLSX (for humans):
    output.algo_output_to_csv(cluster_dict)

    return(cluster_score)


def main_kmc_results():
    main_cluster = retrieve_clusters()
    string = md.create_kmc_output(main_cluster)
    cluster_scores = output.retreive_score_pickle()
    return(string, cluster_scores)


def retrieve_clusters():
    # Pickle to Cluster Dictionary:
    clusters = output.retreive_output_pickle()

    # Retrieving last cluster:
    main_cluster = clusters[list(clusters)[-2]]

    return(main_cluster)


# --------------------------------------------------------------------------- #
# k-Nearest-Neighbor functions ---------------------------------------------- #
# --------------------------------------------------------------------------- #

def main_test_data():
    # Main DataSource, DataFrame and Samples for time-series simulations.
    net, ds_lrn, smpls_lrn, ds_tst, smpls_tst, dtnms, df_l, df_t = main_data()

    # Creating test data:
    test.create_test_output(net, ds_tst, dtnms, smpls_tst, smpls_lrn)

    # Generating test datapoints:
    vm, va, vm_norm, va_norm, events = test.retreive_dataframe()
    md.generate_data_points(vm_norm, va_norm, events)

    # Create Pickle
    test.datapoint_list()


def main_knn_results():
    datapoints, base_datapoints = retrieve_datapoints()
    kNN, Precision, datapoints = knn.k_nearest_neighbor(datapoints,
                                                        base_datapoints)
    return(kNN, Precision, datapoints)


def retrieve_datapoints():
    base_datapoints = output.retreive_base_datapoints_pickle()
    datapoints = output.retreive_test_datapoints_pickle()
    return(datapoints, base_datapoints)


# --------------------------------------------------------------------------- #
# Other functions ----------------------------------------------------------- #
# --------------------------------------------------------------------------- #

def show_grid():
    net = grid.grid_creator()
    grid.plot_grid(net)


# --------------------------------------------------------------------------- #
# Run from "main" ----------------------------------------------------------- #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    '''
    If main.py is ran without GUI, the following will occur.
    '''
    # Run complete program:
    # main_run_all()

    # Run complete kMC:
    main_run_kmc()

    # Run complete kNN:
    # main_run_knn()

    # Show kMC results:
    # main_kmc_results()

    # Run kNN from files:
    # main_knn_results()

    # Print Pandapower network:
    # show_grid()

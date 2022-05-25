import grid
import algo
import data
import output
import algo_data as ad
import kclasses as kc


def main(events, samples=100, samples_test=20):
    samples_learn = 100 - samples_test

    net = grid.grid_creator()
    network = net
    print(net)

    ds_learn, ds_test, df, datanames = data.create_data_source(net,
                                                               samples,
                                                               samples_test)

    output.create_event_csv(df)

    cluster_count = output.create_output(net,
                                         ds_learn,
                                         datanames,
                                         samples_learn,
                                         events)

    print(f'\n{cluster_count} number of clusters expected.\n')

    return(network, ds_test, cluster_count)


def clustering(cluster_count, iterations=100):
    cluster_score, cluster_dict, datapoint_list = algo.k_means_clustering(
                                                        cluster_count,
                                                        iterations)
    return(cluster_score, cluster_dict, datapoint_list)


def main_test(net, ds_test):
    pass


if __name__ == "__main__":
    '''
    If main.py is ran without GUI, the following will occur.
    '''
    # Change "events" to change the number of events implemented in the grid
    network, ds_test, cluster_count = main(events=25)

    # Print Pandapower network:
    # grid.plot_grid(network)

    # Starting k-Means clustering:
    cluster_score, cluster_dict, datapoint_list = clustering(cluster_count)

    # Printing results:
    print(cluster_dict)
    print(cluster_score)
    print(datapoint_list[-1])

    # print(kc.Cluster.rand_clusters)
    print(f'Max Vm/Va: {kc.Cluster.rand_clusters.max()}')
    print(f'Max Vm/Va: {kc.Cluster.rand_clusters.min()}')

    # Output to CSV and XLSX:
    output.algo_output_to_csv(cluster_dict)

    # Printing cost-functions:
    ad.plot_elbow(cluster_score)

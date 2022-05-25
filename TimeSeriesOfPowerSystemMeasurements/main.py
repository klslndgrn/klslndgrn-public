import grid
import algo
import data
import output


def main(samples=100, samples_test=20):
    samples_learn = 100 - samples_test

    net = grid.grid_creator()
    network = net
    print(net)
    # print(net.sgen)

    ds_learn, ds_test, df, datanames = data.create_data_source(net,
                                                               samples,
                                                               samples_test)

    output.create_event_csv(df)

    cluster_count = output.create_output(net,
                                         ds_learn,
                                         datanames,
                                         samples_learn)

    print(f'{cluster_count} number of clusters expected.')

    return(network, ds_test, cluster_count)


def clustering(cluster_count, iterations):
    clstr_score, output_dict = algo.k_means_clustering(cluster_count,
                                                       iterations)
    return(clstr_score, output_dict)


def main_test(net, ds_test):
    pass


if __name__ == "__main__":
    '''
    If main.py is ran without GUI, the following will occur.
    '''
    network, ds_test, cluster_count = main()
    clstr_score, output_dict = clustering(cluster_count)
    # grid.plot_grid(network)

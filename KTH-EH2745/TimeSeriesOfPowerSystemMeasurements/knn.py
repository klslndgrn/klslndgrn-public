import numpy as np


def k_nearest_neighbor(datapoints, base_datapoints):

    score_dict = {}
    num_dps = len(datapoints)
    num_bdps = len(base_datapoints)

    print(f'\n------ There are {num_dps} datapoints to be processed\
based on {num_bdps} nearest neighbors. ------\n')

    datapoints = find_distances(datapoints, base_datapoints)
    datapoints = datapoint_nearest_neighbors(datapoints)
    k_start = find_starting_k(base_datapoints)
    k = k_start

    P, tol, loop = loop_prerequisities()

    while loop is True:
        Pprev = P

        datapoints = find_classifications(k, datapoints, base_datapoints)
        datapoints = set_classification(datapoints)
        precision = find_precision(datapoints, num_dps)

        P = precision

        score_dict[k] = P
        loop = check_loop(P, Pprev, k, tol, loop)
        k -= 1

    # print(score_dict)
    kNN = find_best_k(score_dict, k_start)
    Precision = score_dict[kNN]

    return(kNN, Precision, datapoints)


def datapoint_nearest_neighbors(dps):
    '''
    Finding the...
    '''
    for dtpnt in dps:
        lst = dtpnt.Dist2Clust
        dct = dict(zip(range(len(lst)), lst))
        dtpnt.ClassDict = dict(sorted(dct.items(), key=lambda item: item[1]))
    return(dps)


def find_distances(dps, base_dps):
    '''
    Find distance between datapoints and every cluster centroid.
    '''
    for dtpnt in dps:
        # Clearing lists for each datapoint.
        dtpnt.Dist2Clust = []

    # Loop through temporate clusters.
    for dtpnt in dps:

        # Loop through datapoints
        for base_dtpnt in base_dps:
            # Calulcating distance from datapoint to cluster.
            dist = dtpnt.EucDist(base_dtpnt)

            # Appending this distance to a list of the distances to all
            # temporary clusters.
            dtpnt.Dist2Clust.append(dist)
    return(dps)


def find_starting_k(base_datapoints):
    num = len(base_datapoints)
    k = np.sqrt(num)
    k = round(k)
    return(k)


def find_classifications(k, datapoints, base_datapoints):
    # Loop through all datapoints to be classified.
    for dp in datapoints:
        dp.ClassList = []
        IDlist = list(dp.ClassDict.keys())
        IDlist = IDlist[:k]

        # Loop to find "k nearest neighbors"
        for base_dp in base_datapoints:
            baseID = base_dp.DPnum
            baseTYPE = base_dp.Ev_type
            if baseID in IDlist:
                dp.ClassList.append(baseTYPE)

    return(datapoints)


def set_classification(datapoints):
    for dp in datapoints:
        classlist = dp.ClassList
        dp_type = most_frequent(classlist)
        dp.Classification = dp_type
    return(datapoints)


def most_frequent(List):
    counter = 0
    id = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            id = i

    return(id)


def find_precision(datapoints, num_dps):
    precision = 0
    for dp in datapoints:
        if dp.Classification == dp.Ev_type:
            precision += 1
    precision = precision / num_dps
    return(precision)


def check_loop(P, Pprev, k, tol, loop):
    Pdiff = abs(P - Pprev)/Pprev
    if k == 1:
        loop = False
    if Pdiff < tol:
        pass
    return(loop)


def loop_prerequisities():
    '''
    "While-loop prerequisite data.
    '''
    P = 1e-3
    tol = 1e-2
    loop = True
    return(P, tol, loop)


def find_best_k(score_dict, k_start):
    score_list = list(score_dict.values())

    max_value = max(score_list)
    max_index = score_list.index(max_value)

    kNN = k_start - max_index

    return(kNN)

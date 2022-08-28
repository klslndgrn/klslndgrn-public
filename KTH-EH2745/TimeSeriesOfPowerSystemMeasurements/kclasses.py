import numpy as np
import pandas as pd


class ClusterClasses():
    # Dictionary of set of Clusters depending on how many clusters there are:
    cluster_scores = {}

    def __init__(self, X_coordinates, Y_coordinates, Type=None):

        self.X_coords = X_coordinates
        self.Y_coords = Y_coordinates
        self.Type = Type

    def EucDist(self, other):
        x1 = self.X_coords
        y1 = self.Y_coords

        vec1 = [None]*(len(x1)+len(y1))
        vec1[::2] = x1
        vec1[1::2] = y1

        x2 = other.X_coords
        y2 = other.Y_coords

        vec2 = [None]*(len(x2)+len(y2))
        vec2[::2] = x2
        vec2[1::2] = y2

        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dist = np.linalg.norm(vec1-vec2)
        return(dist)


class Cluster(ClusterClasses):
    # List of all clusters:
    clusters = {}
    temp_clusters = []
    prev_clusters = []
    rand_clusters = pd.DataFrame()

    cost_sum = 0

    def __init__(self, X_coordinates, Y_coordinates, Type='Cluster',
                 Cnum=None,
                 Cost=0,
                 DPs=0):
        super().__init__(X_coordinates, Y_coordinates, Type)

        self.Cnum = Cnum
        self.Cost = Cost
        self.DPs = DPs
        self.DPtypes = []

    # def __repr__(self):
    #     return(f'\n{self.Type} {self.Cnum}:\
    #     \nVa={self.X_coords}\
    #     \nVm={self.Y_coords}\
    #     \nCost={self.Cost}\
    #     \nDataPoints={self.DPs}\
    #         \n')

    def __repr__(self):
        return(f'\n{self.Type} {self.Cnum}:\
        \nVm={self.Y_coords}\
        \nVa={self.X_coords}\
        \nCost={self.Cost}\
        \nDataPoints={self.DPs}\
        \nEvents={self.DPtypes}\
        \n')


class DataPoint(ClusterClasses):
    # List of all DataPoints:
    # datapoints = {}
    datapoints = []

    def __init__(self, X_coordinates, Y_coordinates, Type='DataPoint',
                 DPnum=None,
                 Ev_type=None,
                 Cluster=None,
                 NumClust=None,
                 MinClustDist=None,
                 Classification=None):
        super().__init__(X_coordinates, Y_coordinates, Type)

        self.DPnum = DPnum
        self.Ev_type = Ev_type

        self.Dist2Clust = []

        self.Cluster = Cluster
        self.NumClust = NumClust
        self.MinClustDist = MinClustDist

        self.Classification = Classification
        self.ClassDict = {}
        self.ClassList = []

    def __repr__(self):
        return(f'\n{self.Type} {self.DPnum}:\
        \nVm={self.Y_coords}\
        \nVa={self.X_coords}\
        \nClosestCluster={self.Cluster}\
        \nEventType={self.Ev_type}\
        \nClassification={self.Classification}\
        \n')
        # \nDist2Clust={self.Dist2Clust}\

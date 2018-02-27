import numpy as np


class Graph(object):
    def __init__(self, matrix):
        self.n = len(matrix[0])
        # self.vertex = []
        self.adj = matrix

    def dijkstra(self, start, end):
        d = [np.inf for i in range(self.n)]
        prev = [None for i in range(self.n)]
        d[start] = 0
        S = set([])
        Q = set([i for i in range(self.n)])
        while len(Q) != 0:
            tmp_min = None
            for v in Q:
                if tmp_min is None or np.less(d[v], d[tmp_min]):
                    tmp_min = v
            v = tmp_min
            S.add(v)
            Q.remove(v)
            for u in range(len(self.adj[v])):
                if self.adj[v][u] is not None:
                    if np.less(d[v] + self.adj[v][u], d[u]):
                        d[u] = d[v] + self.adj[v][u]
                        prev[u] = v
        path = []
        v = end
        while v is not None:
            path = [v] + path
            v = prev[v]

        return path

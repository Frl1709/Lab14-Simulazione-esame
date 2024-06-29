import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._listChromosome = []
        self._listGenes = []
        self._bestPath = []
        self._bestCost = 0

        self.loadChromosome()
        self.loadGenes()

    def getBestPath(self, soglia):
        self._bestPath = []
        self._bestCost = 0

        for node in self._graph.nodes:
            parziale = [node]
            visitati = []
            lunghezza = 0
            self._ricorsione(parziale, visitati, lunghezza, soglia)

        return self._bestPath, self._bestCost

    def _ricorsione(self, parziale, visitati, lunghezza, soglia):
        if lunghezza >= self._bestCost:
            self._bestCost = lunghezza
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph[parziale[-1]]:
            if (self._graph[parziale[-1]], n) not in visitati and self._graph[parziale[-1]][n]['weight'] > soglia:
                parziale.append(n)
                visitati.append((self._graph[parziale[-2]], n))
                lunghezza += self._graph[parziale[-2]][n]['weight']
                self._ricorsione(parziale, visitati, lunghezza, soglia)
                lunghezza -= self._graph[parziale[-2]][n]['weight']
                visitati.pop()
                parziale.pop()

    def getPesoArco(self, v0, v1):
        return self._graph[v0][v1]['weight']

    def contaArchi(self, soglia):
        archiMinori = 0
        archiMaggiori = 0
        for edge, weight in nx.get_edge_attributes(self._graph, 'weight').items():
            if weight < soglia:
                archiMinori += 1
            if weight > soglia:
                archiMaggiori += 1

        return archiMinori, archiMaggiori

    def loadGenes(self):
        self._listGenes = DAO.getGenes()

    def loadChromosome(self):
        self._listChromosome = DAO.getNodes()

    def buildGraph(self):
        self._graph.clear()
        self._graph.add_nodes_from(DAO.getNodes())

        edge = []
        for r in DAO.getEdges():
            if (r[2], r[3]) not in edge:
                edge.append((r[2], r[3]))
                self._graph.add_edge(r[2], r[3], weight=float(r[4]))
            else:
                self._graph[r[2]][r[3]]['weight'] += float(r[4])

    def getGraphSize(self):
        return len(self._graph.nodes()), len(self._graph.edges())

    def maxMinWeight(self):
        maxWeight = 0
        minWeight = float('inf')
        for edge, weight in nx.get_edge_attributes(self._graph, 'weight').items():
            if weight > maxWeight:
                maxWeight = weight
            if weight < minWeight:
                minWeight = weight

        return maxWeight, minWeight

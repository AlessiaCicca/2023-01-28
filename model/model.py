import copy

import networkx as nx
from geopy.distance import geodesic
from database.DAO import DAO


class Model:
    def __init__(self):
        self.provider=DAO.getProvider()
        self.grafo = nx.Graph()
        self._solBest = []
        self._costBest = 0
        self.lista=[]

    def creaGrafo(self, distanza, prov):
        #self.addEdges(forma, anno)
        self.nodi = DAO.getNodi(prov)
        self.grafo.add_nodes_from(self.nodi)
        self._idMap = {}

        for v in self.nodi:
            self._idMap[v.Location] = v
        self.addEdges(distanza)
        return self.grafo

    def addEdges(self, distanza):
         self.grafo.clear_edges()
         for nodo1 in self.grafo:
             for nodo2 in self.grafo:
                 if nodo1!=nodo2 and self.grafo.has_edge(nodo1, nodo2) == False:
                    posizione1=(nodo1.Latitude, nodo1.Longitude)
                    posizione2 = (nodo2.Latitude, nodo2.Longitude)
                    distanzaCalcolata=geodesic(posizione1,posizione2).kilometers
                    if distanzaCalcolata<=distanza:
                        self.grafo.add_edge(nodo1, nodo2, weight=abs(distanzaCalcolata))

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def analisi(self):
        dizio={}
        lista=[]
        for nodo in self.grafo.nodes:
            dizio[nodo.Location]=len(list(self.grafo.neighbors(nodo)))
        dizioOrder=list(sorted(dizio.items(), key=lambda items:items[1], reverse=True))
        pesoMassimo=dizioOrder[0][1]
        for chiave in dizio.keys():
            if dizio[chiave]==pesoMassimo:
                lista.append(self._idMap[chiave])
        self.lista=lista
        return lista,pesoMassimo

    def getBestPath(self, vf, string):
        self._solBest = []
        self._costBest = 0
        parziale = []
        stringa=string.lower()
        for v in self.lista:
            print(stringa)
            print(v)
            if stringa not in v.Location.lower():
                parziale.append(v)
                self.ricorsione(parziale,vf,stringa)
                parziale.pop()
        return self._solBest, self._costBest

    def ricorsione(self, parziale,vf,stringa):
        # Controllo se parziale è una sol valida, ed in caso se è migliore del best
        if parziale[-1].Location.__eq__(vf):
            if len(parziale) > self._costBest:
                self._costBest = len(parziale)
                self._solBest = copy.deepcopy(parziale)
        #nodo=self._idMap[parziale[-1]]
        for v in self.grafo.neighbors(parziale[-1]):
            if v not in parziale:
                if stringa not in v.Location.lower():
                    parziale.append(v)
                    self.ricorsione(parziale, vf,stringa)
                    parziale.pop()


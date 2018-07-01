#pylint: disable=W0614
import sys
import csv
from gistfile1 import *
from math import radians, sin, cos, atan2, sqrt
import heapq

class OpenStreetGabs():
    def __init__(self):
        self.inicial = '1942043262'
        self.final = '5451630914'
        self.__heapq = []
        self.G = read_osm('map.osm')
  
    def getInicial(self):
        return self.inicial
    
    def getFinal(self):
        return self.final

    def getCoord(self, idt):
        for nodo in self.G.nodes():
            if idt == self.G.nodes[nodo]['data'].id:
                lat = self.G.nodes[nodo]['data'].lat
                lon = self.G.nodes[nodo]['data'].lon
        return lat, lon

    def createNodesDatabase(self):
        nodes = []
        node = {
            'id': [],
            'lat': [],
            'lon': []
        }
        for nodo in self.G.nodes():
            node['id'].append(self.G.nodes[nodo]['data'].id) 
            node['lat'].append(self.G.nodes[nodo]['data'].lat)
            node['lon'].append(self.G.nodes[nodo]['data'].lon)
            nodes.append(node)
        return nodes
    
    def getAdjPoints(self):
        lat = []
        lon = []
        nodes = self.createNodesDatabase()
        adj = self.G.__getitem__(nodes[0]['id'][0])
        lat.append(nodes[0]['lat'][0])
        lon.append(nodes[0]['lon'][0])
        for n_adj in adj:
            lat.append(self.G.nodes[n_adj]['data'].lat)
            lon.append(self.G.nodes[n_adj]['data'].lon)
        return(zip(lat, lon))

    def createListOfAllPoints(self):
        lat = []
        lon = []
        for nodo in self.G.nodes():
            lat.append(self.G.nodes[nodo]['data'].lat)
            lon.append(self.G.nodes[nodo]['data'].lon)
        return (zip(lat, lon))

    def createZipPath(self):
        lat = []
        lon = []
        caminho = self.dijkstra()
        for idt in caminho:
            for nodo in self.G.nodes():
                if idt == self.G.nodes[nodo]['data'].id:
                    lat.append(self.G.nodes[nodo]['data'].lat)
                    lon.append(self.G.nodes[nodo]['data'].lon)
        return zip(lat, lon)

    def coordDistances(self, lat1, lon1, lat2, lon2):
        R = 6371e3 #raio da  terra  
        a = sin(radians(lat2 - lat1) / 2) * sin(radians(lat2 - lat1) / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(radians(lon2 - lon1) / 2) * sin(radians(lon2 - lon1) / 2)
        dist = R * 2 * atan2(sqrt(a), sqrt(1 - a))    
        return dist/1000    

    def dijkstra(self):
        # Fontes: 
        # https://gist.github.com/kachayev/5990802
        # https://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python 
        # https://github.com/luanlorenzo/GPS_OSM 
        # https://www.cse.ust.hk/~dekai/271/notes/L10/L10.pdf
        self.__heapq.append((0, self.getInicial()))
        heapq.heapify(self.__heapq)
        origin, costCounter = {}, {}
        costCounter[self.getInicial()] = 0
        origin[self.getInicial()] = None
        while not (len(self.__heapq) == 0):    
            current = heapq.heappop(self.__heapq)[1]
            if current == self.getFinal():
                break
            for neighbor in self.G.neighbors(current):
                new_cost = costCounter[current] + float(self.coordDistances(self.G.nodes[current]['data'].lat, self.G.nodes[current]['data'].lon, self.G.nodes[neighbor]['data'].lat, self.G.nodes[neighbor]['data'].lon))
                if neighbor not in costCounter or new_cost < costCounter[neighbor]:
                    costCounter[neighbor] = new_cost
                    self.__heapq.append((new_cost, neighbor))
                    heapq.heapify(self.__heapq)
                    origin[neighbor] = current
        current = self.getFinal()
        path = [current]
        while current != self.getInicial():
            current = origin[current]
            path.append(current)
        path.reverse()
        return path


import xml.etree.ElementTree as ET
from classes import *
import geopy.distance


class DataLoader:
    def __init__(self, path: str):
        tree = ET.parse(path)
        root = tree.getroot()

        nodesCoordsDict = {}
        nodes = []
        for node in root[0][0]:
            name = node.attrib["id"]
            x = float(node[0][0].text)
            y = float(node[0][1].text)
            nodesCoordsDict[name] = (y, x)
            nodes.append(Node(name, x, y))

        paths = []
        for path in root[0][1]:
            source = path[0].text
            target = path[1].text
            source_coords = nodesCoordsDict[source]
            target_coords = nodesCoordsDict[target]
            distance = geopy.distance.geodesic(source_coords, target_coords).km
            paths.append(Path(source, target, distance))

        demands = []
        for demand in root[1]:
            source = demand[0].text
            target = demand[1].text
            value = float(demand[2].text)
            demands.append(Demand(source, target, value))

        self._nodes = nodes
        self._paths = paths
        self._demands = demands

    def get_nodes(self):
        return self._nodes

    def get_paths(self):
        return self._paths

    def get_demands(self):
        return self._demands


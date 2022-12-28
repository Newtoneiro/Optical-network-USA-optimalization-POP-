import xml.etree.ElementTree as ET
from classes import Link, Demand


class DataLoader:
    def __init__(self, path: str):
        tree = ET.parse(path)
        root = tree.getroot()

        nodes = [node.attrib["id"] for node in root[0][0]]

        links = []
        for link in root[0][1]:
            source = link[0].text
            target = link[1].text
            links.append(Link(source, target))

        demands = []
        for demand in root[1]:
            source = demand[0].text
            target = demand[1].text
            value = float(demand[2].text)
            demands.append(Demand(source, target, value))\

        self._nodes = nodes
        self._links = links
        self._demands = demands

    def get_nodes(self):
        return self._nodes

    def get_links(self):
        return self._links

    def get_demands(self):
        return self._demands

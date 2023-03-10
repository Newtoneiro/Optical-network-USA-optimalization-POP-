from classes import Node, Path, Demand
import xml.etree.ElementTree as ET
import geopy.distance


class DataLoader:
    """
    This is handle class for getting the data from datafile and
    transforming it into usefull format
    """

    def __init__(self, path: str) -> None:
        tree = ET.parse(path)
        root = tree.getroot()

        # Get individual cities - Nodes
        nodes_coords_dict = {}
        nodes = []
        for node in root[0][0]:
            name = node.attrib["id"]
            x = float(node[0][0].text)
            y = float(node[0][1].text)
            nodes_coords_dict[name] = (y, x)
            nodes.append(Node(name, x, y))

        # Get connection between cities - Paths
        paths = []
        for path in root[0][1]:
            source = path[0].text
            target = path[1].text
            source_coords = nodes_coords_dict[source]
            target_coords = nodes_coords_dict[target]
            # Calculate distance between cities
            distance = geopy.distance.geodesic(source_coords, target_coords).km
            paths.append(Path(source, target, distance))

        # Get demands between cities - Demands
        demands = []
        for demand in root[1]:
            source = demand[0].text
            target = demand[1].text
            value = demand[2].text
            value = float(value)
            demands.append(Demand(source, target, value))

        self._nodes = nodes
        self._paths = paths
        self._demands = demands

    def get_nodes(self) -> list[Node]:
        """
        Nodes getter
        """

        return self._nodes

    def get_paths(self) -> list[Path]:
        """
        Paths getter
        """

        return self._paths

    def get_demands(self) -> list[Demand]:
        """
        Demands getter
        """

        return self._demands

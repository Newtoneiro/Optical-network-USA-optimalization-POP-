import xml.etree.ElementTree as ET


class Link:
    def __init__(self, source: str, target: str) -> None:
        self.source = source
        self.target = target


class Demand:
    def __init__(self, source: str, target: str, value: float) -> None:
        self.source = source
        self.target = target
        self.value = value


if __name__ == "__main__":
    tree = ET.parse("janos-us-ca.xml")
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
        demands.append(Demand(source, target, value))

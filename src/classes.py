MAX_PATH_CAPACITY = 96

# tranponders costs
COST_100G = 2
COST_200G = 3
COST_400G = 5


class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.name} [x: {self.x}, y: {self.y}]"


class Path:
    def __init__(self, source: str, target: str, distance: float) -> None:
        self._source = source
        self._target = target
        self._distance = distance
        self._capacity = 0

    def __str__(self) -> str:
        return f"{self._source} - {self._target} : {self._distance}"


class Demand:
    def __init__(self, source: str, target: str, value: float) -> None:
        self.source = source
        self.target = target
        self.value = value
        self.id = f"{source}-{target}"

    def __str__(self) -> str:
        return f"{self.source} - {self.target} - {self.value}"


class Connection:
    '''path + used transponders'''

    def __init__(self, path: list[Node], tranponders: list[int]):
        self.path = path
        self.transponders = tranponders

    def __str__(self) -> str:
        return f"{self.path} - {self.transponders}"

    def getCost(self) -> int:
        return (
            self.transponders[0] * COST_100G +
            self.transponders[1] * COST_200G +
            self.transponders[2] * COST_400G
        )


class Individual:
    '''
    Single solution defined as dictionary of lists of
    "Connection" class objects
    '''

    content = {}

    def __init__(self):
        pass

    def appendDemand(self, demand_id: str, connections: list[Connection]):
        self.content[demand_id] = []
        for connection in connections:
            self.content[demand_id].append(connection)

    def getCost(self) -> int:
        return sum(
            [
                connection.getCost()
                for connection in self.content.values()
            ]
        )

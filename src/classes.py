from config.config import *

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
    
    def getAvailableCapacity(self):
        return MAX_PATH_CAPACITY - self._capacity

    def increaseLambdas(self, lambdas):
        self._capacity += lambdas

    def matchesSourceAndTarget(self, source, target):
        return self._source == source and self._target == target
    
    def hasAvailableSpace(self, demandedLambdas):
        return self._capacity + demandedLambdas <= MAX_PATH_CAPACITY

    def __str__(self) -> str:
        return f"{self._source} - {self._target} : {self._distance}"


class Demand:
    def __init__(self, source: str, target: str, value: float) -> None:
        self.id = f"{source}-{target}"
        self.source = source
        self.target = target
        self.value = value

    def __str__(self) -> str:
        return f"{self.source} - {self.target} - {self.value}"


class DemandFulfillment:
    '''path + used transponders'''

    def __init__(self, genome):
        self.genome = genome

    def __str__(self) -> str:
        return f"{self.genome}"

    # def getCost(self) -> int:
    #     return (
    #         self.transponders["100"] * COST_100G +
    #         self.transponders["200"] * COST_200G +
    #         self.transponders["400"] * COST_400G
    #     )


class Individual:
    '''
    Single solution defined as dictionary of lists of
    "Connection" class objects
    '''

    content = {}

    def __init__(self):
        pass

    def appendDemand(self, demand_id: str, connections: list[DemandFulfillment]):
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

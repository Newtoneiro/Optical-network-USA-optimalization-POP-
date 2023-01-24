from config.config import (
    MAX_PATH_CAPACITY,
    TRANSPONDERS,
    TRANSPONDERS_COSTS
)


class Node:
    def __init__(self, name, x, y) -> None:
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

    def get_available_capacity(self) -> int:
        return MAX_PATH_CAPACITY - self._capacity

    def increase_lambdas(self, lambdas) -> None:
        self._capacity += lambdas

    def matches_source_and_target(self, source, target) -> bool:
        return self._source == source and self._target == target

    def has_available_space(self, demandedLambdas) -> bool:
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


class Individual:
    """
    Single solution defined as dictionary of lists of
    "Connection" class objects
    """
    def __init__(self) -> None:
        self.content = {}

    def sum_transponders(self, demand_id: str) -> dict:
        demand_transponders = {
            transponder: 0
            for transponder
            in TRANSPONDERS
        }

        demand_ff = self.content[demand_id]

        for connection in demand_ff:
            connection_transponders = connection[1]
            for transponder in connection_transponders:
                number = connection_transponders[transponder]
                demand_transponders[transponder] += number
        return demand_transponders

    def append_demand(self, demand_id: str, genome: list) -> None:
        self.content[demand_id] = genome

    def get_cost(self) -> int:
        cost_transponders = 0
        for demand in self.content.values():
            for connection in demand:
                transponders = connection[1]

                cost_transponders += sum(
                    [
                        transponders[type] * cost
                        for type, cost
                        in zip(TRANSPONDERS, TRANSPONDERS_COSTS.values())
                    ]
                )

        return cost_transponders

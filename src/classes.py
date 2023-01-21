from config.config import (
    MAX_PATH_CAPACITY,
    TRANSPONDERS,
    TRANSPONDERS_COSTS,
    COST_LAMBDA
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

    def append_demand(self, demand_id: str, genome: list) -> None:
        self.content[demand_id] = genome

    def get_cost(self) -> int:
        cost_transponders = 0
        cost_lambdas = 0
        for demand in self.content.values():
            for connection in demand:
                transponders = connection[1]

                cost_transponders += sum(
                    [
                        transponders[transponder] * cost
                        for transponder, cost
                        in zip(TRANSPONDERS, TRANSPONDERS_COSTS)
                    ]
                )

                for value in transponders.values():
                    cost_lambdas += value

        cost_lambdas *= COST_LAMBDA

        return cost_transponders + cost_lambdas

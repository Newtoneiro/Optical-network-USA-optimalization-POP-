from config.config import MAX_PATH_CAPACITY


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

    def __init__(self):
        self.content = {}

    def append_demand(self, demand_id: str, genome: list):
        self.content[demand_id] = genome

    def get_cost(self) -> int:
        return sum(
            [
                connection.get_cost()
                for connection in self.content.values()
            ]
        )

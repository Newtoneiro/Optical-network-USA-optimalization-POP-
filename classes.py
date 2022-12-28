class Link:
    def __init__(self, source: str, target: str) -> None:
        self.source = source
        self.target = target


class Demand:
    def __init__(self, source: str, target: str, value: float) -> None:
        self.source = source
        self.target = target
        self.value = value

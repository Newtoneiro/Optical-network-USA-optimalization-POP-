class Link:
    def __init__(self, source: str, target: str) -> None:
        self.source = source
        self.target = target

    def __str__(self) -> str:
        return f"{self.source} - {self.target}"


class Demand:
    def __init__(self, source: str, target: str, value: float) -> None:
        self.source = source
        self.target = target
        self.value = value

    def __str__(self) -> str:
        return f"{self.source} - {self.target} - {self.value}"

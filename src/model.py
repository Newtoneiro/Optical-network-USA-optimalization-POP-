import numpy as np
from classes import Node, Path


class Model:
    """
    Class responsible for representing the actual physical model of the
    problem, the citieswith their connections and demands. It helps to
    create some sort of abstraction used to simplify perations such as
    finding the shortest path and increasing path"s lambdas demand.
    """

    def __init__(
        self, nodes: list[Node], paths: list[Path]
    ) -> None:
        self._nodes = nodes
        self._paths = paths

    def findAllPaths(self, start):
        """
        Using Dijkstra algorithm it creates the output
        table for Dijkstra algorithm containing all the
        available paths with some lambda capacity left.
        """

        # Prepare visited and unvisited node lists
        visited = []
        unvisited = self._nodes.copy()
        distances = {}
        for unvisitedNode in unvisited:
            distances[unvisitedNode.name] = (np.inf, "")
        distances[start] = (0, start)

        # While there are still some nodes
        # unvisited, proceed with Dijkstra"s algorithm
        while len(unvisited) != len(visited):
            distances_without_visited = {
                k: distances[k] for k in distances.keys() - visited
            }
            cur_node = min(
                distances_without_visited,
                key=lambda node: distances_without_visited.get(node),
            )
            for path in [
                path for path
                in self._paths
                if (cur_node == path._source)
                and path.get_available_capacity() > 0
            ]:
                if (
                    distances[cur_node][0]
                    + path._distance
                    < distances[path._target][0]
                ):
                    distances[path._target] = (
                        distances[cur_node][0] + path._distance, cur_node
                    )
            visited.append(cur_node)

        return distances

    def get_maximum_available_lambdas(self, path: list[str]) -> float:
        """
        For path given as a list of city names it returns the maximum
        possible lambda availability in entire path. Let"s say there
        are 3 nodes : A, B, C in a path. A->B has the current lambda
        availability at 20, and the B->C at 12. The algorithm then
        returns 12, as it"s the bottleneck of the entire path.
        """

        maxAvailableLambdas = np.inf
        for source, target in zip(path[:-1], path[1:]):
            path = next(
                element for element
                in self._paths
                if element.matches_source_and_target(source, target)
            )
            if path.get_available_capacity() < maxAvailableLambdas:
                maxAvailableLambdas = path.get_available_capacity()
        return maxAvailableLambdas

    def get_shortest_available_path(
        self, source: str, target: str
    ) -> list[str]:
        """
        Using available algorithms and methods
        it calculates the shortest available path
        for two cities given as their names.
        """
        pathMap = self.findAllPaths(source)
        if pathMap[target][0] == np.inf:
            raise Exception("Max lambda capacity achieved, can't find path.")

        shortest_path = [target]
        start = target
        while source not in shortest_path:
            start = pathMap[start][1]
            shortest_path.append(start)
        shortest_path.reverse()

        return shortest_path

    def increase_path_lambdas(
        self, source: str, target: str, lambdas: int
    ) -> None:
        """
        Increases the lambda capacity for the
        path given as source and target node names
        """

        pathToModify = next(
            element for element
            in self._paths
            if element.matches_source_and_target(source, target)
        )
        pathToModify.increase_lambdas(lambdas)

    def increase_lambdas(self, path: list[str], lambdas: int) -> None:
        """
        Increases the lambdas capacity for each
        path entity in between nodes in path given
        as list of city names
        """

        for source, target in zip(path[:-1], path[1:]):
            self.increase_path_lambdas(source, target, lambdas)

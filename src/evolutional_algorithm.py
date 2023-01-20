from classes import Individual, Demand, Connection
import random


TRANSPONDERS = [100, 200, 400]


class EvolutionalAlgorithm:

    def __init__(self, model):
        self._model = model

        # self.population = self.generateBasePopulation()

    def generateBasePopulation(
        self, size: int
    ) -> list[Individual]:
        return [
            self.generateRandomIndividual()
            for _ in range(size)
        ]

    def generateRandomIndividual(self):
        individual = Individual()

        for demand in self._model.getDemands():
            connections = [self.generateConection(demand)]

            individual.appendDemand(
                demand_id=demand.id,
                connections=connections
            )

        return individual

    def generateConection(self, demand: Demand):
        path = self._model.getShortestPath(
            demand.source, demand.target
        )
        self._model.decreaseCapacity(path)

        transponders = {
            transponder: 0 for transponder
            in TRANSPONDERS
        }
        value = demand.value
        while value > 0:
            transponder = random.choice(TRANSPONDERS)
            transponders[transponder] += 1
            value -= transponder

        return Connection(path, transponders)

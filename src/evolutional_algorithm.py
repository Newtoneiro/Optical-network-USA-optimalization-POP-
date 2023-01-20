from classes import Individual


class EvolutionalAlgorithm:

    def __init__(self, model):
        self._model = model

        self.population = self.generateBasePopulation()

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
            # TODO:
            connections = None

            individual.appendDemand(
                demand_id=demand.id,
                connections=connections
            )

        return individual

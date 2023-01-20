class EvolutionalAlgorithm:

    def __init__(self, model):
        self._model = model

        self.initBasePopulation()

    def initBasePopulation(self):
        for demand in self._model.getDemands():
            source, target, value = demand.source, demand.target, demand.value

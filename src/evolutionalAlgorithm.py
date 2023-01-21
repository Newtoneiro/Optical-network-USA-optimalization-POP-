from classes import Individual, Demand
from model import Model
from config.config import *
import random
import copy

class EvolutionalAlgorithm:
    """
    This is the abstract class representing evolutional algorithm, it makes it easier to manage
    populations and perform the evolution
    """
    def __init__(self, baseModel: Model) -> None:
        self._baseModel = baseModel
        self.population = self.generateBasePopulation(5)

    def generateBasePopulation(self, size: int) -> list[Individual]:
        """
        Initializes base population
        """
        return [self.generateRandomIndividual() for _ in range(size)]

    def generateRandomIndividual(self) -> None:
        """
        Initializes single individual in population
        """
        individualModel = copy.deepcopy(self._baseModel)
        individual = Individual()

        for demand in individualModel.getDemands():
            # for now generating single connection
            genome = self.generateDemandFullfilment(demand, individualModel)

            individual.appendDemand(
                demand_id=demand.id,
                genome=genome
            )

        return individual

    def generateDemandFullfilment(self, demand: Demand, model: Model) -> list:
        """
        Returns proposed demand fullfilment for given demand
        """
        value = demand.value
        genome = []
        if (demand.id == "LosAngeles-LasVegas"):
            print('dupa')

        while value > 0:
            path = model.getShortestAvailablePath(demand.source, demand.target)
            maxFreeLambdasInPath = model.getMaximumAvailableLambdas(path)
            transponders = {
                transponder: 0 for transponder in TRANSPONDERS
            }
            demandedLambdas = 0
            while maxFreeLambdasInPath > 0 and value > 0:
                transponder = random.choice(TRANSPONDERS)
                transponders[transponder] += 1
                value -= transponder
                demandedLambdas += 1
                maxFreeLambdasInPath -= 1

            model.increaseLambdas(path, demandedLambdas)
            
            genome.append((path, transponders))

        return genome

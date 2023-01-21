from classes import Individual, Demand
from model import Model
from config.config import *
import random

class EvolutionalAlgorithm:
    """
    This is the abstract class representing evolutional algorithm, it makes it easier to manage
    populations and perform the evolution
    """
    def __init__(self, model: Model) -> None:
        self._model = model

        self.population = self.generateBasePopulation(1)

    def generateBasePopulation(self, size: int) -> list[Individual]:
        """
        Initializes base population
        """
        return [self.generateRandomIndividual() for _ in range(size)]

    def generateRandomIndividual(self) -> None:
        """
        Initializes single individual in population
        """
        individual = Individual()

        for demand in self._model.getDemands():
            # for now generating single connection
            genome = self.generateDemandFullfilment(demand)

            individual.appendDemand(
                demand_id=demand.id,
                genome=genome
            )

        return individual

    def generateDemandFullfilment(self, demand: Demand) -> list:
        """
        Returns proposed demand fullfilment for given demand
        """
        value = demand.value
        genome = []

        while value > 0:
            path = self._model.getShortestAvailablePath(demand.source, demand.target)
            maxFreeLambdasInPath = self._model.getMaximumAvailableLambdas(path)
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

            self._model.increaseLambdas(path, demandedLambdas)
            
            genome.append((path, transponders))
        
        if len(genome) > 1:
            print(genome)

        return genome

from classes import Individual, Demand
from model import Model
from config.config import (
    TRANSPONDERS,
    DEMAND_MUTATION_PROBABILITY,
    # CONNECTION_MUTATION_PROBABILITY,
    TYPE_MUTATION_PROBABILITY
)
import random
import copy


class EvolutionalAlgorithm:
    """
    This is the abstract class representing evolutional
    algorithm, it makes it easier to manage
    populations and perform the evolution
    """

    def __init__(
        self, baseModel: Model, demands: list[Demand], size: int
    ) -> None:
        self.base_model = baseModel
        self.demands = demands
        self.population = self.generate_base_population(size)

    def generate_base_population(self, size: int) -> list[Individual]:
        """
        Initializes base population
        """

        return [
            self.generate_random_individual()
            for _ in range(size)
        ]

    def generate_random_individual(self) -> Individual:
        """
        Initializes single individual in population
        """

        individual = Individual()
        individual_model = copy.deepcopy(self.base_model)

        for demand in self.demands:
            # for now generating single connection
            genome = self.generate_demand_fullfilment(demand, individual_model)
            individual.append_demand(
                demand_id=demand.id,
                genome=genome
            )

        return individual

    def mutate_individual(self, individual: Individual) -> Individual:
        """
        Create new indiviudal by mutation
        """

        mutated_individual = copy.deepcopy(individual)
        mutated_individual_model = copy.deepcopy(self.base_model)

        # mutate tranponders
        for demand_id in mutated_individual.content:
            if random.random() > DEMAND_MUTATION_PROBABILITY:
                continue

            demand_transponders = {
                transponder: 0
                for transponder
                in TRANSPONDERS
            }

            demand_ff = mutated_individual.content[demand_id]

            for connection in demand_ff:
                connection_transponders = connection[1]
                for transponder in connection_transponders:
                    number = connection_transponders[transponder]
                    demand_transponders[transponder] += number

            mutated_demand_transponders = copy.deepcopy(demand_transponders)

            for type in TRANSPONDERS:
                if random.random() > TYPE_MUTATION_PROBABILITY:
                    continue

                number = mutated_demand_transponders[type]
                if type == 100:
                    if number >= 2:
                        # 2x100 -> 1x200
                        mutated_demand_transponders[100] -= 2
                        mutated_demand_transponders[200] += 1
                elif type == 200:
                    if random.random() > 0.5:  # convert to 400 or 100
                        if number >= 2:
                            # 2x200 -> 1x400
                            mutated_demand_transponders[200] -= 2
                            mutated_demand_transponders[400] += 1
                    else:
                        if number >= 1:
                            # 1x200 -> 2x100
                            mutated_demand_transponders[200] -= 1
                            mutated_demand_transponders[100] += 2
                elif type == 400:
                    if number >= 1:
                        # 1x400 -> 2x200
                        mutated_demand_transponders[400] -= 1
                        mutated_demand_transponders[200] += 2

            # generate new demand fullfilment
            new_demand_ff = self.generate_demand_fullfilment(
                demand=self.get_demand_by_id(demand_id),
                model=mutated_individual_model,
                transponders=mutated_demand_transponders
            )

            mutated_individual.content[demand_id] = new_demand_ff

        return mutated_individual

    def get_demand_by_id(self, id: str) -> Demand | None:
        for demand in self.demands:
            if demand.id == id:
                return demand
        return None

    def generate_demand_fullfilment(
        self, demand: Demand, model: Model, transponders: map = None
    ) -> list:
        """
        Returns proposed demand fullfilment for given demand
        """

        available_transponders = copy.deepcopy(transponders)

        value = demand.value
        if not available_transponders:
            available_transponders = self.generate_random_transponders(value)
        else:
            assert (sum([
                key * value for key, value in available_transponders.items()
            ]) >= value)

        genome = []

        while any([val > 0 for val in available_transponders.values()]):
            path = model.get_shortest_available_path(
                demand.source, demand.target
            )
            maxFreeLambdasInPath = model.get_maximum_available_lambdas(path)
            transponders_for_path = {
                transponder: 0 for transponder in TRANSPONDERS
            }
            demandedLambdas = 0
            while maxFreeLambdasInPath > 0 and any([
                val > 0 for val in available_transponders.values()
            ]):
                selected_transponder = random.choice([
                    transponder_value for transponder_value
                    in available_transponders.keys()
                    if available_transponders[transponder_value] > 0])

                available_transponders[selected_transponder] -= 1

                transponders_for_path[selected_transponder] += 1
                value -= selected_transponder
                demandedLambdas += 1
                maxFreeLambdasInPath -= 1

            model.increase_lambdas(path, demandedLambdas)

            genome.append((path, transponders_for_path))

        return genome

    def generate_random_transponders(self, demand_value: float) -> map:
        """
        Generates random transponders that fulfill given demand value.
        """
        transponders = {
            transponder: 0 for transponder in TRANSPONDERS
        }
        while demand_value > 0:
            selected_transponder = random.choice(TRANSPONDERS)
            transponders[selected_transponder] += 1
            demand_value -= selected_transponder

        return transponders

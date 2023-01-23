from classes import Individual, Demand
from model import Model
from config.config import (
    TRANSPONDERS,
    INDIVIDUAL_MUTATION_PROBABILITY,
    MUTATION_PROBABILITY,
    TYPE_MUTATION_PROBABILITY,
    CROSSOVER_PROBABILITY,
    NO_EPOCHS
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
        self, base_model: Model, demands: list[Demand], size: int
    ) -> None:
        self.population_size = size
        self.base_model = base_model
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

    def run(self) -> None:
        """
        Starts the algorithm
        """
        cur_epoch = 1
        while cur_epoch <= NO_EPOCHS:
            self.step()
            # best_score = \
            #     min(self.population, key=lambda a: a.get_cost()).get_cost()
            scores = set([individual.get_cost() for individual in self.population])
            print(f"Epoch {cur_epoch}/{NO_EPOCHS}, len: {len(self.population)} score: {scores}, best_score: {min(scores)}")
            cur_epoch += 1

    def step(self) -> None:
        """
        Performs selection and mutation for given epoch
        """
        selected_population = self.selection(self.population)
        crossover_population = self.crossover(selected_population)
        mutated_population = self.mutation(crossover_population)
        # mutated_population = self.mutation(selected_population)
        self.population = mutated_population

    def selection(self, population: list[Individual]) -> list[Individual]:
        """
        Selects individuals for new population using tournament selections
        with one elite member
        """
        new_population = []
        # Pick an elite member
        new_population.append(min(population, key=lambda a: a.get_cost()))

        while len(new_population) < self.population_size:
            first_individual = random.choice(population)
            second_individual = random.choice(population)
            if (first_individual.get_cost() < second_individual.get_cost()):
                new_population.append(first_individual)
            else:
                new_population.append(second_individual)
        return new_population

    def crossover(self, population: list[Individual]) -> list[Individual]:
        """
        Does crossover on population
        """
        crossover_population = []
        for individual in population:
            if random.random() > CROSSOVER_PROBABILITY:
                crossover_population.append(individual)
                continue

            individual_model = copy.deepcopy(self.base_model)
            individual_partner = random.choice(population)
            crossover_individual = Individual()
            for demand_id in [demand.id for demand in self.demands]:
                if random.random() < 0.5:
                    demand_transponders = individual.sum_transponders(
                        demand_id
                    )
                else:
                    demand_transponders = individual_partner.sum_transponders(
                        demand_id
                    )
                new_genome = self.generate_demand_fullfilment(
                    demand=self.get_demand_by_id(demand_id),
                    model=individual_model,
                    transponders=demand_transponders
                )
                crossover_individual.append_demand(demand_id, new_genome)

            crossover_population.append(crossover_individual)

        return crossover_population

    def mutation(self, population: list[Individual]) -> list[Individual]:
        """
        Mutates every individual in population
        with given probability
        """
        mutated_population = [
            self.mutate_individual(individual)
            if random.random() < INDIVIDUAL_MUTATION_PROBABILITY
            else individual
            for individual in population
        ]

        return mutated_population

    def mutate_individual(self, individual: Individual) -> Individual:
        """
        Creates new indiviudal by mutating the given one
        according to a given set of probabilities
        """

        mutated_individual = copy.deepcopy(individual)
        mutated_individual_model = copy.deepcopy(self.base_model)

        # mutate tranponders
        for demand_id in mutated_individual.content:
            if random.random() > MUTATION_PROBABILITY:
                continue

            demand_transponders = mutated_individual.sum_transponders(
                demand_id
            )

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
                    # continue
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
                    # continue
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

            mutated_individual.append_demand(demand_id, new_demand_ff)

        return mutated_individual

    def get_demand_by_id(self, id: str) -> Demand or None:
        """
        Retruns "Demand" class object from base model
        that has the same id as given
        """

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
            max_free_lambdas_in_path = model.get_maximum_available_lambdas(
                path
            )
            transponders_for_path = {
                transponder: 0 for transponder in TRANSPONDERS
            }
            demandedLambdas = 0
            while max_free_lambdas_in_path > 0 and any([
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
                max_free_lambdas_in_path -= 1

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

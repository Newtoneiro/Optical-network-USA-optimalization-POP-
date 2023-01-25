from classes import Individual, Demand
from model import Model
from config.config import (
    TRANSPONDERS,
    POPULATION_SIZE,
    INDIVIDUAL_MUTATION_PROBABILITY,
    DEMAND_MUTATION_PROBABILITY,
    CROSSOVER_PROBABILITY,
    NO_EPOCHS,
    OUTPUT_PATH
)
import random
import copy
import csv


class EvolutionalAlgorithm:
    """
    This is the abstract class representing evolutional
    algorithm, it makes it easier to manage
    populations and perform the evolution
    """

    def __init__(
        self,
        base_model: Model,
        demands: list[Demand],
        pop_size: int = POPULATION_SIZE,
        cross_prob: float = CROSSOVER_PROBABILITY,
        indiv_mut_prob: float = INDIVIDUAL_MUTATION_PROBABILITY,
        demand_mut_prob: float = DEMAND_MUTATION_PROBABILITY,
        epochs: int = NO_EPOCHS
    ) -> None:
        self.population_size = pop_size
        self.cross_prob = cross_prob
        self.indiv_mut_prob = indiv_mut_prob
        self.demands_mut_prob = demand_mut_prob
        self.epochs = epochs
        self.base_model = base_model
        self.demands = demands
        self.population = self.generate_base_population(pop_size)

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
            genome = self.generate_demand_fulfillment(demand, individual_model)
            individual.append_demand(
                demand_id=demand.id,
                genome=genome
            )

        return individual

    def run(self, save_bests: bool = False) -> None:
        """
        Starts the algorithm
        """
        cur_epoch = 1
        best_values = []
        while cur_epoch <= self.epochs:
            self.step()
            scores = set([
                individual.get_cost() for individual in self.population
                ])
            print(f"Epoch {cur_epoch}/{self.epochs} best_score: {min(scores)}")
            if (save_bests):
                best_values.append(min(scores))
            cur_epoch += 1

        return best_values

    def step(self) -> None:
        """
        Performs selection and mutation for given epoch
        """
        selected_population, elite = self.selection(self.population)
        crossover_population = self.crossover(selected_population)
        mutated_population = self.mutation(crossover_population)
        self.population = mutated_population
        # Add elite
        self.population.append(copy.deepcopy(elite))

    def selection(self, population: list[Individual]) -> list[Individual]:
        """
        Selects individuals for new population using tournament selections
        with one elite member
        """
        new_population = []
        # Pick an elite member
        elite = min(population, key=lambda a: a.get_cost())

        while len(new_population) < self.population_size - 1:  # For elite
            first_individual = random.choice(population)
            second_individual = random.choice(population)
            if (first_individual.get_cost() < second_individual.get_cost()):
                new_population.append(first_individual)
            else:
                new_population.append(second_individual)
        return new_population, elite

    def crossover(self, population: list[Individual]) -> list[Individual]:
        """
        Does crossover on population
        """
        crossover_population = []
        for individual in population:
            if random.random() > self.cross_prob:
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
                new_genome = self.generate_demand_fulfillment(
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
        mutated_population = []
        for individual in population:
            if random.random() > self.indiv_mut_prob:
                mutated_population.append(individual)
                continue

            mutated_individual = Individual()
            individual_model = copy.deepcopy(self.base_model)
            for demand_id in [demand.id for demand in self.demands]:
                demand_transponders = individual.sum_transponders(
                    demand_id
                )
                if random.random() < self.demands_mut_prob:
                    # If mutation occured, change transponders
                    transponder_to_change = random.choice(TRANSPONDERS)
                    transponder_to_change_to = random.choice(
                        [t for t in TRANSPONDERS if t != transponder_to_change]
                    )
                    ratio = transponder_to_change / transponder_to_change_to
                    if (ratio > 1):
                        if demand_transponders[transponder_to_change] > 1:
                            demand_transponders[transponder_to_change] -= 1
                            demand_transponders[
                                transponder_to_change_to
                            ] += ratio
                    else:
                        if demand_transponders[
                                transponder_to_change] > int(1/ratio):
                            demand_transponders[
                                transponder_to_change
                            ] -= int(1/ratio)
                            demand_transponders[transponder_to_change_to] += 1

                new_genome = self.generate_demand_fulfillment(
                    demand=self.get_demand_by_id(demand_id),
                    model=individual_model,
                    transponders=demand_transponders
                )
                mutated_individual.append_demand(demand_id, new_genome)
            mutated_population.append(mutated_individual)

        return mutated_population

    def get_demand_by_id(self, id: str) -> Demand or None:
        """
        Retruns "Demand" class object from base model
        that has the same id as given
        """

        for demand in self.demands:
            if demand.id == id:
                return demand
        return None

    def generate_demand_fulfillment(
        self, demand: Demand, model: Model, transponders: map = None
    ) -> list:
        """
        Returns proposed demand fulfillment for given demand
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

    def save_result(self) -> None:
        with open(OUTPUT_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Demand_id",
                 "Path",
                 "Transponder-100",
                 "Transponder-200",
                 "Transponder-400"]
            )
            best_individual = min(self.population, key=lambda a: a.get_cost())
            for demand_id in best_individual.content:
                for fulfillment in best_individual.content[demand_id]:
                    writer.writerow(
                        [demand_id,
                         fulfillment[0],
                         fulfillment[1][100],
                         fulfillment[1][200],
                         fulfillment[1][400]]
                    )

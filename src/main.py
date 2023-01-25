from data_loader import DataLoader
from model import Model
from evolutional_algorithm import EvolutionalAlgorithm
import random
import matplotlib.pyplot as plt
import os

from config.config import SEED, NO_EPOCHS, DATA_PATH

dir_path = os.path.dirname(os.path.realpath(__file__))

tests = {
    "Crossover_probability": [0.1, 0.3, 0.5, 0.9],
    "Demand_mutation_probability": [0.1, 0.3, 0.5, 0.9],
    "Population_size": [2, 10, 20, 30]
}

if __name__ == "__main__":
    if SEED != 0:
        random.seed(SEED)

    data_loader = DataLoader(f"{dir_path}/../{DATA_PATH}")
    demands = data_loader.get_demands()
    model = Model(
        data_loader.get_nodes(),
        data_loader.get_paths()
    )

    epoch_axis = range(NO_EPOCHS)
    for metric, values in tests.items():
        plt.clf()
        print(f"===| Testing for metric: {metric} |===")
        if metric == "Crossover_probability":
            for value in values:
                print(f"--> Testing for value: {value}")
                ea = EvolutionalAlgorithm(
                    base_model=model,
                    demands=demands,
                    cross_prob=value,
                )
                best_scores = ea.run(save_bests=True)
                plt.plot(epoch_axis, best_scores, label=f'Value: {value}')
        elif metric == "Demand_mutation_probability":
            for value in values:
                print(f"--> Testing for value: {value}")
                ea = EvolutionalAlgorithm(
                    base_model=model,
                    demands=demands,
                    demand_mut_prob=value
                )
                best_scores = ea.run(save_bests=True)
                plt.plot(epoch_axis, best_scores, label=f'Value: {value}')
        elif metric == "Population_size":
            for value in values:
                print(f"--> Testing for value: {value}")
                ea = EvolutionalAlgorithm(
                    base_model=model,
                    demands=demands,
                    pop_size=value
                )
                best_scores = ea.run(save_bests=True)
                plt.plot(epoch_axis, best_scores, label=f'Value: {value}')
        plt.xlabel("Epoch")
        plt.ylabel("Best in epoch")
        plt.ylim(bottom=30_000)
        plt.title(metric)
        plt.legend()
        plt.savefig(f'{dir_path}/../plots/{metric}.png')

    # ea.save_result())

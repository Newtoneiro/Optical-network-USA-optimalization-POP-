from data_loader import DataLoader
from model import Model
from evolutional_algorithm import EvolutionalAlgorithm
import random

from config.config import SEED

if __name__ == "__main__":
    if SEED != 0:
        random.seed(SEED)

    data_loader = DataLoader("janos-us-ca.xml")
    model = Model(
        data_loader.get_nodes(),
        data_loader.get_paths()
    )
    ea = EvolutionalAlgorithm(model, data_loader.get_demands(), size=5)
    ea.run()
    ea.save_result()

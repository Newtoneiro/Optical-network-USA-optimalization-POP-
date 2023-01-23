from data_loader import DataLoader
from model import Model
from evolutional_algorithm import EvolutionalAlgorithm

if __name__ == "__main__":
    data_loader = DataLoader("janos-us-ca.xml")
    model = Model(
        data_loader.get_nodes(),
        data_loader.get_paths()
    )
    ea = EvolutionalAlgorithm(model, data_loader.get_demands(), size=10)
    ea.run()

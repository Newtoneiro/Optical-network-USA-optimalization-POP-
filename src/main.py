from data_loader import DataLoader
from model import Model
from evolutional_algorithm import EvolutionalAlgorithm

# test_nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
# test_paths = [Path('a', 'b'), Path('b', 'c'), Path('b', 'e'), Path('b', 'f'), Path('c', 'g'),
#     Path('c', 'd'), Path('d', 'e'), Path('e', 'f'), Path('g', 'f'), Path('f', 'h'), Path('h', 'i')
# ]
# test_model = Model(test_nodes, test_paths, [])

if __name__ == "__main__":
    data_loader = DataLoader("janos-us-ca.xml")
    model = Model(
        data_loader.get_nodes(),
        data_loader.get_paths(),
        data_loader.get_demands()
    )
    EA = EvolutionalAlgorithm(model)

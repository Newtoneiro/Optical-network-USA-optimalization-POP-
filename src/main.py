from data_loader import DataLoader
from model import Model
from evolutional_algorithm import EvolutionalAlgorithm

# test_nodes = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
# test_paths = [
#     Path("a", "b"), Path("b", "c"), Path("b", "e"),
#     Path("b", "f"), Path("c", "g"), Path("c", "d"),
#     Path("d", "e"), Path("e", "f"), Path("g", "f"),
#     Path("f", "h"), Path("h", "i")
# ]
# test_model = Model(test_nodes, test_paths, [])

if __name__ == "__main__":
    data_loader = DataLoader("janos-us-ca.xml")
    model = Model(
        data_loader.get_nodes(),
        data_loader.get_paths()
    )
    ea = EvolutionalAlgorithm(model, data_loader.get_demands(), size=2)
    # for individual in ea.population:
    #     print(individual.content["Vancouver-LosAngeles"])
    #     print(individual.get_cost())
    # print(ea.population[0].content)
    # ea.mutate_individual(ea.population[0])

    a = ea.population[0]
    print(a.content["Vancouver-LosAngeles"][0])
    print(a.get_cost())
    a = ea.mutate_individual(a)
    print()
    print(a.content["Vancouver-LosAngeles"][0])
    print(a.get_cost())

    # path = model.get_shortest_available_path("Calgary", "Denver", 80)
    # model.increase_lambdas(path, 90)
    # path = model.get_shortest_available_path("Calgary", "Denver", 80)
    # print(path)

    # demand = ea._model._demands[0]
    # print(demand)
    # print(ea.generateConections(demand))

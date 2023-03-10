# GLOBAL
SEED = 0

# PATH
MAX_PATH_CAPACITY = 1008

# TRANSPONDERS
TRANSPONDERS = [100, 200, 400]
TRANSPONDERS_COSTS = {
    100: 1,
    200: 3,
    400: 7
}

# EVOLUTIONAL ALGORITHM
POPULATION_SIZE = 20
NO_EPOCHS = 30
INDIVIDUAL_MUTATION_PROBABILITY = 1.0
DEMAND_MUTATION_PROBABILITY = 0.5
CROSSOVER_PROBABILITY = 0.5

# FILES
OUTPUT_PATH = 'output.csv'
DATA_PATH = 'data/janos-us-ca.xml'

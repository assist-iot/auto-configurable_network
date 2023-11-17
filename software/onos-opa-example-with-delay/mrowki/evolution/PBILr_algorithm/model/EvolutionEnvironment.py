class EvolutionEnvironment:
    population_size = 100
    cross_probability = 90
    mutation_probability = 5
    learning_rate = 0.05
    best_chromosomes_limit = int(population_size * 0.05)

    def __init__(self, links, demands, paths_for_demand):
        self.links = links
        self.demands = demands
        self.paths_for_demand = paths_for_demand
        self.probability_vector = []
        self.reset_probability_vector()

    def reset_probability_vector(self):
        self.probability_vector = [0.5] * len(self.paths_for_demand.keys())

    def learn(self, best_chromosomes: []):
        for chromosome in best_chromosomes:
            for i in range(len(self.probability_vector)):
                self.probability_vector[i] = (1 - self.learning_rate) * self.probability_vector[i] + self.learning_rate * chromosome.paths_vector[i]

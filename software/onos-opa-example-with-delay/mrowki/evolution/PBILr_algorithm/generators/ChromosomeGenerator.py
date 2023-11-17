import random

from evolution.PBILr_algorithm.model.Chromosome import Chromosome
from evolution.PBILr_algorithm.model.EvolutionEnvironment import EvolutionEnvironment


class ChromosomeGenerator:

    @staticmethod
    def generate_population(environment: EvolutionEnvironment):
        population = []
        for i in range(environment.population_size):
            population.append(ChromosomeGenerator.__generate_chromosome(environment))
        return population

    @staticmethod
    def __generate_chromosome(environment: EvolutionEnvironment):
        paths_vector = []
        for probability in environment.probability_vector:
            value = random.random()
            if value < probability:
                paths_vector.append(0)
            else:
                paths_vector.append(1)
        return Chromosome(paths_vector)

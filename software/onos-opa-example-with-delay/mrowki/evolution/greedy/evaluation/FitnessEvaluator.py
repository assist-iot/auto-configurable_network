from ants_algorithm.model.AntEnvironment import AntEnvironment
from evolution.greedy.model.Chromosome import Chromosome


class FitnessEvaluator:

    @staticmethod
    def evaluate_fitness_value(chromosome: Chromosome, ant_environment: AntEnvironment):
        fitness_value = 0
        for link_id, value in chromosome.links_usage_map.items():
            fitness_value = fitness_value + max(value - ant_environment.links.links_map_id[link_id].capacity, 0) * 10
        return fitness_value

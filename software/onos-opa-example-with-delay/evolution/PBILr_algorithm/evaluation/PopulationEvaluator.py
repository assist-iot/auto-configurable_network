from evolution.PBILr_algorithm.evaluation.FitnessValueResolver import FitnessValueResolver
from evolution.PBILr_algorithm.model.Chromosome import Chromosome
from evolution.PBILr_algorithm.model.EvolutionEnvironment import EvolutionEnvironment


class PopulationEvaluator:

    @staticmethod
    def evaluate_population(population: [], environment: EvolutionEnvironment):
        for chromosome in population:
            PopulationEvaluator.__evaluate_chromosome(chromosome, environment)

    @staticmethod
    def __evaluate_chromosome(chromosome: Chromosome, environment: EvolutionEnvironment):
        chromosome.fitness_value = FitnessValueResolver.calculate_fitness_value(chromosome, environment)

    @staticmethod
    def select_best_chromosomes(population: [], environment: EvolutionEnvironment):
        population.sort(key=PopulationEvaluator.__sort_function)
        return population[0:environment.best_chromosomes_limit]

    @staticmethod
    def __sort_function(value: Chromosome):
        return value.fitness_value

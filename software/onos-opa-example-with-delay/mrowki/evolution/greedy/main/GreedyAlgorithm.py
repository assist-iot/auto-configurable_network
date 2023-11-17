from ants_algorithm.main.PathsForDemandProvider import PathsForDemandProvider
from ants_algorithm.model.AntEnvironment import AntEnvironment
from events.EventProvider import EventProvider
from evolution.greedy.evaluation.EventProcessing import EventProcessing
from evolution.greedy.evaluation.FitnessEvaluator import FitnessEvaluator
from evolution.greedy.generator.ChromosomeGenerator import ChromosomeGenerator


class GreedyAlgorithm:

    @staticmethod
    def calculate(ant_environment: AntEnvironment, paths_for_demand):
        iterations_number = 1
        chromosome = ChromosomeGenerator.create_initial_chromosome(paths_for_demand, ant_environment)
        FitnessEvaluator.evaluate_fitness_value(chromosome, ant_environment)
        new_paths_for_demand = paths_for_demand
        while iterations_number < 1000000:
            if EventProvider.is_event_time(iterations_number):
                EventProcessing.process_event(ant_environment, new_paths_for_demand, chromosome)
                FitnessEvaluator.evaluate_fitness_value(chromosome, ant_environment)

            if EventProvider.is_reevaluation_time(iterations_number):
                for link in ant_environment.links.links_map_id.values():
                    link.pheromone = 0
                new_paths_for_demand = PathsForDemandProvider.calculate_paths_for_demand(ant_environment, "reevaluated_results.csv")
            #     TODO można porównać jak bardzo się różni new_paths_for_demand od paths_for_demand
            iterations_number = iterations_number + 1

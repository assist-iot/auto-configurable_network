from events.EventProvider import EventProvider
from evolution.PBILr_algorithm.evaluation.EventProcessing import EventProcessing
from evolution.PBILr_algorithm.evaluation.PopulationEvaluator import PopulationEvaluator
from evolution.PBILr_algorithm.generators.ChromosomeGenerator import ChromosomeGenerator
from evolution.PBILr_algorithm.model.EvolutionEnvironment import EvolutionEnvironment

# Implementacja algorytmu PBILr


class EvolutionAlgorithm:

    @staticmethod
    def calculate(evolution_environment: EvolutionEnvironment):
        best_fitness_value = 99999999
        iterations_number = 0
        evolution_environment.reset_probability_vector()
        while best_fitness_value != 0 and iterations_number < 1000000:
            new_population = ChromosomeGenerator.generate_population(evolution_environment)
            PopulationEvaluator.evaluate_population(new_population, evolution_environment)
            best_chromosomes = PopulationEvaluator.select_best_chromosomes(new_population, evolution_environment)
            if best_fitness_value > best_chromosomes[0].fitness_value:
                best_fitness_value = best_chromosomes[0].fitness_value
            evolution_environment.learn(best_chromosomes)
            iterations_number = iterations_number + 1

            if EventProvider.is_event_time(iterations_number):
                EventProcessing.process_event(evolution_environment)
                best_fitness_value = 99999999

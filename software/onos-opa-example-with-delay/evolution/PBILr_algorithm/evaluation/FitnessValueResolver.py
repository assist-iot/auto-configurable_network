from ants_algorithm.model.AntPathSolution import AntPathSolution
from evolution.PBILr_algorithm.model.Chromosome import Chromosome
from evolution.PBILr_algorithm.model.EvolutionEnvironment import EvolutionEnvironment


class FitnessValueResolver:

    @staticmethod
    def calculate_fitness_value(chromosome: Chromosome, environment: EvolutionEnvironment):
        fitness_value = 0
        demand_sum_on_link_map = {}
        paths_for_demand_keys = list(environment.paths_for_demand.keys())
        for path_index in range(len(chromosome.paths_vector)):
            demand_id = paths_for_demand_keys[path_index]
            demand_paths = environment.paths_for_demand[demand_id]
            if chromosome.paths_vector[path_index] == 0:
                path_solution: AntPathSolution = demand_paths.first_path
            else:
                path_solution: AntPathSolution = demand_paths.second_path

            for link in path_solution.path:
                demand_value = environment.demands.demands_map_id[demand_id].value
                if link.link_id in demand_sum_on_link_map:
                    demand_sum_on_link_map[link.link_id] = demand_sum_on_link_map[link.link_id] + demand_value
                else:
                    demand_sum_on_link_map[link.link_id] = demand_value

        for link_id, value in demand_sum_on_link_map.items():
            current_link = environment.links.links_map_id[link_id]
            link_capacity = current_link.capacity
            fitness_value = fitness_value + current_link.cost
            if value > link_capacity:
                fitness_value = fitness_value + 10000 * (value - link_capacity)

        return fitness_value

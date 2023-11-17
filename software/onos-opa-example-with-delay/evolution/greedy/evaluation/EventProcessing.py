import random

from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.AntPathSolution import AntPathSolution
from evolution.greedy.model.Chromosome import Chromosome


class EventProcessing:

    @staticmethod
    def process_event(environment: AntEnvironment, paths_for_demand, chromosome: Chromosome):
        keys = list(environment.demands.demands_map_id.keys())
        key_index = random.randint(0, len(keys) - 1)
        key = keys[key_index]
        old_value = environment.demands.demands_map_id[key].value
        new_value = old_value * 2
        environment.demands.demands_map_id[key].value = new_value
        print('Event changed demand', key, 'value from', old_value, 'to', new_value)

        demand_paths = paths_for_demand[key]
        if chromosome.path_first_or_second_map[key] == 0:
            for link in demand_paths.first_path.path:
                chromosome.links_usage_map[link.link_id] = chromosome.links_usage_map[link.link_id] - old_value
        else:
            for link in demand_paths.second_path.path:
                chromosome.links_usage_map[link.link_id] = chromosome.links_usage_map[link.link_id] - old_value

        first_path_cost = EventProcessing.__calculate_path_cost(demand_paths.first_path, chromosome, new_value)
        second_path_cost = EventProcessing.__calculate_path_cost(demand_paths.second_path, chromosome, new_value)
        if first_path_cost <= second_path_cost:
            chromosome.path_first_or_second_map[key] = 0
            for link in demand_paths.first_path.path:
                EventProcessing.update_links_values(chromosome, environment, link, new_value)
        else:
            chromosome.path_first_or_second_map[key] = 1
            for link in demand_paths.second_path.path:
                EventProcessing.update_links_values(chromosome, environment, link, new_value)

    @staticmethod
    def update_links_values(chromosome, environment, link, new_value):
        new_demand_value = chromosome.links_usage_map[link.link_id] + new_value
        chromosome.links_usage_map[link.link_id] = new_demand_value
        if new_demand_value > link.capacity:
            overflow = new_demand_value - link.capacity
            chosen_extensions = 0
            while overflow > 0:
                max_extension = environment.capacity_extensions[len(environment.capacity_extensions) - 1]
                if overflow > max_extension:
                    chosen_extensions = chosen_extensions + max_extension
                    overflow = overflow - max_extension
                else:
                    for extension in environment.capacity_extensions:
                        if extension >= overflow:
                            chosen_extensions = chosen_extensions + extension
                            overflow = overflow - extension
                            break
            if link.link_id in environment.capacities_extended:
                environment.capacities_extended[link.link_id] = environment.capacities_extended[link.link_id] + chosen_extensions
            else:
                environment.capacities_extended[link.link_id] = chosen_extensions

    @staticmethod
    def __calculate_path_cost(solution: AntPathSolution, chromosome: Chromosome, new_value):
        cost = 0
        for link in solution.path:
            new_value_on_link = chromosome.links_usage_map[link.link_id] + new_value
            cost = cost + link.cost + max(new_value_on_link - link.capacity, 0) * 10
        return cost

from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.AntPathSolution import AntPathSolution


class PheromoneUtil:

    @staticmethod
    def update_pheromones(iteration_number, visited_links, environment: AntEnvironment, path_x: AntPathSolution = None):
        for link_id in visited_links:
            increment = PheromoneUtil.__calculate_increment(environment, link_id, path_x)
            environment.links.links_map_id[link_id].pheromone = environment.links.links_map_id[link_id].pheromone + increment

        if iteration_number > 0 and iteration_number % 5 == 0:
            for link in environment.links.links_map_id.values():
                link.pheromone = max(link.pheromone - environment.pheromone_decrement, 0)

    @staticmethod
    def __calculate_increment(environment, link_id, path_x):
        if path_x is not None:
            return PheromoneUtil.__calculate_increment_for_y(environment, link_id, path_x)
        return PheromoneUtil.__calculate_increment_for_x(environment, link_id)

    @staticmethod
    def __calculate_increment_for_x(environment, link_id):
        increment = environment.pheromone_increment
        link_load = environment.links_usage_values[link_id] / environment.links.links_map_id[link_id].capacity
        increment = (1 - link_load) * increment
        return increment

    @staticmethod
    def __calculate_increment_for_y(environment, link_id, path_x):
        for link in path_x.path:
            if link.link_id == link_id:
                return 0.1 * environment.pheromone_increment
        return environment.pheromone_increment


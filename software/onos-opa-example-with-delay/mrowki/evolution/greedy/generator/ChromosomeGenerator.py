from ants_algorithm.model.AntEnvironment import AntEnvironment
from evolution.greedy.model.Chromosome import Chromosome


class ChromosomeGenerator:

    @staticmethod
    def create_initial_chromosome(paths_for_demand, environment: AntEnvironment):
        paths_vector = {}
        link_usage_map = {}
        for key, value in paths_for_demand.items():
            paths_vector[key] = 0
            for link in value.first_path.path:
                if link.link_id in link_usage_map:
                    link_usage_map[link.link_id] = link_usage_map[link.link_id] + environment.demands.demands_map_id[key].value
                else:
                    link_usage_map[link.link_id] = environment.demands.demands_map_id[key].value

        return Chromosome(paths_vector, link_usage_map)

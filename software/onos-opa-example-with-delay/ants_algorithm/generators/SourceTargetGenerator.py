import random

from ants_algorithm.model.AntEnvironment import AntEnvironment


class SourceTargetGenerator:

    @staticmethod
    def generate_source_and_target(environment: AntEnvironment):
        keys = list(environment.links.neighbours_links_map.keys())
        source = keys[random.randint(0, len(keys) - 1)]
        keys.remove(source)
        target = keys[random.randint(0, len(keys) - 1)]
        return source, target

    @staticmethod
    def generate_all_demands(environment: AntEnvironment):
        keys = list(environment.links.neighbours_links_map.keys())
        source = keys.pop()

        while len(keys) != 0:
            for key in keys:
                environment.demand_source_target.append([source, key])
            source = keys.pop()

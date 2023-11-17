import random

from evolution.PBILr_algorithm.model.EvolutionEnvironment import EvolutionEnvironment


class EventProcessing:

    @staticmethod
    def process_event(environment: EvolutionEnvironment):
        environment.reset_probability_vector()
        keys = list(environment.demands.demands_map_id.keys())
        key_index = random.randint(0, len(keys) - 1)
        key = keys[key_index]
        environment.demands.demands_map_id[key].value = environment.demands.demands_map_id[key].value * 2

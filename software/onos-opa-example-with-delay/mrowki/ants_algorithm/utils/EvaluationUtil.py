from ants_algorithm.model.Ant import Ant
from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.AntPathSolution import AntPathSolution


class EvaluationUtil:

    @staticmethod
    def evaluate(ant: Ant, x_path: AntPathSolution = None, environment: AntEnvironment = None):
        if x_path is None:
            return EvaluationUtil.__evaluate_x_solution(ant, environment)

        return EvaluationUtil.__evaluate_y_solution(ant, x_path)

    @staticmethod
    def __evaluate_x_solution(ant, environment):
        overloaded_links_number = 0
        for link in ant.last_solution.path:
            link_load = (environment.links_usage_values[link.link_id] + environment.current_demand.value) / link.capacity
            if link_load > 0.9:
                overloaded_links_number = overloaded_links_number + 1
        return overloaded_links_number

    @staticmethod
    def __evaluate_y_solution(ant, x_path):
        path_x_link_ids = set(map(lambda x: x.link_id, x_path.path))
        common_links_amount = 0
        for link in ant.last_solution.path:
            if link.link_id in path_x_link_ids:
                common_links_amount = common_links_amount + 1
        return common_links_amount

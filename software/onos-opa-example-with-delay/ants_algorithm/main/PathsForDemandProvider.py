import copy
import csv

from ants_algorithm.generators.PathGenerator import PathGenerator
from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.AntPathSolution import AntPathSolution
from ants_algorithm.model.DemandPaths import DemandPaths


# Algorytm mrówkowy znajdujący dwie najlepsze ścieżki, którymi może być zrealizowane zapotrzebowanie


class PathsForDemandProvider:

    @staticmethod
    def __prepare_test_demands(ant_environment: AntEnvironment):
        map_id = ant_environment.demands.demands_map_id
        return [map_id['Essen_Duesseldorf'], map_id['Essen_Koeln'], map_id['Essen_Dortmund'], map_id['Essen_Aachen'],
                map_id['Essen_Muenster'], map_id['Essen_Koblenz'], map_id['Essen_Siegen'], map_id['Essen_Wesel']]

    @staticmethod
    def calculate_paths_for_demand(ant_environment: AntEnvironment, file_name=None):
        paths_for_demand = {}
        init_links = copy.deepcopy(ant_environment.links)
        for current_demand in ant_environment.demands.demands_map_id.values():
        # for current_demand in PathsForDemandProvider.__prepare_test_demands(ant_environment):
            ant_environment.current_demand = current_demand
            ant_environment.links = copy.deepcopy(init_links)
            first_path, second_path = PathGenerator.calculate_best_paths_for_demand(ant_environment, None, None)
            demand_paths = DemandPaths(first_path, second_path)
            paths_for_demand[current_demand.id] = demand_paths
        if file_name is not None:
            PathsForDemandProvider.__write_paths_for_demand_to_file(paths_for_demand, file_name)
        return paths_for_demand

    @staticmethod
    def __write_paths_for_demand_to_file(paths_for_demand, file_name):
        with open(file_name, mode="w") as csv_file:
            field_names = ['demand_id', 'first_path', 'second_path', 'cost1', 'cost2']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            csv_file.flush()

            for demand_id, demand_paths in paths_for_demand.items():
                writer.writerow({'demand_id': demand_id, 'first_path': demand_paths.first_path.path_to_string,
                                 'second_path': demand_paths.second_path.path_to_string,
                                 'cost1': demand_paths.first_path.cost, 'cost2': demand_paths.second_path.cost})
                csv_file.flush()

    @staticmethod
    def __prepare_ant_path_solution(reverted_path_to_string: str, ant_environment: AntEnvironment, desired_cost):
        reverted_path = reverted_path_to_string[1:].split("-")
        reverted_path.reverse()

        cost = 0
        path = []
        for link_id in reverted_path:
            link = ant_environment.links.links_map_id[link_id]
            cost = cost + link.cost
            path.append(link)

        solution = AntPathSolution()
        solution.path = path
        solution.cost = cost
        solution.path_to_string = reverted_path_to_string

        if int(desired_cost) != cost:
            raise Exception("Something went wrong in loading path", reverted_path_to_string, cost, desired_cost)

        return solution

    @staticmethod
    def load_paths_for_demand_from_file(ant_environment: AntEnvironment, file_name):
        paths_for_demand = {}
        with open(file_name, mode="r") as csv_file:
            field_names = ['demand_id', 'first_path', 'second_path', 'cost1', 'cost2']
            content = csv.DictReader(csv_file, fieldnames=field_names)

            for row in content:
                dict_row = dict(row)
                if dict_row['demand_id'] == 'demand_id':
                    continue
                first_solution = PathsForDemandProvider.__prepare_ant_path_solution(dict_row['first_path'], ant_environment, dict_row['cost1'])
                second_solution = PathsForDemandProvider.__prepare_ant_path_solution(dict_row['second_path'], ant_environment, dict_row['cost2'])
                paths_for_demand[dict_row['demand_id']] = DemandPaths(first_solution, second_solution)
        return paths_for_demand

import copy
import math
import random

from ants_algorithm.model.Ant import Ant
from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.AntPathSolution import AntPathSolution
from ants_algorithm.utils.EvaluationUtil import EvaluationUtil
from ants_algorithm.utils.PheromoneUtil import PheromoneUtil
from ants_algorithm.utils.SolutionsPrinter import SolutionsPrinter


class PathGenerator:

    @staticmethod
    def calculate_best_paths_for_demand(environment: AntEnvironment, path_x: AntPathSolution = None, writer=None, csv_file=None):
        ants = []
        for x in range(int(environment.ant_colony_size)):
            ants.append(Ant(environment.current_demand.source))
        for it in range(int(environment.iterations_number)):
            visited_links = []
            for ant in ants:
                move_ant = PathGenerator.__move_ant(ant, environment, path_x)
                if move_ant is not None:
                    visited_links.append(move_ant)

            PheromoneUtil.update_pheromones(it, visited_links, environment, path_x)
        first_solution, second_solution = PathGenerator.__find_two_best_solutions(ants)
        if first_solution.cost == 99999999 or second_solution.cost == 99999999:
            raise Exception("ERROR could not find two different solutions")
        # keys = list(environment.demands.demands_map_id.keys())
        # index = keys.index(environment.current_demand.id)
        # print(index + 1, '/', len(keys), environment.current_demand.source, environment.current_demand.target)
        print(SolutionsPrinter.print_cities(first_solution.path, environment))
        print(SolutionsPrinter.print_cities(second_solution.path, environment))
        # sorted_path_lengths = SolutionsPrinter.print_path_costs(ants)
        # SolutionsPrinter.print_paths_with_best_cost(ants, sorted_path_lengths, environment, writer, csv_file)
        # SolutionsPrinter.print_best_path_costs(ants)
        print('first best cost -', first_solution.cost, '\nsecond best cost -', second_solution.cost)
        return first_solution, second_solution

    @staticmethod
    def __move_ant(ant: Ant, environment: AntEnvironment, x_path: AntPathSolution = None):
        if ant.forward:
            if ant.current_node == environment.current_demand.source:
                ant.path_cost = 0
                ant.links_stack = []
            chosen_link_id = PathGenerator.__choose_link_id_by_probability(ant, environment)
            chosen_link = environment.links.links_map_id[chosen_link_id]
            ant.links_stack.append(chosen_link)
            ant.path_cost = ant.path_cost + chosen_link.cost
            if ant.current_node == chosen_link.source:
                ant.current_node = chosen_link.target
            elif ant.current_node == chosen_link.target:
                ant.current_node = chosen_link.source
            else:
                raise Exception("Error while moving forward ant!!!")
            if ant.current_node == environment.current_demand.target:
                ant.forward = False
            return

        else:
            if ant.current_node == environment.current_demand.target:
                PathGenerator.__remove_loops(ant, environment)
                PathGenerator.__remember_last_path_and_best_paths(ant, x_path, environment)
            last_link = ant.links_stack.pop()
            if ant.current_node == last_link.source:
                ant.current_node = last_link.target
            elif ant.current_node == last_link.target:
                ant.current_node = last_link.source
            else:
                raise Exception("Error while moving backward ant!!!")
            if ant.current_node == environment.current_demand.source and len(ant.links_stack) == 0:
                ant.forward = True
                ant.path_cost = 0

            return last_link.link_id

    @staticmethod
    # todo depricated
    def __choose_link_id(ant, environment):
        neighbours = environment.links.neighbours_links_map[ant.current_node]
        selection_links_list = []
        for neighbour in neighbours:
            if len(ant.links_stack) == 0 or neighbour.link_id != ant.links_stack[len(ant.links_stack) - 1].link_id:
                for i in range(environment.links.links_map_id[neighbour.link_id].pheromone + 1):
                    selection_links_list.append(neighbour.link_id)
        chosen_link_id = selection_links_list[random.randint(0, len(selection_links_list) - 1)]
        return chosen_link_id

    @staticmethod
    def __choose_link_id_by_probability(ant, environment):
        neighbours = environment.links.neighbours_links_map[ant.current_node]
        selection_links_range = 0
        for neighbour in neighbours:
            if len(ant.links_stack) == 0 or neighbour.link_id != ant.links_stack[len(ant.links_stack) - 1].link_id:
                selection_links_range = selection_links_range + math.pow(PathGenerator.__get_pheromone_value(environment, neighbour, ant), 2) + 1
        if selection_links_range == 0 and len(ant.links_stack) > 0:
            return ant.links_stack[len(ant.links_stack) - 1].link_id
        elif selection_links_range == 0:
            raise Exception("Graph is not consistent or has one node")

        selected_index = random.randint(0, selection_links_range - 1)
        iterator = 0
        for neighbour in neighbours:
            prev_value = iterator
            if len(ant.links_stack) == 0 or neighbour.link_id != ant.links_stack[len(ant.links_stack) - 1].link_id:
                iterator = iterator + math.pow(PathGenerator.__get_pheromone_value(environment, neighbour, ant), 2) + 1
                if prev_value <= selected_index < iterator:
                    return neighbour.link_id
        raise Exception("Error when choosing link")

    @staticmethod
    def __get_pheromone_value(environment: AntEnvironment, neighbour, ant: Ant):
        # TODO poprawić wydajność
        multiplier = 1
        # TODO
        # for link in ant.links_stack:
        #     if neighbour.link_id == link.link_id:
        #         multiplier = 0.1
        #         break

        return int(multiplier * environment.links.links_map_id[neighbour.link_id].pheromone)

    @staticmethod
    def __remember_last_path_and_best_paths(ant: Ant, x_path: AntPathSolution = None, environment: AntEnvironment = None):
        ant.last_solution.path = copy.deepcopy(ant.links_stack)
        ant.last_solution.cost = ant.path_cost
        ant.last_solution.evaluation = EvaluationUtil.evaluate(ant, x_path, environment)
        current_evaluation = ant.last_solution.evaluation
        best_solution1_evaluation = ant.best_solution.evaluation
        if current_evaluation < best_solution1_evaluation or current_evaluation == best_solution1_evaluation and \
                ant.last_solution.path_to_string != ant.best_solution.path_to_string and ant.last_solution.cost < ant.best_solution.cost:
            best_solution2_evaluation = ant.best_solution2.evaluation
            if best_solution1_evaluation < best_solution2_evaluation or best_solution1_evaluation == best_solution2_evaluation and \
                    ant.best_solution.path_to_string != ant.best_solution2.path_to_string and ant.best_solution.cost < ant.best_solution2.cost:
                ant.best_solution2.cost = ant.best_solution.cost
                ant.best_solution2.path = ant.best_solution.path
                ant.best_solution2.path_to_string = ant.best_solution.path_to_string
                ant.best_solution2.evaluation = ant.best_solution.evaluation
            ant.best_solution.cost = ant.last_solution.cost
            ant.best_solution.path = ant.last_solution.path
            ant.best_solution.path_to_string = ant.last_solution.path_to_string
            ant.best_solution.evaluation = ant.last_solution.evaluation

    @staticmethod
    def __remove_loops(ant: Ant, environment: AntEnvironment):
        current_path = ant.links_stack
        output_reversed_path = []
        new_cost = 0
        path_to_string = ""
        i = len(current_path) - 1
        while i >= 0:
            current_node = current_path[i]
            j = 0
            while j < i:
                if PathGenerator.__check_links_source_and_target(current_path, i, j) \
                        or current_path[i].source == environment.current_demand.source or current_path[i].target == environment.current_demand.source:
                    # usuwamy pętlę
                    i = j
                    break
                elif PathGenerator.__check_if_can_remove_redundant_links_between(current_path, i, j):
                    # usuwamy przejścia pośrednie, które są zbędne np gdy idziemy do jakiegoś node'a, a potem się cofamy
                    i = j + 1
                    break
                j = j + 1
            output_reversed_path.append(current_node)
            new_cost = new_cost + current_node.cost
            path_to_string = path_to_string + "-" + current_node.link_id
            i = i - 1
        ant.last_solution.path_to_string = path_to_string
        if len(output_reversed_path) < len(current_path):
            # print("loops removed was", len(current_path), "is", len(output_reversed_path))
            output_reversed_path.reverse()
            ant.links_stack = output_reversed_path
            ant.path_cost = new_cost

    @staticmethod
    # Sprawdzamy czy znaleziony link o tym samym id jest skierowany w tę samą stronę
    def __check_links_source_and_target(current_path, i, j):
        if current_path[i - 1].target == current_path[i].source or current_path[i - 1].source == current_path[i].source:
            i_source = current_path[i].source
            i_target = current_path[i].target
        else:
            i_source = current_path[i].target
            i_target = current_path[i].source

        if current_path[j].target == current_path[j + 1].source or current_path[j].target == current_path[j + 1].target:
            j_source = current_path[j].source
            j_target = current_path[j].target
        else:
            j_source = current_path[j].target
            j_target = current_path[j].source

        return i_source == j_source and i_target == j_target

    @staticmethod
    # Sprawdzamy czy znaleziony link o tym samym id jest skierowany w tę samą stronę
    def __check_if_can_remove_redundant_links_between(current_path, i, j):
        if current_path[i - 1].target == current_path[i].source or current_path[i - 1].source == current_path[i].source:
            i_source = current_path[i].source
            i_target = current_path[i].target
        else:
            i_source = current_path[i].target
            i_target = current_path[i].source

        if current_path[j].target == current_path[j + 1].source or current_path[j].target == current_path[j + 1].target:
            j_source = current_path[j].source
            j_target = current_path[j].target
        else:
            j_source = current_path[j].target
            j_target = current_path[j].source

        return i - j != 1 and (i_source == j_target or i_target == j_source)

    @staticmethod
    def __find_two_best_solutions(ants: []):
        first_solution = AntPathSolution()
        second_solution = AntPathSolution()
        for ant in ants:
            best_solution_evaluation = ant.best_solution.evaluation
            best_solution2_evaluation = ant.best_solution2.evaluation
            first_solution_evaluation = first_solution.evaluation
            second_solution_evaluation = second_solution.evaluation
            if best_solution_evaluation < first_solution_evaluation or best_solution_evaluation == first_solution_evaluation and \
                    ant.best_solution.cost < first_solution.cost:
                if first_solution_evaluation < second_solution_evaluation or first_solution_evaluation == second_solution_evaluation and \
                    first_solution.cost < second_solution.cost:
                    second_solution.cost = first_solution.cost
                    second_solution.path = first_solution.path
                    second_solution.path_to_string = first_solution.path_to_string
                    second_solution.evaluation = first_solution.evaluation
                first_solution.cost = ant.best_solution.cost
                first_solution.path = ant.best_solution.path
                first_solution.path_to_string = ant.best_solution.path_to_string
                first_solution.evaluation = ant.best_solution.evaluation
            elif best_solution2_evaluation < first_solution_evaluation or best_solution2_evaluation == first_solution_evaluation and \
                    ant.best_solution2.cost < first_solution.cost:
                if first_solution_evaluation < second_solution_evaluation or first_solution_evaluation == second_solution_evaluation and \
                    first_solution.cost < second_solution.cost:
                    second_solution.cost = first_solution.cost
                    second_solution.path = first_solution.path
                    second_solution.path_to_string = first_solution.path_to_string
                    second_solution.evaluation = first_solution.evaluation
                first_solution.cost = ant.best_solution2.cost
                first_solution.path = ant.best_solution2.path
                first_solution.path_to_string = ant.best_solution2.path_to_string
                first_solution.evaluation = ant.best_solution2.evaluation

            if ant.best_solution.path_to_string != first_solution.path_to_string and best_solution_evaluation < second_solution_evaluation or \
                    ant.best_solution.path_to_string != first_solution.path_to_string and best_solution_evaluation == second_solution_evaluation and ant.best_solution.cost < second_solution.cost:
                second_solution.cost = ant.best_solution.cost
                second_solution.path = ant.best_solution.path
                second_solution.path_to_string = ant.best_solution.path_to_string
                second_solution.evaluation = ant.best_solution.evaluation
            elif ant.best_solution2.path_to_string != first_solution.path_to_string and best_solution2_evaluation < second_solution_evaluation or \
                    ant.best_solution2.path_to_string != first_solution.path_to_string and best_solution2_evaluation == second_solution_evaluation and ant.best_solution2.cost < second_solution.cost:
                second_solution.cost = ant.best_solution2.cost
                second_solution.path = ant.best_solution2.path
                second_solution.path_to_string = ant.best_solution2.path_to_string
                second_solution.evaluation = ant.best_solution2.evaluation

            if first_solution.path_to_string == second_solution.path_to_string:
                raise Exception("ERROR find_two_best_solutions two best paths should never be the same")
        return first_solution, second_solution

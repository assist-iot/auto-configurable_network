import copy

from networkx import DiGraph

from OutputObject import OutputObject
from ants_algorithm.generators.PathGenerator import PathGenerator
from ants_algorithm.model.ProbableXYSolution import ProbableXYSolution
from ants_algorithm.utils.EnvironmentProvider import EnvironmentProvider


class EventProcessor:

    @staticmethod
    def process(graph: DiGraph, source, target, event_demand_value):
        print("proces")
        env = EnvironmentProvider.prepare_env_from_graph(graph, source, target, event_demand_value)
        init_links = copy.deepcopy(env.links)
        out_object = OutputObject(env, init_links)
        if source < target:
            demand_event = str(source) + "_" + str(target)
        else:
            demand_event = str(target) + "_" + str(source)

        EventProcessor.__process_event(demand_event, event_demand_value, out_object)

        print()

        return [EventProcessor.__prepare_nodes(env, out_object.ant_environment.paths_for_demands[demand_event].x.path),
                EventProcessor.__prepare_nodes(env, out_object.ant_environment.paths_for_demands[demand_event].y.path)]

    @staticmethod
    def __prepare_nodes(env, path):
        current_node = env.current_demand.source
        nodes = [current_node]
        for node in path:
            if node.source == current_node:
                nodes.append(node.target)
                current_node = node.target
            else:
                nodes.append(node.source)
                current_node = node.source
        return nodes

    @staticmethod
    def __find_paths_for_demand(demand, demand_value, output_object: OutputObject):
        ant_environment = output_object.ant_environment
        cur_demand = ant_environment.demands.demands_map_id[demand]
        cur_demand.value = demand_value
        ant_environment.current_demand = copy.copy(cur_demand)
        ant_environment.current_demand.source = ant_environment.source
        ant_environment.current_demand.target = ant_environment.target
        ant_environment.links = copy.deepcopy(output_object.init_links)
        print(f'source: {ant_environment.current_demand.source}, target:{ant_environment.current_demand.target}')
        print(f'demand value:{ant_environment.current_demand.value}')
        print('Calculating X1 and X2')
        x1, x2 = PathGenerator.calculate_best_paths_for_demand(ant_environment)
        ant_environment.links = copy.deepcopy(output_object.init_links)
        print('Calculating Y1 and Y2 for X1')
        y1, y2 = PathGenerator.calculate_best_paths_for_demand(ant_environment, x1)
        ant_environment.links = copy.deepcopy(output_object.init_links)
        print('Calculating Y3 and Y4 for X2')
        y3, y4 = PathGenerator.calculate_best_paths_for_demand(ant_environment, x2)

        x_y_pairs = [ProbableXYSolution(x1, y1, cur_demand.value), ProbableXYSolution(x1, y2, cur_demand.value),
                     ProbableXYSolution(x2, y3, cur_demand.value), ProbableXYSolution(x2, y4, cur_demand.value)]

        best_x_y_solution = EventProcessor.__find_best_x_y_solution_with_losses(x_y_pairs, ant_environment)

        for link in best_x_y_solution.x.path:
            ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[
                                                                   link.link_id] + cur_demand.value

        output_object.solution_path = best_x_y_solution.x

        ant_environment.paths_for_demands[demand] = best_x_y_solution

        # paths_for_demand = PathsForDemandProvider.calculate_paths_for_demand(ant_environment, results_csv)
        # paths_for_demand = PathsForDemandProvider.load_paths_for_demand_from_file(ant_environment, results_csv)
        # PBILr algorithm
        # evolution_environment = EvolutionEnvironment(ant_environment.links, ant_environment.demands, paths_for_demand)
        # EvolutionAlgorithm.calculate(evolution_environment)
        # greedy algoritm
        # GreedyAlgorithm.calculate(ant_environment, paths_for_demand)
        print()

    @staticmethod
    def __find_best_x_y_solution(x_y_pairs, ant_environment):
        min_weighted_sum = 99999999
        best_x_y_solution = None
        for x_y_pair in x_y_pairs:
            x_factor = ant_environment.alpha * len(x_y_pair.x.path)
            y_factor = 1
            for y_link in x_y_pair.y.path:
                y_link_load = ant_environment.links_usage_values[y_link.link_id]
                y_usage_percent = y_link_load / y_link.capacity
                if y_usage_percent > 1:
                    print(y_link.link_id, "link is overloaded:", y_usage_percent)
                if y_usage_percent >= 0.99:
                    y_usage_percent = 0.98999
                y_factor = y_factor * (1 / (0.99 - y_usage_percent))
            y_factor = ant_environment.beta * y_factor

            x_y_pair.weighted_sum = x_factor + y_factor
            if x_y_pair.weighted_sum < min_weighted_sum:
                min_weighted_sum = x_y_pair.weighted_sum
                best_x_y_solution = x_y_pair
        return best_x_y_solution

    def __find_best_x_y_solution_with_losses(x_y_pairs, ant_environment):
        min_weighted_sum = 99999999
        best_x_y_solution = None
        for x_y_pair in x_y_pairs:
            x_factor = ant_environment.alpha * len(x_y_pair.x.path)
            y_factor = 1
            z_factor = 1
            d_factor = 1
            print("CO JEST")
            for y_link in x_y_pair.y.path:
                y_link_load = ant_environment.links_usage_values[y_link.link_id]
                y_usage_percent = y_link_load / y_link.capacity
                y_link_loss = ant_environment.links_losses[y_link.link_id] #MR
                y_loss_tmp = y_link_loss / 100 #MR
                y_link_delay = ant_environment.links_delays[y_link.link_id] / 100 #MR
                if y_usage_percent > 1:
                    print(y_link.link_id, "link is overloaded:", y_usage_percent)
                if y_usage_percent >= 0.99:
                    y_usage_percent = 0.98999
                y_factor = y_factor * (1 / (0.99 - y_usage_percent))
                z_factor = z_factor * (1 / (0.99 - y_loss_tmp))
                d_factor = d_factor * (1 / (0.99 - y_link_delay))
                d_factor = max(0, d_factor)

                print("CO JEST")
            y_factor = ant_environment.beta * y_factor
            z_factor = ant_environment.beta * z_factor
            d_factor = ant_environment.beta * d_factor

            x_y_pair.weighted_sum = x_factor + (y_factor + z_factor + d_factor)/3
            if x_y_pair.weighted_sum < min_weighted_sum:
                min_weighted_sum = x_y_pair.weighted_sum
                best_x_y_solution = x_y_pair
        return best_x_y_solution

    @staticmethod
    def __process_event(demand_event, demand_value, out_object):
        print(out_object)
        if demand_event in out_object.ant_environment.paths_for_demands:
            print(f"demand={demand_event} was already calculated. It is in paths_for_demands")
            prob_solution = out_object.ant_environment.paths_for_demands[demand_event]
            ant_environment = out_object.ant_environment
            cur_demand = ant_environment.demands.demands_map_id[demand_event]
            cur_demand.value = demand_value
            ant_environment.current_demand = cur_demand
            new_demand_value = prob_solution.demand_value + cur_demand.value
            if prob_solution.chosen_path_x:
                # wcześniej demand był przesyłany ścieżką x
                can_x_be_extended = True
                for link in prob_solution.x.path:
                    if (ant_environment.links_usage_values[link.link_id] + cur_demand.value) / link.capacity > 0.9:
                        can_x_be_extended = False
                        break
                if can_x_be_extended:
                    # przesyłamy większy demand ścieżką x, bo nie przekracza obciążenia 90%
                    for link in prob_solution.x.path:
                        ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[
                                                                               link.link_id] \
                                                                           + cur_demand.value
                    prob_solution.demand_value = new_demand_value
                    prob_solution.chosen_path_x = True
                    out_object.solution_path = prob_solution.x
                else:
                    # usuwamy starą przesyłaną wartość ze ścieżki x bo się nie mieści nowa
                    for link in prob_solution.x.path:
                        ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[
                                                                               link.link_id] \
                                                                           - prob_solution.demand_value
                    can_y_be_used = True
                    for link in prob_solution.y.path:
                        if ant_environment.links_usage_values[link.link_id] + new_demand_value > link.capacity:
                            can_y_be_used = False
                            break
                    if can_y_be_used:
                        # da się przesłać y więc przesyłamy ścieżką y
                        for link in prob_solution.y.path:
                            ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[
                                                                                   link.link_id] \
                                                                               + new_demand_value
                        prob_solution.demand_value = new_demand_value
                        prob_solution.chosen_path_x = False
                        out_object.solution_path = prob_solution.y
                    else:
                        # nie da się przesłać nowej wartości ani ścieżką x ani y, więc wyznaczamy nowe
                        EventProcessor.__find_paths_for_demand(demand_event, new_demand_value, out_object)
            else:
                # wcześniej demand był przesyłany ścieżką y
                # usuwamy starą przesyłaną wartość ze ścieżki y
                for link in prob_solution.y.path:
                    ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[link.link_id] \
                                                                       - prob_solution.demand_value
                # sprawdzamy czy da się przesłać całe nowe zapotrzebowanie ścieżką x
                can_x_be_used = True
                for link in prob_solution.x.path:
                    if (ant_environment.links_usage_values[link.link_id] + new_demand_value) / link.capacity > 0.9:
                        can_x_be_used = False
                        break
                if can_x_be_used:
                    # da się przesłać ścieżką x
                    for link in prob_solution.x.path:
                        ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[
                                                                               link.link_id] \
                                                                           + new_demand_value
                    prob_solution.demand_value = new_demand_value
                    prob_solution.chosen_path_x = True
                    out_object.solution_path = prob_solution.x
                else:
                    # sprawdzamy czy da się przesłać całe nowe zapotrzebowanie ścieżką y
                    can_y_be_used = True
                    for link in prob_solution.y.path:
                        if ant_environment.links_usage_values[link.link_id] + new_demand_value > link.capacity:
                            can_y_be_used = False
                            break
                    if can_y_be_used:
                        # da się przesłać y więc przesyłamy ścieżką y
                        for link in prob_solution.y.path:
                            ant_environment.links_usage_values[link.link_id] = ant_environment.links_usage_values[
                                                                                   link.link_id] \
                                                                               + new_demand_value
                        prob_solution.demand_value = new_demand_value
                        prob_solution.chosen_path_x = False
                        out_object.solution_path = prob_solution.y
                    else:
                        # nie da się przesłać nowej wartości ani ścieżką x ani y, więc wyznaczamy nowe
                        EventProcessor.__find_paths_for_demand(demand_event, new_demand_value, out_object)
        else:
            print(f"Calculating new paths for demand={demand_event}")
            EventProcessor.__find_paths_for_demand(demand_event, demand_value, out_object)

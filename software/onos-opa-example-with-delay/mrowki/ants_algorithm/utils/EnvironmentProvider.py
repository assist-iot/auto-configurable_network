import getopt
import sys

from networkx import DiGraph

from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.Demands import Demands, Demand
from ants_algorithm.model.Links import NeighbourLink, Link, Links
from ants_algorithm.utils.InputFileParser import InputFileParser


class EnvironmentProvider:

    @staticmethod
    def prepare_env_from_graph(graph: DiGraph, source, target, event_demand_value):
        print(f'Processing graph=[nodes={graph.nodes}, edges={graph.edges}], source={source}, target={target}, demand_value={event_demand_value}')
        links, links_usage_values = EnvironmentProvider.__prepare_links_and_links_usage_values(graph)
        print(f'Created links={links}\nlinks_usage_values={links_usage_values}')

        demand_map = {(str(source), str(target)): {'demand_value': int(event_demand_value), 'path_x': [], 'path_y': []}}
        demands = EnvironmentProvider.__prepare_demands(demand_map)
        print(f'Created demands={demands}')
        env = AntEnvironment(links, demands)
        env.links_usage_values = links_usage_values
        env.paths_for_demands = {}  # TODO póki co ustawiam pustą, żeby przypadkiem nie pamiętać wcześniej wyliczonych ścieżek
        env.source = str(source)
        env.target = str(target)

        env.alpha = 0.5
        env.beta = 0.5

        return env

    @staticmethod
    def prepare_environment():
        xml_file = getopt.getopt(sys.argv[1], "")[1]
        max_link_capacity = int(getopt.getopt(sys.argv[4], "")[1])
        env = InputFileParser.parse(xml_file, max_link_capacity)
        if len(sys.argv) > 5:
            ant_colony_size = getopt.getopt(sys.argv[5], "")[1]
            env.ant_colony_size = ant_colony_size
        if len(sys.argv) > 6:
            iterations_number = getopt.getopt(sys.argv[6], "")[1]
            env.iterations_number = iterations_number
        # env.demand_source_target.append(["Regensburg", "Saarbruecken"])
        # SourceTargetGenerator.generate_all_demands(env)
        return env

    @staticmethod
    def __prepare_links_and_links_usage_values(graph: DiGraph):
        new_links = Links()
        links_usage_values = {}
        for key, value in graph.edges.items():
            link_first_node, link_second_node = key
            link_first_node = str(link_first_node)
            link_second_node = str(link_second_node)
            bandwidth = value['bandwidth']
            used_bandwidth = value['used_bandwidth']
            if link_first_node < link_second_node:
                link_id = str(link_first_node) + "_" + str(link_second_node)
                new_link = Link(link_id, link_first_node, link_second_node, 1, bandwidth)
            else:
                link_id = str(link_second_node) + "_" + str(link_first_node)
                new_link = Link(link_id, link_second_node, link_first_node, 1, bandwidth)
            new_links.links_map_id[link_id] = new_link
            neighbour_for_first = NeighbourLink(link_id, link_second_node, 1)
            neighbour_for_second = NeighbourLink(link_id, link_first_node, 1)
            if link_first_node not in new_links.neighbours_links_map:
                new_links.neighbours_links_map[link_first_node] = [neighbour_for_first]
            else:
                new_links.neighbours_links_map[link_first_node].append(neighbour_for_first)

            if link_second_node not in new_links.neighbours_links_map:
                new_links.neighbours_links_map[link_second_node] = [neighbour_for_second]
            else:
                new_links.neighbours_links_map[link_second_node].append(neighbour_for_second)

            links_usage_values[link_id] = used_bandwidth
        return new_links, links_usage_values

    @staticmethod
    def __prepare_demands(demand_map):
        new_demands = Demands()
        for key, value in demand_map.items():
            demand_source, demand_target = key
            demand_source = str(demand_source)
            demand_target = str(demand_target)
            demand_value = value['demand_value']
            if demand_source < demand_target:
                demand_id = str(demand_source) + "_" + str(demand_target)
                new_demand = Demand(demand_id, demand_source, demand_target, demand_value)
            else:
                demand_id = str(demand_target) + "_" + str(demand_source)
                new_demand = Demand(demand_id, demand_target, demand_source, demand_value)
            new_demands.demands_map_id[demand_id] = new_demand
        return new_demands

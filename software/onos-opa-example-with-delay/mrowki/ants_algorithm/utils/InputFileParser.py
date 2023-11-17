import xml.etree.ElementTree as eT

from ants_algorithm.model.AntEnvironment import AntEnvironment
from ants_algorithm.model.Demands import Demands, Demand
from ants_algorithm.model.Links import Links, Link, NeighbourLink


class InputFileParser:

    @staticmethod
    def parse(file_path, max_link_capacity):
        root = eT.parse(file_path).getroot()

        new_links = InputFileParser.__parse_links(root, max_link_capacity)
        new_demands = InputFileParser.__parse_demands(root)

        environment = AntEnvironment(new_links, new_demands)

        return environment

    @staticmethod
    def __parse_links(root, max_link_capacity):
        new_links = Links()
        for link in root.iter('link'):
            link_id = link.attrib['id']
            link_first_node = link.find('source').text
            link_second_node = link.find('target').text
            additional_module = link.find('additionalModules')[0]
            # cost = int(float(additional_module.find('cost').text))
            cost = 1
            # capacity = int(float(additional_module.find('capacity').text))
            capacity = max_link_capacity
            new_link = Link(link_id, link_first_node, link_second_node, cost, capacity)
            neighbour_for_first = NeighbourLink(link_id, link_second_node, cost)
            neighbour_for_second = NeighbourLink(link_id, link_first_node, cost)
            new_links.links_map_id[link_id] = new_link
            if link_first_node not in new_links.neighbours_links_map:
                new_links.neighbours_links_map[link_first_node] = [neighbour_for_first]
            else:
                new_links.neighbours_links_map[link_first_node].append(neighbour_for_first)

            if link_second_node not in new_links.neighbours_links_map:
                new_links.neighbours_links_map[link_second_node] = [neighbour_for_second]
            else:
                new_links.neighbours_links_map[link_second_node].append(neighbour_for_second)
        return new_links

    @staticmethod
    def __parse_demands(root):
        new_demands = Demands()
        for link in root.iter('demand'):
            demand_id = link.attrib['id']
            demand_source = link.find('source').text
            demand_target = link.find('target').text
            demand_value = int(float(link.find('demandValue').text))
            new_demand = Demand(demand_id, demand_source, demand_target, demand_value)
            new_demands.demands_map_id[demand_id] = new_demand

        return new_demands

class AntEnvironment:
    demand_source_target = []
    current_demand = None
    source = None
    target = None
    ant_colony_size = 50
    iterations_number = 100
    pheromone_increment = 10
    pheromone_decrement = 3
    capacity_extensions = [50, 100, 200]
    paths_for_demands = {}
    alpha = None
    beta = None

    def __init__(self, links, demands):
        self.links = links
        self.demands = demands
        self.capacities_extended = {}
        self.links_usage_values = {}
        self.links_losses = {}
        self.links_delays = {}
        for link_id in links.links_map_id.keys():
            self.links_usage_values[link_id] = 0
            self.links_losses[link_id] = 0
            self.links_delays[link_id] = 0


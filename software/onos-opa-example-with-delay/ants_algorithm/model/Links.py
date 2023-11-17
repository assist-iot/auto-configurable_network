class Links:
    def __init__(self):
        self.links_map_id = {}
        self.neighbours_links_map = {}

    def __str__(self) -> str:
        nl = "\n"
        return f"[links_map_id: \n{nl.join(map(lambda x: str(x), self.links_map_id.values()))}\n" \
               f"neighbours_links_map: \n{nl.join(map(lambda neighbour_list: ' '.join(map(lambda neighbour: str(neighbour), neighbour_list)), self.neighbours_links_map.values()))}]"


class Link:

    def __init__(self, link_id, source, target, cost, capacity):
        self.link_id = link_id
        self.source = source
        self.target = target
        self.cost = cost
        self.capacity = capacity
        self.pheromone = 0

    def __str__(self) -> str:
        return f"[link_id: {self.link_id}, pheromone: {str(self.pheromone)}, cost={self.cost}, capacity={self.capacity}]"


class NeighbourLink:

    def __init__(self, link_id, neighbour, cost):
        self.link_id = link_id
        self.neighbour = neighbour
        self.cost = cost

    def __str__(self) -> str:
        return f"[link_id: {self.link_id}, neighbour: {str(self.neighbour)}, cost={self.cost}]"

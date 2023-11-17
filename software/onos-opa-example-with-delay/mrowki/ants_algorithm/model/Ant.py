from ants_algorithm.model.AntPathSolution import AntPathSolution


class Ant:

    def __init__(self, current_node):
        self.current_node = current_node
        self.links_stack = []
        self.path_cost = 0
        self.forward = True
        self.last_solution = AntPathSolution()
        self.best_solution = AntPathSolution()
        self.best_solution2 = AntPathSolution()

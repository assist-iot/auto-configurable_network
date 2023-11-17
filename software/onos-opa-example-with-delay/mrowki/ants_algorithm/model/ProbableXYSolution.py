class ProbableXYSolution:

    def __init__(self, x, y, demand_value):
        self.x = x
        self.y = y
        self.demand_value = demand_value
        self.chosen_path_x = True
        self.weighted_sum = 99999999

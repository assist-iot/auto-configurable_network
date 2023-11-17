class InputObject:

    def __init__(self, demand_id, alpha=None, beta=None):
        self.demand_id = demand_id
        if alpha is None:
            self.alpha = 0.5
        else:
            self.alpha = alpha
        if beta is None:
            self.beta = 0.5
        else:
            self.beta = beta


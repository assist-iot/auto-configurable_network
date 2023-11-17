class Demands:
    def __init__(self):
        self.demands_map_id = {}

    def __str__(self) -> str:
        nl = "\n"
        return f"[demands_map_id: {nl.join(map(lambda x: str(x), self.demands_map_id.values()))}]"


class Demand:
    def __init__(self, id, source, target, value):
        self.id = id
        self.source = source
        self.target = target
        self.value = value

    def __str__(self) -> str:
        return f"[demand_id: {self.id}, source={self.source}, target={self.target}, value={self.value}]"

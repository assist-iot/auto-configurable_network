class SingleLine:

    def __init__(self, name, reachability, avg_del):
        self.link_name = name
        name = name.replace(">", "")
        names = name.split("-")
        self.src_name = names[0]
        self.dst_name = names[1]
        self.reachability = reachability
        self.average_delay = avg_del


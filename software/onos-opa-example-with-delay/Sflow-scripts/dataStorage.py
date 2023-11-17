class Switch:
    def __init__(self, if_name, agent_sub_id):
        self.ifName = if_name
        self.agentSubId = agent_sub_id
        self.flows = []

    def add_flow(self, flow):
        self.flows.append(flow)

    def add_bytes_to_flow(self, src_ip, dst_ip, bytes_reg):
        for flow in self.flows:
            if src_ip == flow.src_ip and dst_ip == flow.dst_ip:
                flow.bytes_registered += float(bytes_reg)
                return

        self.flows.append(Flow(src_ip, dst_ip, bytes_reg))  # jesli doszlo do tego miejsca to flowa trzeba utworzyc i dodac

    def print_switch(self):
        print("IfName: {}\nAgentSubId:{}".format(self.ifName, self.agentSubId))
        for flow in self.flows:
            print("SrcIP: {}\nDstIP: {}\nBytesReg: {}".format(flow.src_ip, flow.dst_ip, flow.bytes_registered))
        print("\n")


class Flow:
    def __init__(self, src_ip, dst_ip, bytes_reg):
        self.id = src_ip + "-" + dst_ip
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.bytes_registered = float(bytes_reg)

    def add_bytes(self, bytes_reg):
        self.bytes_registered += float(bytes_reg)

import numpy as np

class Observation():

	# Return minimal ratio of available bandwidth on edge to maximum bandwidth in network
	def get_capacity_ratio(self, ports, active, mutual, links_capacity, tx_bandwidth, bw_tx):
		
		tmp = {}
		#print("porty:")
		#print(ports)
		for port in ports:
			if port in mutual and not active:
				tmp[port] = links_capacity[port] - tx_bandwidth[port] + bw_tx
			else:
				tmp[port] = links_capacity[port] - tx_bandwidth[port]
		#print("tu sa tmpy")
		#print(tmp)
		#print(tmp.get)
		bottleneck = min(tmp, key=tmp.get)
		return tmp[bottleneck] if tmp[bottleneck] >= 0.0 else 0.0, bottleneck

	# Return the percentage of edge bandwidth used by demand
	def get_occupany_percentage(self, active, bw_tx, mutual, edge_capacity, capacity_ratio, bottleneck):
		edge = edge_capacity - capacity_ratio
		if edge:
			if active or bottleneck in mutual:
				occupancy_perc = bw_tx/edge
			else: 
				occupancy_perc = bw_tx/(bw_tx+edge)
		else:
			occupancy_perc = 1.0
		
		return round(occupancy_perc, 5) if occupancy_perc <= 1.0 else 1.0
	# Return ratio of transmitted bandwidth to end host and order bandwidth of demand
	def get_path_efficiency(self, bw_tx, order_bandwidth):
		path_efficiency = bw_tx/order_bandwidth
		return round(path_efficiency, 5) if path_efficiency <= 1.0 else 1.0

	def get_potential_efficiency(self, capacity_ratio, order_bandwidth):
		potential_efficiency = capacity_ratio/order_bandwidth
		return round(potential_efficiency, 5) if potential_efficiency <= 1.0 else 1.0

	# Return observation for agent
	def get_all(self, tx_bandwidth, ports_first, ports_second, order_bandwidth, 
		links_capacity, end_port, mutual, max_bps):
		"""Return observation for given values.
        Parameters
        ----------
        tx_bandwidth : list
            List of transmitted bandwith for every interface/port in network.
		ports_first : list
        	List of indexes referring to the "tx_bandwidth" variable about 
        	through which interfaces the chosen (actual) path passes.
        ports_second : list 
			List of indexes referring to the "tx_bandwidth" variable about 
        	through which interfaces the second (inactive) path passes.
        order_bandwidth : float
			Value of the ordered bandwidth for this demand. Specified in Mb.
        links_capacity : list
        	The capacity of the links/interfaces. Is sorted the same way as "tx_bandwidth" list. 
        end_port : int
        	Index which reffer to "tx_bandwidth" list about interface which transmit 
        	date to destination host
        mutual : list
			List of indexes referring to the "tx_bandwidth" variable about 
			interfaces mutual for both path
        max_bps : 
        	Maximal link capacity in network. Specified in Mb.
        """
		obs = []
		
		capacity_ratio, bottleneck = self.get_capacity_ratio(ports_first, True, 
			[], links_capacity/max_bps, tx_bandwidth, tx_bandwidth[end_port])
		
		potencial_capacity_ratio, potencial_bottleneck = self.get_capacity_ratio(ports_second, False, 
			mutual, links_capacity/max_bps, tx_bandwidth, tx_bandwidth[end_port])
		
		# Ratio of efficiency on actual path
		obs.append(self.get_path_efficiency(tx_bandwidth[end_port], order_bandwidth/max_bps))
		# Ratio of potencial efficiency on second path
		obs.append(self.get_potential_efficiency(potencial_capacity_ratio, order_bandwidth/max_bps))
		# Edge occupancy percentage on active path
		obs.append(self.get_occupany_percentage(True, tx_bandwidth[end_port], mutual,
			links_capacity[bottleneck]/max_bps, capacity_ratio, bottleneck))
		# Edge occupancy percentage on inactive path
		obs.append(self.get_occupany_percentage(False, tx_bandwidth[end_port], mutual,
			links_capacity[potencial_bottleneck]/max_bps, potencial_capacity_ratio, potencial_bottleneck))

		return obs
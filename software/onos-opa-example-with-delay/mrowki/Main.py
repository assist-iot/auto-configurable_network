from networkx import DiGraph

from events.EventProcessor import EventProcessor

if __name__ == '__main__':
    nodes = ['of:0000000000000003', 'of:0000000000000004', 'of:0000000000000001', 'of:0000000000000002', 'of:0000000000000007', 'of:0000000000000008', 'of:0000000000000005', 'of:0000000000000006', '16:BE:60:14:86:82/None', '8A:FB:1F:85:32:C8/None', '2E:6C:79:76:F1:F2/None', '2E:F6:94:B2:A5:9D/None', 'C2:B1:06:BE:E7:ED/None', 'C6:51:CF:E1:2F:FB/None']
    edges = [('of:0000000000000003', 'of:0000000000000002', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000003', 'of:0000000000000006', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000003', 'of:0000000000000008', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000003', 'of:0000000000000004', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000003', '8A:FB:1F:85:32:C8/None', {'bandwidth': 500000000.0, 'used_bandwidth': 0}),
             ('of:0000000000000003', '2E:6C:79:76:F1:F2/None', {'bandwidth': 500000000.0, 'used_bandwidth': 0}),
             ('of:0000000000000003', '2E:F6:94:B2:A5:9D/None', {'bandwidth': 500000000.0, 'used_bandwidth': 0}),
             ('of:0000000000000004', 'of:0000000000000002', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000001', 'of:0000000000000005', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000001', 'of:0000000000000007', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000001', 'of:0000000000000002', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000001', '16:BE:60:14:86:82/None', {'bandwidth': 500000000.0, 'used_bandwidth': 0}),
             ('of:0000000000000001', 'C2:B1:06:BE:E7:ED/None', {'bandwidth': 500000000.0, 'used_bandwidth': 0}),
             ('of:0000000000000001', 'C6:51:CF:E1:2F:FB/None', {'bandwidth': 500000000.0, 'used_bandwidth': 0}),
             ('of:0000000000000007', 'of:0000000000000008', {'bandwidth': 50000, 'used_bandwidth': 0}),
             ('of:0000000000000005', 'of:0000000000000006', {'bandwidth': 50000, 'used_bandwidth': 0})]
    # edges = [(1, 2, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (1, 7, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (2, 3, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (2, 6, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (3, 4, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (3, 5, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (4, 5, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (5, 6, {'bandwidth': 50000, 'used_bandwidth': 0}),
    #          (6, 7, {'bandwidth': 50000, 'used_bandwidth': 0})]
    example_graph = DiGraph()
    example_graph.add_nodes_from(nodes)
    example_graph.add_edges_from(edges)

    # argumenty: graf (typu DiGraph), źródło, ujście, wartość nowego zapotrzebowania
    paths = EventProcessor.process(example_graph, '2E:6C:79:76:F1:F2/None', '16:BE:60:14:86:82/None', 30000)
    print(paths)

# if __name__ == '__main__':
#     if len(sys.argv) < 4:
#         print("Please type arguments: \n - input file name \n - demand id \n - demand value delta (increment) \n - max link capacity \n - (optional) ant colony size (default 50) \n - (optional) iterations number (default 100)")
#         exit(-1)
#     environment = prepare_environment()
#     demand_event = getopt.getopt(sys.argv[2], "")[1]
#     # różnica między nową wartością zapotrzebowania a starą wartością, musi być dodatnia
#     demand_value = int(getopt.getopt(sys.argv[3], "")[1])
#
#     input_object = InputObject(demand_event)
#     environment.alpha = input_object.alpha
#     environment.beta = input_object.beta
#
#     results_csv = "output_files/result.csv"
#     init_links = copy.deepcopy(environment.links)
#
#     out_object = OutputObject(environment, init_links)
#
#     # demand_events = ["Muenchen_Regensburg", "Muenchen_Augsburg", "Ulm_Wuerzburg", "Ulm_Augsburg", "Karlsruhe_Augsburg", "Stuttgart_Konstanz"]
#     #
#     # for demand_event in demand_events:
#     while True:
#         EventProcessor.process_event(demand_event, demand_value, out_object)
#     print()

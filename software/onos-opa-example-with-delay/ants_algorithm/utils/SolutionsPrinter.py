
class SolutionsPrinter:

    @staticmethod
    def print_path_costs(ants_list):
        path_lengths = set()
        for ant1 in ants_list:
            path_lengths.add(ant1.last_solution.cost)
        path_lengths = sorted(path_lengths)
        for path_length in path_lengths:
            print('cost', path_length, '-', sum(map(lambda y: y.last_solution.cost == path_length, ants_list)), 'ants')
        return path_lengths

    @staticmethod
    def print_best_path_costs(ants_list):
        path_lengths = set()
        for ant1 in ants_list:
            path_lengths.add(ant1.best_solution.cost)
        path_lengths = sorted(path_lengths)
        for path_length in path_lengths:
            print('best cost ever found', path_length, '-',
                  sum(map(lambda y: y.best_solution.cost == path_length, ants_list)), 'ants')

    @staticmethod
    def print_cities(path: [], env):
        current_city = env.current_demand.source
        cities = current_city
        for node in path:
            if node.source == current_city:
                cities = cities + ' - ' + node.target
                current_city = node.target
            else:
                cities = cities + ' - ' + node.source
                current_city = node.source
        return cities

    @staticmethod
    def print_paths_with_best_cost(ants_list, sorted_path_lens, env, writer, csv_file):
        best_paths = {}
        iterator = 0
        limit = 3
        while len(best_paths) != limit and iterator != len(sorted_path_lens):
            for curr_ant in ants_list:
                if curr_ant.last_solution.cost == sorted_path_lens[iterator]:
                    if curr_ant.last_solution.path_to_string not in best_paths:
                        best_paths[curr_ant.last_solution.path_to_string] = curr_ant.last_solution.path
                if len(best_paths) == limit:
                    break
            iterator = iterator + 1

        for best_path in best_paths:
            cities = SolutionsPrinter.print_cities(best_paths[best_path], env)
            print("cost", len(best_paths[best_path]), ":", cities, "\nreversed links:", best_path)
            writer.writerow(
                {'source': env.current_demand.source, 'target': env.current_demand.target, 'cost': len(best_paths[best_path]), 'path': cities})
            csv_file.flush()

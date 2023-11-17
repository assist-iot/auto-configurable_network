import singleLine
from time import sleep


def split_line(line):
    line_components = line.split(' ')
    name = line_components[1][:-1]
    delays = line_components[5]
    divided_delays = delays.split('/')
    avg_delay = divided_delays[1]
    reachability = True
    if float(avg_delay) == 0:
        reachability = False

    return singleLine.SingleLine(name=name, reachability=reachability, avg_del=avg_delay)


def print_delays(single_lines_list, headers_printed, host_switch_dict, switches_list, links_dict):

    if not headers_printed:
        for key in links_dict.keys():           # printowanie nazw portow
            print("\t\t{}\t\t\t\t".format(key), end='')
            print("\t\t{}\t\t\t\t".format(links_dict[key]), end='')
        print('')

        counter = 2*len(links_dict.keys())
        for i in range(0, counter):                # printowanie KB's in/out
            print("KB/s in\t\tKB/s out\t", end='')
        print('')

    for key in links_dict.keys():               # lecimy po wszystkich linkach
        src_switch = key[:3]                    # tlumaczymy src i dst linka na hosty
        dst_switch = links_dict[key][:3]
        src_host = host_switch_dict[src_switch]
        dst_host = host_switch_dict[dst_switch]

        # todo zoptymalizowac
        for line in single_lines_list:          # szukamy wsrod wszystkich pomiarow pomiaru dla danego linka i printujemy go
            if line.src_name == src_host and line.dst_name == dst_host:
                print("{}\t{}\t".format(line.average_delay, line.average_delay), end='')
                print("{}\t{}\t".format(line.average_delay, line.average_delay), end='')
                break

    print('')

    # for line in single_lines_list:
    #     print("{}\t{}\t".format(line.average_delay, line.average_delay), end='')
    #     print("{}\t{}\t".format(line.average_delay, line.average_delay), end='')
    # print('')


def read_log_file(filename, iterations, host_switch_dict, switches_list, links_dict):
    headers_printed = False
    for j in range(0, iterations):
        my_file = open(filename, "r")
        lines = my_file.readlines()

        # przejście po wszystkich liniach, wychwycenie linii z *** results
        results_lines = []  # nry linii z *** results
        for i in range(0, len(lines)):
            lines[i] = lines[i][:-1]
            if lines[i] == "*** Results: ":
                results_lines.append(i)

        # bierzemy przedostatnie results i ucinamy wszystko przed
        startline = results_lines[len(results_lines) - 2]
        lines = lines[startline + 1:]

        # znajdujemy koniec fragmentu z delayami i ucinamy wszystko po
        endline = 0
        for i in range(0, len(lines)):
            if len(lines[i]) < 60:
                endline = i
                break

        lines = lines[:endline]
        single_lines_list = []              # lista obiektow klasy SingleLine
        for line in lines:
            single_line = split_line(line)
            single_lines_list.append(single_line)

        print_delays(single_lines_list, headers_printed, host_switch_dict, switches_list, links_dict)
        headers_printed = True
        sleep(3)


def calculate_avg_delay(single_lines_list, host_switch_dict, switches_list, links_dict):
    delay_sum = 0.0
    delay_counter = 0
    for key in links_dict.keys():               # lecimy po wszystkich linkach
        src_switch = key[:3]                    # tlumaczymy src i dst linka na hosty
        dst_switch = links_dict[key][:3]
        src_host = host_switch_dict[src_switch]
        dst_host = host_switch_dict[dst_switch]

        # todo zoptymalizowac
        for line in single_lines_list:          # szukamy wsrod wszystkich pomiarow pomiaru dla danego linka i printujemy go
            if line.src_name == src_host and line.dst_name == dst_host:
                if line.average_delay != 0:
                    delay_sum += line.average_delay
                    delay_counter += 1
                break

    avg_delay = delay_sum / delay_counter
    return avg_delay


def read_whole_log_file(filename, host_switch_dict, switches_list, links_dict):
    my_file = open(filename, "r")
    lines = my_file.readlines()

    # przejście po wszystkich liniach, wychwycenie linii z *** results
    results_lines = []  # nry linii z *** results
    for i in range(0, len(lines)):
        lines[i] = lines[i][:-1]
        if lines[i] == "*** Results: ":
            results_lines.append(i)

            # bierzemy przedostatnie results i ucinamy wszystko przed
            startline = results_lines[len(results_lines) - 2]
            lines = lines[startline + 1:]

            # znajdujemy koniec fragmentu z delayami i ucinamy wszystko po
            endline = 0
            for i in range(0, len(lines)):
                if len(lines[i]) < 60:
                    endline = i
                    break

            lines = lines[:endline]
            single_lines_list = []  # lista obiektow klasy SingleLine
            for line in lines:
                single_line = split_line(line)
                single_lines_list.append(single_line)

    avg_delay = calculate_avg_delay(single_lines_list, host_switch_dict, switches_list, links_dict)
    print(avg_delay)



import pandas as pd


def process_file(filename):
    names = get_names(filename)
    myFile = open(filename, "r").read().splitlines()
    names["input_Mb"] = 0
    names["output_Mb"] = 0
    names["input_pkts"] = 0
    names["output_pkts"] = 0
    names["diff"] = 0
    names["discards"] = 0
    names["errors"] = 0
    names.columns = ["name", "input_Mb", "output_Mb", "input_pkts", "output_pkts", "diff", "discards", "errors"]
    counter = 0
    inOctets = 0
    last_name = ""
    for line in myFile:
        if counter % 8 == 0:        # todo replace 8 with parameter
            last_name = line
        if counter % 8 == 1:
            inOctets = int(line)
            index = names[names['name'] == last_name].index.item()
            names.at[index, 'input_Mb'] = inOctets
        if counter % 8 == 2:
            index = names[names['name'] == last_name].index.item()
            names.at[index, 'output_Mb'] = int(line)
            diff = inOctets - int(line)
            index = names[names['name'] == last_name].index.item()
            names.at[index, 'diff'] = diff
        # if counter % 8 == 3:
        #     index = names[names['name'] == last_name].index.item()
        #     names.at[index, 'input_pkts'] = int(line)
        # if counter % 8 == 4:
        #     index = names[names['name'] == last_name].index.item()
        #     names.at[index, 'output_pkts'] = int(line)
        if counter % 8 == 5:
            index = names[names['name'] == last_name].index.item()
            names.at[index, 'discards'] = int(line)
        # if counter % 8 == 6:
        #     index = names[names['name'] == last_name].index.item()
        #     names.at[index, 'errors'] = int(line)

        counter = counter + 1
    convert_to_mb(names)
    print(names)


def get_names(filename):
    file = open(filename, "r")
    lines = file.readlines()
    desired_lines = lines[0::8]     # todo replace 8
    for i in range(0, len(desired_lines)):
        desired_lines[i] = desired_lines[i][:-1]
    names = set(desired_lines)
    names_list = list(names)
    names_df = pd.DataFrame(names_list)
    file.close()
    return names_df


def convert_to_mb(df):
    df['input_Mb'] = df['input_Mb'].apply(lambda x: x / 1000000)
    df['output_Mb'] = df['output_Mb'].apply(lambda x: x / 1000000)
    df['diff'] = df['diff'].apply(lambda x: x / 1000000)


process_file("sflowMonitorLogs.txt")

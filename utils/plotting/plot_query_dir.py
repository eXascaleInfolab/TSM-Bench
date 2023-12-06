from utils.plotting.options import color_dict
import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_query_directory(query_dir):
    runtime_dir = f"{query_dir}/runtime"
    plot_dir = f"{query_dir}/plots"
    selected_query = query_dir.split("/")[-1]

    if not os.path.exists(plot_dir):
        os.mkdir(plot_dir)
    db_txt_files = sorted([f_name for f_name in os.listdir(runtime_dir) if f_name.endswith(".txt")])

    results = {file_n.split(".")[0]: pd.read_csv(runtime_dir + "/" + file_n, index_col=0) for file_n in db_txt_files}

    stations_scenario = {k: df[df.index.str.contains('st_')][["runtime"]] for k, df in results.items()}

    sensor_scenario = {k: df[df.index.str.contains('s_')][["runtime"]] for k, df in results.items()}

    time_scenario = {k: df[~df.index.str.contains('_')][["runtime"]] for k, df in results.items()}

    combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in stations_scenario.items()], axis=1)
    new_index = combined_df.index.map(lambda x: int(x[3:]))
    combined_df.set_index(new_index, inplace=True)

    combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
    plt.xlabel("# Stations")
    plt.ylabel("Runtime (ms)")
    plt.title(f"{selected_query} varying #stations")
    plt.savefig(f"{plot_dir}/stations.png")
    plt.close()

    combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in sensor_scenario.items()], axis=1)
    new_index = combined_df.index.map(lambda x: int(x.strip()[2:]))
    combined_df.set_index(new_index, inplace=True)
    combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
    plt.ylabel("Runtime (ms)") or plt.xlabel("#Sensors")
    plt.title(f"{selected_query} varying #sensors")
    plt.savefig(f"{plot_dir}/sensors.png")
    plt.close()

    combined_df = pd.concat([df.rename(columns={'runtime': key}) for key, df in time_scenario.items()], axis=1)
    combined_df.plot(color=[color_dict.get(x, '#333333') for x in combined_df.columns])
    plt.ylabel("Runtime (ms)") or plt.xlabel("Query Range")
    plt.title(f"{selected_query} varying query range")
    plt.savefig(f"{plot_dir}/time_range.png")
    plt.close()

import os
import datetime
import time
import sys

def convert_csv_to_influxdb_format(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    output_folder = "datasets_influx"
    #output_folder = os.path.join(folder_path, "datasets_influx")
    os.makedirs(output_folder, exist_ok=True)

    processed_files = set()  # To keep track of processed files

    start = time.time()

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and filename not in processed_files:
            csv_path = os.path.join(folder_path, filename)
            dataset_name = os.path.splitext(filename)[0]
            output_filename = os.path.join(output_folder, f"{dataset_name}-influxdb.csv")

            with open(output_filename, 'w') as data_target:
                head_line = f"# DDL\n CREATE DATABASE {dataset_name}\n"
                head_line2 = f"# DML\n# CONTEXT-DATABASE: {dataset_name}\n"
                data_target.write(head_line)
                data_target.write(head_line2)

                with open(csv_path, 'r') as data_src:
                    line = data_src.readline()
                    index = 1
                    new_line = '\n'
                    while True:
                        line = data_src.readline()
                        if not line:
                            break
                        if line.strip() != '':
                            columns = line.split(',')
                            date_str = columns[0]
                            date_str = str(int(datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").timestamp()) * 1000)
                            id_station = columns[1]
                            influx_line = f"sensor,id_station={id_station} "
                            influx_line += ",".join([f"s{i}={(v if (v != '' and v != new_line) else 'null')}" for i, v in enumerate(columns[2:102]) if (v != '' and v != new_line)])
                            influx_line = influx_line[:-1] + " " + date_str + '\n'
                            data_target.write(influx_line)
                            if index % 1000 == 0:
                                print(f"Processed {index} lines for dataset '{dataset_name}'")
                            index += 1

            processed_files.add(filename)  # Mark file as processed

    print(f"Conversion completed. Time taken: {time.time() - start} seconds")

# Check if folder path is provided as argument
if len(sys.argv) < 2:
    print("Please provide the folder path containing CSV files.")
    sys.exit(1)

# Get folder path from command line argument
folder_path = sys.argv[1]

# Call the function to convert CSV files to InfluxDB format
convert_csv_to_influxdb_format(folder_path)

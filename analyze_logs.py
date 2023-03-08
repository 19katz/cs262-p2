import matplotlib.pyplot as plt
import numpy as np
import os
import csv

def read_and_parse_from_log(file):
    with open(file, 'r') as fr:
        first_line = fr.readline()
        args = first_line.split(':')
        clock_rate = int(args[-1].strip())
        logical_clock_times = []
        max_queue_length = 0
        jumps = []
        drifts = []
        i = 0
        while True:
            line = fr.readline()
            if not line:
                break
            line_args = line.split(';')
            line_clock = line_args[1]
            logical_clock_time = int(line_clock.split(':')[1].strip())
            logical_clock_times.append(logical_clock_time)

            if i > 0:
                prev_time = logical_clock_times[i - 1]
                jumps.append(logical_clock_time - prev_time)

            drifts.append(round(logical_clock_time / clock_rate - (i + 1) / clock_rate, 2))

            if "Received" in line:
                line_queue = line_args[2]
                queue_length = int(line_queue.split(':')[-1].strip())

                if queue_length > max_queue_length:
                    max_queue_length = queue_length
            i += 1
    fr.close()
        
    return clock_rate, logical_clock_times, jumps, drifts, max_queue_length

def plot_histogram(data, x_vals, x_label, y_label, title, timestamp):
    fig, ax = plt.subplots(figsize =(6, 4))
    ax.hist(data, bins = x_vals)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.title(title)
    plt.savefig("./plots/" + timestamp + "_" + title + ".png", dpi=120)
    plt.close()

if __name__ == "__main__":
    directory = "./normal_logs/"
    files = [f for f in os.listdir(directory)]
    timestamps = []
    out_file = "6_tickrange_5_runs_data.csv"

    # getting the timestamp identifiers for each run
    for f in files:
        if ".log" in f:
            timestamp = f.split('_')[1]
            if timestamp not in timestamps:
                timestamps.append(timestamp)

    with open(out_file, 'w') as out:
        csvwriter = csv.writer(out)
        csvwriter.writerow(['Trial', 'Tick Rate', 'Mean Jump', 'Stdev Jump', 'Max Jump', 'Max Drift', 'Max Queue Length'])

        for i in range(len(timestamps)):
            timestamp = timestamps[i]
            for j in range(3):
                t_file = directory + "machine_" + timestamp + "_" + str(j) + "_6.log"
                clock_rate, logical_clock_times, jumps, drifts, max_queue_length = read_and_parse_from_log(t_file)
                max_jump = max(jumps)
                mean_jump = round(np.mean(jumps), 3)
                std_jump = round(np.std(jumps), 3)
                print(max_jump)
                plot_histogram(jumps, range(0, max_jump + 1), "Jump Magnitude", "Frequency", "Jump Histogram for Trial " + str(i) + " machine " + str(j) + " with tick rate = "+ str(clock_rate), timestamp)
                max_drift = max(drifts)
                
                to_write = [i, clock_rate, mean_jump, std_jump, max_jump, max_drift, max_queue_length]
                csvwriter.writerow(to_write)
    
    directory = "./exp_logs/"
    files = [f for f in os.listdir(directory)]
    timestamps = []
    tick_ranges = []
    rand_ranges = []
    out_file = "varied_params_runs_data.csv"

    # getting the timestamp identifiers for each run
    for f in files:
        if ".log" in f:
            args = f.split('_')
            timestamp = args[1]
            if timestamp not in timestamps:
                timestamps.append(timestamp)

    with open(out_file, 'w') as out:
        csvwriter = csv.writer(out)
        csvwriter.writerow(['Trial', 'Tick Rate', 'Mean Jump', 'Stdev Jump', 'Max Jump', 'Max Drift', 'Max Queue Length'])

        for i in range(len(timestamps)):
            timestamp = timestamps[i]

            for j in range(3):
                t_file = directory + "machine_" + timestamp + "_" + str(j) + "_3_5.log"
                clock_rate, logical_clock_times, jumps, drifts, max_queue_length = read_and_parse_from_log(t_file)
                max_jump = max(jumps)
                mean_jump = round(np.mean(jumps), 3)
                std_jump = round(np.std(jumps), 3)
                print(jumps)
                print(max_jump)
                plot_histogram(jumps, range(0, max_jump + 1), "Jump Magnitude", "Frequency", "Jump Histogram for tick range = 3, rand = 5, machine " + str(j) + ", tick rate = "+ str(clock_rate), timestamp)
                max_drift = max(drifts)
                
                to_write = [i, clock_rate, mean_jump, std_jump, max_jump, max_drift, max_queue_length]
                csvwriter.writerow(to_write)
    







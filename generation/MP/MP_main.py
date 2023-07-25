import json
import time
from decimal import Decimal

import pandas as pd

import statistics as s
from stream.MP.library import *


def main(export_path, path_ori_dataset, path_fake, num_cont, dict_size, learn=True):
    # export_path = 'ec21ts/shift=10/'
    # dataset_name = 'TravelTime1ts'
    # path_ori_dataset = './datasets/ec21ts.csv'
    # path_ori_dataset = './datasets/TravelTime1ts.csv'

    # path_fake = export_path + 'fake.csv'

    # load parameters

    with open("./parameters.json", "r") as f:
        para_dict = json.load(f)
        # dict_size = para_dict['batch_size_generation']
        window = para_dict["window"]
        # num_cont = para_dict["num_cont"]

    # load original data and create its windows
    x = np.genfromtxt(path_ori_dataset, delimiter=',', dtype=np.float32)
    # x = x[1:, 1:]
    ori = (x - x.min()) / (x.max() - x.min())



    total_generation = []
    # load generated data
    for ts_index in range(num_cont):

        df_ori = pd.DataFrame()
        for i in range(int(len(ori) / window)):
            df_ori[str(i)] = [i[0] for i in ori[i * window:(i + 1) * window]]

        # last window
        if len(ori) % window != 0:
            df_ori[str(int(len(ori) / window))] = [i[0] for i in ori[len(ori) - window:len(ori)]]

        df_ori.columns = [i for i in range(len(df_ori.columns))]
        # df_ori.to_csv('original.csv')

        print(ts_index)
        df_fake = pd.read_csv(path_fake + 'fake' + str(ts_index) + '.csv')
        df_fake.columns = [i for i in range(len(df_fake.columns))]

        # CREATING TRICKLETS
        time_series_data_dictionary = dataframeToTricklets(df_fake, window)
        time_series_data = dataframeToTricklets(df_ori, window)

        print("Building the dictionary for series %d... \n" % ts_index, end='')
        for i in range(1, int(len(time_series_data_dictionary))):
            time_series_data_dictionary[0].extend(time_series_data_dictionary[i])

        if learn:
            Dictionary = learnDictionary(time_series_data_dictionary[0], dict_size, 1, 500,
                                         export_path + 'dictionary' + str(ts_index) + '.pkl')
        else:
            try:
                Dictionary = load_object(export_path + 'dictionary' + str(ts_index) + '.pkl')
            except:
                print("No dictionary found, learning instead!")
                Dictionary = learnDictionary(time_series_data_dictionary[0], dict_size, 1, 500,
                                             export_path + 'dictionary' + str(ts_index) + '.pkl')

        # COMPRESSING THE DATA THE TRISTAN WAY
        start1 = time.time()
        atoms_coded_tricklets, recons, errors = compress_without_correlation(time_series_data, Dictionary, 1, 'omp')

        print('Computation time without correlation: ', round(Decimal(time.time() - start1), 2), 's')
        print('New error:', "{0:.5}".format(s.mean(errors)))

        generation = recons[0][0]
        for i in range(1, len(recons)):
            if len(generation) + window > len(ori):
                generation = generation[:len(ori) - window]
            generation = np.array(list(generation) + recons[i][0])

        # generation = np.array(list(generation) + [0 for i in range(len(ori) - len(generation))])

        np.savetxt(export_path + "fake_long" + str(ts_index) + ".csv", generation, delimiter=",")

        # plt.plot(ori)  # plotting by columns
        # plt.plot(generation)  # plotting by columns
        # plt.show()

        fig, axs = plt.subplots(2, sharex=True)
        fig.suptitle('Original vs. Generated data for ' + export_path + str(ts_index))
        axs[0].plot(ori[:,ts_index])
        axs[0].set_title('original data')
        axs[1].plot(generation)
        axs[1].set_title('generated data')
        # axs[1].get_shared_x_axes().join(axs[1], axs[0])
        # plt.show()
        plt.savefig(export_path + 'ori_vs_generation' + str(ts_index) + '.png')
        total_generation.append(generation)
    total_generation = pd.DataFrame(total_generation).T
    total_generation.to_csv(export_path + "fake_long_complete.csv", index=False)
    return ori, total_generation

# main(learn = False)

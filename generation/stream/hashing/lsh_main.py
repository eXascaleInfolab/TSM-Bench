import time
from decimal import Decimal

import pandas as pd
import lshashpy3 as lshash
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import random

import sys

sys.path.insert(1, '~/ABench-IoT/Generation/stream/')


class LSH_conca:

    def lsh_generate_with_update(self, ori_path, df_fake, export_path, window_size, top_n, tr_sampling_size, conca_plot,
                                 num_hashtables, hash_size_percentage,
                                 update_percentage, nb_fragments, gen_ts_length=0, gen_ts_dim=0):
        """
        Formats a number (greater than unity) with SI Order of Magnitude
        prefixes.

        Parameters
        ----------
        ori_path  : string
            Path to the original time series dataset, it can be of any number of time series.

            Example:
                564,563
                730,324LSH
                770,135

        gen_path  : string
            Path to a directory that contains files of the generated time series.

            For each time series, a file named 'fake{i}.csv', for example: fake0.csv (for the first time series)
                and fake1.csv (for the first time series)

            Example:
                └── ./gen_path/
                    ├── fake0.csv
                    ├── fake1.csv
                    ├── fake2.csv
                    └── fake3.csv

                Content of fake0.csv
                0,1,2,3....,500
                0.36852998,0.36335656,....,0.37748763

        export_path  : string
            Path of the directory to export the full time series files.

            Example of result:
                └── ./export_path/
                    ├── fake_long0.csv
                    ├── fake_long1.csv
                    └── fake_long_complete.csv


        window_size  : Integer
            Size of the generation window


        nb_fragments : Integer
            Number of the first generate sequences to consider for each time series


        Returns
        -------
        original    : Pandas Dataframe
            Dataframe containing full original time series.

        total_generation    : Pandas Dataframe
            Dataframe containing full generated time series.

        """

        '''
        while True:
            GAN()
            index()
            query()
            while(used < 90%)
                concat()
            if enough:
                break
        '''
        export_path += 'lsh_with_update/'
        # load original data and create its windows
        if tr_sampling_size > window_size:
            print(ori_path, tr_sampling_size)
            df = pd.read_csv(ori_path, delimiter=',', header=None, nrows=tr_sampling_size)
        else:
            df = pd.read_csv(ori_path, delimiter=',', header=None)
        # x = np.genfromtxt(ori_path, delimiter=',', dtype=np.float32)
        x = df.to_numpy()
        x_list = [float(x[i][0]) for i in range(len(x))]
        x = np.array(x_list)
        ori = (x - x.min()) / (x.max() - x.min())
        try:
            a = x.shape[1]
            del a
        except Exception:
            x = x.reshape(-1, 1)
            ori = ori.reshape(-1, 1)

        start_LSH = time.time()
        compute_time = []
        num_cont = x.shape[1]
        generation = []
        start_time = time.time()

        # time_file = 'lsh_time_bafu.txt'

        for ts_index in range(num_cont):
            generated_so_far = 0
            while True:
                print('gan generating segments...')
                time.sleep(5)

                # total_generation = []
                lsh_arr = []
                non_found_windows = 0
                num_cont = x.shape[1]
                # top_n = max(top_n, gen_ts_dim)
                # top_n = min(top_n, 10)
                time_series_data_fake = []
                time_series_data_ori = []
                gen_ts_dim = max(gen_ts_dim, num_cont)
                total_query_results = []

                print('\nindexing the generated segments...')

                # prepare the hash tables
                lsh_arr.append(
                    lshash.LSHash(int(window_size * hash_size_percentage / 100), window_size,
                                  num_hashtables=num_hashtables))

                # prepare the windows
                df_ori = pd.DataFrame()
                for i in range(int(len(ori) / window_size)):
                    try:
                        df_ori[str(i)] = [i[0] for i in ori[i * window_size:(i + 1) * window_size]]
                    except:
                        df_ori[str(i)] = [i for i in ori[i * window_size:(i + 1) * window_size]]

                # last window_size
                if len(ori) % window_size != 0:
                    try:
                        df_ori[str(int(len(ori) / window_size))] = [i[0] for i in ori[len(ori) - window_size:len(ori)]]
                    except:
                        df_ori[str(int(len(ori) / window_size))] = [i for i in ori[len(ori) - window_size:len(ori)]]

                df_ori.columns = [i for i in range(len(df_ori.columns))]
                df_ori = df_ori.T

                # CREATING Windows
                time_series_data_ori.append(self._dataframeToWindows(df_ori, window_size))

                time_series_data_fake.append(self._dataframeToWindows(df_fake, window_size))

                # Building the Hashing tables for series
                print('\nindexing the generated time series ', ts_index + 1)

                for i in tqdm(range(nb_fragments)):
                    lsh_arr[ts_index].index(time_series_data_fake[-1][i][0])

                print('indexing is done\nquerying begins...')

                query_results = []

                for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
                    counter = 5
                    start1 = time.time()
                    while counter > 0:
                        try:
                            gen = [j[0][0] for j in
                                   lsh_arr[ts_index].query(time_series_data_ori[ts_index][i][0], num_results=top_n,
                                                           distance_func="euclidean")]
                            # print('gen', gen)
                            if gen:
                                query_results.append(gen)
                                break
                        except Exception as e:
                            pass
                            # print('empty output, tries left: ', counter)
                        counter -= 1
                    if counter == 0:
                        non_found_windows += 1
                        query_results.append([time_series_data_fake[ts_index][i][0]])

                    total_query_results.append(query_results)
                    compute_time.append(time.time() - start1)

                print('\nquerying is done\nconcatenation begins...')

                cpt = ts_index

                while (len(generation) - generated_so_far) / window_size < update_percentage * nb_fragments:
                    gen = []
                    # print('\nconcatenating ts: ', ts_index + 1, ', generating ts: ', cpt)
                    for i in range(int(len(time_series_data_ori[ts_index])) - 1):
                        gen.extend(random.choice(total_query_results[ts_index][i]))

                    if (len(gen) % len(ori)) + window_size > len(ori):
                        gen = gen[:int(len(ori) * (len(gen) / len(ori) + 1) - window_size)]
                        gen.extend(random.choice(total_query_results[ts_index][-1]))
                    generation.extend(gen)
                generated_so_far = len(generation)
                print('len(generation)', len(generation))
                print(len(generation) / window_size, gen_ts_length)
                if (len(generation) / window_size >= gen_ts_length):
                    np.savetxt(export_path + "fake_long" + str(cpt) + ".csv", np.array(generation), delimiter=",")
                    break
                else:
                    continue

            print('concatenation is done\nexporting one full dataset file begins...')

            # total_generation.append(generation)

            # if conca_plot:
            #     fig, axs = plt.subplots(2, sharex=True)
            #     fig.suptitle('Original vs. Generated data for ' + export_path + str(cpt))
            #
            #     axs[0].plot([i[0] for i in
            #                  np.repeat(np.expand_dims(ori[:, ts_index], axis=0), repeats=gen_ts_length, axis=0).reshape(-1,
            #                                                                                                             1).tolist()])
            #     axs[0].set_title('original data')
            #     axs[1].plot(generation)
            #     axs[1].set_title('generated data')
            #
            #     plt.savefig(export_path + 'ori_vs_generation' + str(cpt) + '.png')

        # file_object = open(export_path+'time_results.txt', 'a')
        # file_object.write("\n--- LSH Time: %s seconds ---" % (time.time() - start_LSH))
        # file_object.close()
        print("--- LSH Time: %s seconds ---" % (time.time() - start_LSH))

        try:
            import os
            full_data = ''.join([export_path + "fake_long" + str(cpt) + ".csv " for cpt in range(gen_ts_dim)])
            os.system("paste " +
                      full_data +
                      "-d ',' > " + export_path + "fake_long_complete.csv")
        except:
            print("couldn't generate one full file")
        print('\nNumber of non-found windows is: {} (or {}% of the generated data).'.format(non_found_windows,
                                                                                            100 * float(
                                                                                                non_found_windows) / float(
                                                                                                df_ori.shape[
                                                                                                    1] * gen_ts_dim)))
        print('Average hash searching time: ', round((sum(compute_time) / len(compute_time)), 2), 's')
        return time.time() - start_LSH

    def lsh_generate_without_update(self, ori_path, df_fake, export_path, window_size, top_n, tr_sampling_size,
                                    conca_plot, num_hashtables, hash_size_percentage,
                                    update_percentage, nb_fragments, gen_ts_length=0, gen_ts_dim=0):
        """
        Formats a number (greater than unity) with SI Order of Magnitude
        prefixes.

        Parameters
        ----------
        ori_path  : string
            Path to the original time series dataset, it can be of any number of time series.

            Example:
                564,563
                730,324LSH
                770,135

        gen_path  : string
            Path to a directory that contains files of the generated time series.

            For each time series, a file named 'fake{i}.csv', for example: fake0.csv (for the first time series)
                and fake1.csv (for the first time series)

            Example:
                └── ./gen_path/
                    ├── fake0.csv
                    ├── fake1.csv
                    ├── fake2.csv
                    └── fake3.csv

                Content of fake0.csv
                0,1,2,3....,500
                0.36852998,0.36335656,....,0.37748763

        export_path  : string
            Path of the directory to export the full time series files.

            Example of result:
                └── ./export_path/
                    ├── fake_long0.csv
                    ├── fake_long1.csv
                    └── fake_long_complete.csv


        window_size  : Integer
            Size of the generation window


        nb_fragments : Integer
            Number of the first generate sequences to consider for each time series


        Returns
        -------
        original    : Pandas Dataframe
            Dataframe containing full original time series.

        total_generation    : Pandas Dataframe
            Dataframe containing full generated time series.

        """

        '''
        while True:
            GAN()
            index()
            query()
            while(not enough)
                concat()
        '''
        export_path += 'lsh_without_update/'
        # load original data and create its windows
        if tr_sampling_size > window_size:
            print(ori_path, tr_sampling_size)
            df = pd.read_csv(ori_path, delimiter=',', header=None, nrows=tr_sampling_size)
        else:
            df = pd.read_csv(ori_path, delimiter=',', header=None)
        # x = np.genfromtxt(ori_path, delimiter=',', dtype=np.float32)
        x = df.to_numpy()
        x_list = [float(x[i][0]) for i in range(len(x))]
        x = np.array(x_list)
        ori = (x - x.min()) / (x.max() - x.min())
        try:
            a = x.shape[1]
            del a
        except Exception:
            x = x.reshape(-1, 1)
            ori = ori.reshape(-1, 1)

        start_LSH = time.time()
        compute_time = []
        num_cont = x.shape[1]
        generation = []
        start_time = time.time()

        # time_file = 'lsh_time_bafu.txt'

        for ts_index in range(num_cont):
            generated_so_far = 0

            print('gan generating segments...')
            time.sleep(5)

            # total_generation = []
            lsh_arr = []
            non_found_windows = 0
            num_cont = x.shape[1]
            # top_n = max(top_n, gen_ts_dim)
            # top_n = min(top_n, 10)
            time_series_data_fake = []
            time_series_data_ori = []
            gen_ts_dim = max(gen_ts_dim, num_cont)
            total_query_results = []

            print('\nindexing the generated segments...')

            # prepare the hash tables
            lsh_arr.append(
                lshash.LSHash(int(window_size * hash_size_percentage / 100), window_size,
                              num_hashtables=num_hashtables))

            # prepare the windows
            df_ori = pd.DataFrame()
            for i in range(int(len(ori) / window_size)):
                try:
                    df_ori[str(i)] = [i[0] for i in ori[i * window_size:(i + 1) * window_size]]
                except:
                    df_ori[str(i)] = [i for i in ori[i * window_size:(i + 1) * window_size]]

            # last window_size
            if len(ori) % window_size != 0:
                try:
                    df_ori[str(int(len(ori) / window_size))] = [i[0] for i in
                                                                ori[len(ori) - window_size:len(ori)]]
                except:
                    df_ori[str(int(len(ori) / window_size))] = [i for i in ori[len(ori) - window_size:len(ori)]]

            df_ori.columns = [i for i in range(len(df_ori.columns))]
            df_ori = df_ori.T

            # CREATING Windows
            time_series_data_ori.append(self._dataframeToWindows(df_ori, window_size))

            time_series_data_fake.append(self._dataframeToWindows(df_fake, window_size))

            # Building the Hashing tables for series
            print('\nindexing the generated time series ', ts_index + 1)

            for i in tqdm(range(nb_fragments)):
                lsh_arr[ts_index].index(time_series_data_fake[-1][i][0])

            print('indexing is done\nquerying begins...')

            query_results = []

            for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
                counter = 5
                start1 = time.time()
                while counter > 0:
                    try:
                        gen = [j[0][0] for j in
                               lsh_arr[ts_index].query(time_series_data_ori[ts_index][i][0], num_results=top_n,
                                                       distance_func="euclidean")]
                        # print('gen', gen)
                        if gen:
                            query_results.append(gen)
                            break
                    except Exception as e:
                        pass
                        # print('empty output, tries left: ', counter)
                    counter -= 1
                if counter == 0:
                    non_found_windows += 1
                    query_results.append([time_series_data_fake[ts_index][i][0]])

                total_query_results.append(query_results)
                compute_time.append(time.time() - start1)

            print('\nquerying is done\nconcatenation begins...')

            cpt = ts_index

            while len(generation) / window_size <= gen_ts_length:
                gen = []
                # print('\nconcatenating ts: ', ts_index + 1, ', generating ts: ', cpt)
                for i in range(int(len(time_series_data_ori[ts_index])) - 1):
                    gen.extend(random.choice(total_query_results[ts_index][i]))

                if (len(gen) % len(ori)) + window_size > len(ori):
                    gen = gen[:int(len(ori) * (len(gen) / len(ori) + 1) - window_size)]
                    gen.extend(random.choice(total_query_results[ts_index][-1]))
                generation.extend(gen)
            generated_so_far = len(generation)
            print('len(generation)', len(generation))
            print(len(generation) / window_size, gen_ts_length)
            np.savetxt(export_path + "fake_long" + str(cpt) + ".csv", np.array(generation), delimiter=",")

            print('concatenation is done\nexporting one full dataset file begins...')

            # total_generation.append(generation)
        print("--- LSH Time: %s seconds ---" % (time.time() - start_LSH))

        try:
            import os
            full_data = ''.join([export_path + "fake_long" + str(cpt) + ".csv " for cpt in range(gen_ts_dim)])
            os.system("paste " +
                      full_data +
                      "-d ',' > " + export_path + "fake_long_complete.csv")
        except:
            print("couldn't generate one full file")
        print('\nNumber of non-found windows is: {} (or {}% of the generated data).'.format(non_found_windows,
                                                                                            100 * float(
                                                                                                non_found_windows) / float(
                                                                                                df_ori.shape[
                                                                                                    1] * gen_ts_dim)))
        print('Average hash searching time: ', round((sum(compute_time) / len(compute_time)), 2), 's')
        return time.time() - start_LSH

        # def lsh_main_input_complexity(self, ori_path, df_fake, export_path, window_size, top_n, tr_sampling_size, conca_plot, num_hashtables, hash_size_percentage,
        #                   update_percentage, nb_fragments, gen_ts_length=0, gen_ts_dim=0):
        #     """
        #     Formats a number (greater than unity) with SI Order of Magnitude
        #     prefixes.
        #
        #     Parameters
        #     ----------
        #     ori_path  : string
        #         Path to the original time series dataset, it can be of any number of time series.
        #
        #         Example:
        #             564,563
        #             730,324LSH
        #             770,135
        #
        #     gen_path  : string
        #         Path to a directory that contains files of the generated time series.
        #
        #         For each time series, a file named 'fake{i}.csv', for example: fake0.csv (for the first time series)
        #             and fake1.csv (for the first time series)
        #
        #         Example:
        #             └── ./gen_path/
        #                 ├── fake0.csv
        #                 ├── fake1.csv
        #                 ├── fake2.csv
        #                 └── fake3.csv
        #
        #             Content of fake0.csv
        #             0,1,2,3....,500
        #             0.36852998,0.36335656,....,0.37748763
        #
        #     export_path  : string
        #         Path of the directory to export the full time series files.
        #
        #         Example of result:
        #             └── ./export_path/
        #                 ├── fake_long0.csv
        #                 ├── fake_long1.csv
        #                 └── fake_long_complete.csv
        #
        #
        #     window_size  : Integer
        #         Size of the generation window
        #
        #
        #     nb_fragments : Integer
        #         Number of the first generate sequences to consider for each time series
        #
        #
        #     Returns
        #     -------
        #     original    : Pandas Dataframe
        #         Dataframe containing full original time series.
        #
        #     total_generation    : Pandas Dataframe
        #         Dataframe containing full generated time series.
        #
        #     """
        #
        #     '''
        #     while True:
        #         GAN()
        #         index()
        #         query()
        #         while(used < 90%)
        #             concat()
        #         if enough:
        #             break
        #     '''
        #     export_path += 'lsh/'
        #     # load original data and create its windows
        #     if tr_sampling_size > window_size:
        #         print(ori_path, tr_sampling_size)
        #         df = pd.read_csv(ori_path, delimiter=',', header=None, nrows=tr_sampling_size)
        #     else:
        #         df = pd.read_csv(ori_path, delimiter=',', header=None)
        #     # x = np.genfromtxt(ori_path, delimiter=',', dtype=np.float32)
        #     x = df.to_numpy()
        #     x_list = [float(x[i][0]) for i in range(len(x))]
        #     x = np.array(x_list)
        #     ori = (x - x.min()) / (x.max() - x.min())
        #     try:
        #         a = x.shape[1]
        #         del a
        #     except Exception:
        #         x = x.reshape(-1, 1)
        #         ori = ori.reshape(-1, 1)
        #
        #     start_LSH = time.time()
        #     compute_time = []
        #     num_cont = x.shape[1]
        #     generation = []
        #     start_time = time.time()
        #
        #     # time_file = 'lsh_time_bafu.txt'
        #
        #     for ts_index in range(num_cont):
        #         generated_so_far = 0
        #         while True:
        #             # if gen_ts_length >= 2:  # NOT MEMORY EFFICIENT!
        #             #     ori_long = np.repeat(np.expand_dims(ori, axis=0), repeats=gen_ts_length, axis=0).reshape(-1, ori.shape[1])
        #
        #             # total_generation = []
        #             lsh_arr = []
        #             non_found_windows = 0
        #             num_cont = x.shape[1]
        #             # top_n = max(top_n, gen_ts_dim)
        #             # top_n = min(top_n, 10)
        #             time_series_data_fake = []
        #             time_series_data_ori = []
        #             gen_ts_dim = max(gen_ts_dim, num_cont)
        #             total_query_results = []
        #
        #             print('\nindexing the generated time series ')
        #
        #             # indexing generated data
        #
        #
        #             # prepare the hash tables
        #             lsh_arr.append(
        #                 lshash.LSHash(int(window_size * hash_size_percentage / 100), window_size,
        #                               num_hashtables=num_hashtables))
        #
        #             # prepare the windows
        #             df_ori = pd.DataFrame()
        #             for i in range(int(len(ori) / window_size)):
        #                 try:
        #                     df_ori[str(i)] = [i[0] for i in ori[i * window_size:(i + 1) * window_size]]
        #                 except:
        #                     df_ori[str(i)] = [i for i in ori[i * window_size:(i + 1) * window_size]]
        #
        #             # last window_size
        #             if len(ori) % window_size != 0:
        #                 try:
        #                     df_ori[str(int(len(ori) / window_size))] = [i[0] for i in ori[len(ori) - window_size:len(ori)]]
        #                 except:
        #                     df_ori[str(int(len(ori) / window_size))] = [i for i in ori[len(ori) - window_size:len(ori)]]
        #
        #             df_ori.columns = [i for i in range(len(df_ori.columns))]
        #             df_ori = df_ori.T
        #
        #             # df_fake = df_fake.T
        #             # selected_columns = [i for i in range(len(df_fake.columns))]
        #             # if nb_fragments is not None:
        #             #     selected_columns = selected_columns[:nb_fragments]
        #             #     df_fake = df_fake[df_fake.columns.intersection(selected_columns)]
        #
        #             # CREATING Windows
        #             time_series_data_ori.append(self._dataframeToWindows(df_ori, window_size))
        #
        #             time_series_data_fake.append(self._dataframeToWindows(df_fake, window_size))
        #
        #             # Building the Hashing tables for series
        #             print('\nindexing the generated time series ', ts_index + 1)
        #             # for nb_fragments in tqdm(range(100, 3072, 100)):
        #             for i in tqdm(range(nb_fragments)):
        #                 # for i in tqdm(range(int(len(time_series_data_fake[-1])))):
        #                 # for i in tqdm(range(int(len(time_series_data_fake[-1])))):
        #                 # print(ts_index, i)
        #                 lsh_arr[ts_index].index(time_series_data_fake[-1][i][0])
        #             # file_object = open('/Users/abdel/PycharmProjects/ABench-IoT/Generation/stream/hashing/' + time_file, 'a')
        #             # file_object.write(str(nb_fragments) + ',' + str(time.time() - start_time)+'\n')
        #             # file_object.close()
        #
        #
        #             print('indexing is done\n'
        #                   + 'querying begins...')
        #
        #
        #             # for ts_index in range(num_cont):
        #             query_results = []
        #             # print('\nquerying ts: ', ts_index + 1)
        #             start1 = time.time()
        #             for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
        #                 # for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
        #                 counter = 5
        #                 while counter > 0:
        #                     try:
        #                         gen = [j[0][0] for j in
        #                                lsh_arr[ts_index].query(time_series_data_ori[ts_index][i][0], num_results=top_n,
        #                                                        distance_func="euclidean")]
        #                         # print('gen', gen)
        #                         if gen:
        #                             query_results.append(gen)
        #                             break
        #                     except Exception as e:
        #                         pass
        #                         # print('empty output, tries left: ', counter)
        #                     counter -= 1
        #                 if counter == 0:
        #                     non_found_windows += 1
        #                     query_results.append([time_series_data_fake[ts_index][i][0]])
        #
        #             total_query_results.append(query_results)
        #             compute_time.append(time.time() - start1)
        #
        #             print('\nquerying is done\nconcatenation begins...')
        #
        #             # total_generation= []
        #             # for cpt in tqdm(range(gen_ts_dim), position=0, leave=True):
        #             cpt = ts_index
        #             # ts_index = cpt % num_cont
        #
        #
        #             # for r in range(gen_ts_length):
        #             # while (len(generation)/len(ori) < gen_ts_length and (len(generation) - generated_so_far)/window_size < update_percentage * nb_fragments):
        #             while (len(generation) - generated_so_far)/window_size < update_percentage * nb_fragments:
        #                 gen = []
        #                 # print('\nconcatenating ts: ', ts_index + 1, ', generating ts: ', cpt)
        #                 for i in range(int(len(time_series_data_ori[ts_index])) - 1):
        #                     gen.extend(random.choice(total_query_results[ts_index][i]))
        #
        #                 if (len(gen)%len(ori)) + window_size > len(ori):
        #                     gen = gen[:int(len(ori)*(len(gen)/len(ori) + 1) - window_size)]
        #                     gen.extend(random.choice(total_query_results[ts_index][-1]))
        #                 generation.extend(gen)
        #             generated_so_far = len(generation)
        #             print('len(generation)', len(generation))
        #
        #             # file_object = open(time_file, 'a')
        #             # file_object.write(str(generated_so_far) + ',' + str(time.time() - start_time)+'\n')
        #             # file_object.close()
        #
        #             if (len(generation)/window_size >= gen_ts_length):
        #                 np.savetxt(export_path + "fake_long" + str(cpt) + ".csv", np.array(generation), delimiter=",")
        #                 break
        #             else:
        #                 continue
        #
        #
        #
        #         print('concatenation is done\nexporting one full dataset file begins...')

        # total_generation.append(generation)

        # if conca_plot:
        #     fig, axs = plt.subplots(2, sharex=True)
        #     fig.suptitle('Original vs. Generated data for ' + export_path + str(cpt))
        #
        #     axs[0].plot([i[0] for i in
        #                  np.repeat(np.expand_dims(ori[:, ts_index], axis=0), repeats=gen_ts_length, axis=0).reshape(-1,
        #                                                                                                             1).tolist()])
        #     axs[0].set_title('original data')
        #     axs[1].plot(generation)
        #     axs[1].set_title('generated data')
        #
        #     plt.savefig(export_path + 'ori_vs_generation' + str(cpt) + '.png')

        # file_object = open(export_path+'time_results.txt', 'a')
        # file_object.write("\n--- LSH Time: %s seconds ---" % (time.time() - start_LSH))
        # file_object.close()
        print("--- LSH Time: %s seconds ---" % (time.time() - start_LSH))

        try:
            import os
            full_data = ''.join([export_path + "fake_long" + str(cpt) + ".csv " for cpt in range(gen_ts_dim)])
            os.system("paste " +
                      full_data +
                      "-d ',' > " + export_path + "fake_long_complete.csv")
        except:
            print("couldn't generate one full file")

        # os.system("paste foo.csv  bar.csv -d ',' > output.csv")

        # total_generation = pd.DataFrame(total_generation).T
        # total_generation.to_csv(export_path + "fake_long_complete.csv", index=False, header=False)

        print('\nNumber of non-found windows is: {} (or {}% of the generated data).'.format(non_found_windows,
                                                                                            100 * float(
                                                                                                non_found_windows) / float(
                                                                                                df_ori.shape[
                                                                                                    1] * gen_ts_dim)))
        print('Average hash searching time: ', round((sum(compute_time) / len(compute_time)), 2), 's')

        return time.time() - start_LSH
        # return pd.DataFrame(ori), 'fake_long_complete.csv'

    # def lsh_main_time(self, ori_path, gen_path, export_path, window_size, top_n, tr_sampling_size, conca_plot, num_hashtables, hash_size_percentage,
    #                   update_percentage, nb_fragments, gen_ts_length=0, gen_ts_dim=0):
    #     """
    #     Formats a number (greater than unity) with SI Order of Magnitude
    #     prefixes.
    #
    #     Parameters
    #     ----------
    #     ori_path  : string
    #         Path to the original time series dataset, it can be of any number of time series.
    #
    #         Example:
    #             564,563
    #             730,324LSH
    #             770,135
    #
    #     gen_path  : string
    #         Path to a directory that contains files of the generated time series.
    #
    #         For each time series, a file named 'fake{i}.csv', for example: fake0.csv (for the first time series)
    #             and fake1.csv (for the first time series)
    #
    #         Example:
    #             └── ./gen_path/
    #                 ├── fake0.csv
    #                 ├── fake1.csv
    #                 ├── fake2.csv
    #                 └── fake3.csv
    #
    #             Content of fake0.csv
    #             0,1,2,3....,500
    #             0.36852998,0.36335656,....,0.37748763
    #
    #     export_path  : string
    #         Path of the directory to export the full time series files.
    #
    #         Example of result:
    #             └── ./export_path/
    #                 ├── fake_long0.csv
    #                 ├── fake_long1.csv
    #                 └── fake_long_complete.csv
    #
    #
    #     window_size  : Integer
    #         Size of the generation window
    #
    #
    #     nb_fragments : Integer
    #         Number of the first generate sequences to consider for each time series
    #
    #
    #     Returns
    #     -------
    #     original    : Pandas Dataframe
    #         Dataframe containing full original time series.
    #
    #     total_generation    : Pandas Dataframe
    #         Dataframe containing full generated time series.
    #
    #     """
    #
    #     '''
    #     while True:
    #         GAN()
    #         index()
    #         query()
    #         while(used < 90%)
    #         concat()
    #         if fail_condition:
    #             break
    #     '''
    #     export_path += 'lsh/'
    #     # load original data and create its windows
    #     if tr_sampling_size > window_size:
    #         df = pd.read_csv(ori_path, delimiter=',', header=None, nrows=tr_sampling_size)
    #     else:
    #         df = pd.read_csv(ori_path, delimiter=',', header=None)
    #     # x = np.genfromtxt(ori_path, delimiter=',', dtype=np.float32)
    #     x = df.to_numpy()
    #     x_list = [float(x[i][0]) for i in range(len(x))]
    #     x = np.array(x_list)
    #     ori = (x - x.min()) / (x.max() - x.min())
    #     try:
    #         a = x.shape[1]
    #         del a
    #     except Exception:
    #         x = x.reshape(-1, 1)
    #         ori = ori.reshape(-1, 1)
    #
    #     start_LSH = time.time()
    #     compute_time = []
    #     num_cont = x.shape[1]
    #     generation = []
    #     start_time = time.time()
    #
    #     # time_file = 'lsh_time_bafu.txt'
    #
    #     for ts_index in range(num_cont):
    #         generated_so_far = 0
    #         while True:
    #             # if gen_ts_length >= 2:  # NOT MEMORY EFFICIENT!
    #             #     ori_long = np.repeat(np.expand_dims(ori, axis=0), repeats=gen_ts_length, axis=0).reshape(-1, ori.shape[1])
    #
    #             # total_generation = []
    #             lsh_arr = []
    #             non_found_windows = 0
    #             num_cont = x.shape[1]
    #             # top_n = max(top_n, gen_ts_dim)
    #             # top_n = min(top_n, 10)
    #             time_series_data_fake = []
    #             time_series_data_ori = []
    #             gen_ts_dim = max(gen_ts_dim, num_cont)
    #             total_query_results = []
    #
    #             print('\nindexing the generated time series ')
    #
    #             # indexing generated data
    #
    #
    #             # prepare the hash tables
    #             lsh_arr.append(
    #                 lshash.LSHash(int(window_size * hash_size_percentage / 100), window_size,
    #                               num_hashtables=num_hashtables))
    #
    #             # prepare the windows
    #             df_ori = pd.DataFrame()
    #             for i in range(int(len(ori) / window_size)):
    #                 try:
    #                     df_ori[str(i)] = [i[0] for i in ori[i * window_size:(i + 1) * window_size]]
    #                 except:
    #                     df_ori[str(i)] = [i for i in ori[i * window_size:(i + 1) * window_size]]
    #
    #             # last window_size
    #             if len(ori) % window_size != 0:
    #                 try:
    #                     df_ori[str(int(len(ori) / window_size))] = [i[0] for i in ori[len(ori) - window_size:len(ori)]]
    #                 except:
    #                     df_ori[str(int(len(ori) / window_size))] = [i for i in ori[len(ori) - window_size:len(ori)]]
    #
    #             df_ori.columns = [i for i in range(len(df_ori.columns))]
    #
    #             df_fake = pd.read_csv(gen_path + 'fake' + str(ts_index) + '.csv', header=None)
    #             # df_fake = df_fake.T
    #             # selected_columns = [i for i in range(len(df_fake.columns))]
    #             # if nb_fragments is not None:
    #             #     selected_columns = selected_columns[:nb_fragments]
    #             #     df_fake = df_fake[df_fake.columns.intersection(selected_columns)]
    #
    #             # CREATING Windows
    #             time_series_data_ori.append(self._dataframeToWindows(df_ori, window_size))
    #             time_series_data_fake.append(self._dataframeToWindows(df_fake, window_size))
    #
    #             # Building the Hashing tables for series
    #             print('\nindexing the generated time series ', ts_index + 1)
    #             # for nb_fragments in tqdm(range(100, 3072, 100)):
    #             for i in tqdm(range(nb_fragments)):
    #                 # for i in tqdm(range(int(len(time_series_data_fake[-1])))):
    #                 # for i in tqdm(range(int(len(time_series_data_fake[-1])))):
    #                 lsh_arr[ts_index].index(time_series_data_fake[-1][i][0])
    #             # file_object = open('/Users/abdel/PycharmProjects/ABench-IoT/Generation/stream/hashing/' + time_file, 'a')
    #             # file_object.write(str(nb_fragments) + ',' + str(time.time() - start_time)+'\n')
    #             # file_object.close()
    #
    #
    #             print('indexing is done\n'
    #                   + 'querying begins...')
    #
    #
    #             # for ts_index in range(num_cont):
    #             query_results = []
    #             # print('\nquerying ts: ', ts_index + 1)
    #             start1 = time.time()
    #             for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
    #                 # for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
    #                 counter = 5
    #                 while counter > 0:
    #                     try:
    #                         gen = [j[0][0] for j in
    #                                lsh_arr[ts_index].query(time_series_data_ori[ts_index][i][0], num_results=top_n,
    #                                                        distance_func="euclidean")]
    #                         # print('gen', gen)
    #                         if gen:
    #                             query_results.append(gen)
    #                             break
    #                     except Exception as e:
    #                         pass
    #                         # print('empty output, tries left: ', counter)
    #                     counter -= 1
    #                 if counter == 0:
    #                     non_found_windows += 1
    #                     query_results.append([time_series_data_fake[ts_index][i][0]])
    #
    #             total_query_results.append(query_results)
    #             compute_time.append(time.time() - start1)
    #
    #             # print('\nquerying is done\nconcatenation begins...')
    #
    #             # total_generation= []
    #             # for cpt in tqdm(range(gen_ts_dim), position=0, leave=True):
    #             cpt = ts_index
    #             # ts_index = cpt % num_cont
    #
    #             print('concatenation is done\nexporting one full dataset file begins...')
    #
    #             # for r in range(gen_ts_length):
    #             while (len(generation)/window_size < gen_ts_length and len(generation)/window_size < update_percentage * nb_fragments):
    #                 gen = []
    #                 # print('\nconcatenating ts: ', ts_index + 1, ', generating ts: ', cpt)
    #                 for i in range(int(len(time_series_data_ori[ts_index])) - 1):
    #                     gen.extend(random.choice(total_query_results[ts_index][i]))
    #
    #                 if (len(gen)%len(ori)) + window_size > len(ori):
    #                     gen = gen[:int(len(ori)*(len(gen)/len(ori) + 1) - window_size)]
    #                     gen.extend(random.choice(total_query_results[ts_index][-1]))
    #                 generation.extend(gen)
    #             generated_so_far += len(generation)
    #
    #             # file_object = open(time_file, 'a')
    #             # file_object.write(str(generated_so_far) + ',' + str(time.time() - start_time)+'\n')
    #             # file_object.close()
    #
    #             if (len(generation)/len(ori) >= gen_ts_length):
    #                 np.savetxt(export_path + "fake_long" + str(cpt) + ".csv", np.array(generation), delimiter=",")
    #                 break
    #             else:
    #                 continue
    #         # total_generation.append(generation)
    #
    #         # if conca_plot:
    #         #     fig, axs = plt.subplots(2, sharex=True)
    #         #     fig.suptitle('Original vs. Generated data for ' + export_path + str(cpt))
    #         #
    #         #     axs[0].plot([i[0] for i in
    #         #                  np.repeat(np.expand_dims(ori[:, ts_index], axis=0), repeats=gen_ts_length, axis=0).reshape(-1,
    #         #                                                                                                             1).tolist()])
    #         #     axs[0].set_title('original data')
    #         #     axs[1].plot(generation)
    #         #     axs[1].set_title('generated data')
    #         #
    #         #     plt.savefig(export_path + 'ori_vs_generation' + str(cpt) + '.png')
    #
    #     # file_object = open(export_path+'time_results.txt', 'a')
    #     # file_object.write("\n--- LSH Time: %s seconds ---" % (time.time() - start_LSH))
    #     # file_object.close()
    #     print("--- LSH Time: %s seconds ---" % (time.time() - start_LSH))
    #
    #
    #     try:
    #         import os
    #         full_data = ''.join([export_path + "fake_long" + str(cpt) + ".csv " for cpt in range(gen_ts_dim)])
    #         os.system("paste " +
    #                   full_data +
    #                   "-d ',' > " + export_path + "fake_long_complete.csv")
    #     except:
    #         print("couldn't generate one full file")
    #
    #     # os.system("paste foo.csv  bar.csv -d ',' > output.csv")
    #
    #
    #
    #     # total_generation = pd.DataFrame(total_generation).T
    #     # total_generation.to_csv(export_path + "fake_long_complete.csv", index=False, header=False)
    #
    #     print('\nNumber of non-found windows is: {} (or {}% of the generated data).'.format(non_found_windows,
    #                                                                                         100 * float(
    #                                                                                             non_found_windows) / float(
    #                                                                                             df_ori.shape[
    #                                                                                                 1] * gen_ts_dim)))
    #     print('Average hash searching time: ', round((sum(compute_time) / len(compute_time)), 2), 's')
    #
    #     return time.time() - start_LSH
    #     # return pd.DataFrame(ori), 'fake_long_complete.csv'

    def _chunks(self, l, len_tricklet):
        """Yield successive n-sized _chunks from l."""
        res = []
        for i in range(0, len(l), len_tricklet):
            if (len(l[i:i + len_tricklet]) == len_tricklet):
                res.append(l[i:i + len_tricklet])
        return res

    def _dataframeToWindows(self, data, len_tricklet):
        ts = [[] for i in range(len(data.index))]
        # for column in data:
        for index, row in data.iterrows():
            # print(data[column].tolist())
            # pprint.pprint(list(_chunks(data[column].tolist(), len_tricklet)))
            # ts[data.columns.get_loc(column)].extend(self._chunks(data[column].tolist(), len_tricklet))
            ts[index].extend(self._chunks(row.tolist(), len_tricklet))
        return ts

    # def lsh_main(self, ori_path, gen_path, export_path, window_size, top_n, tr_sampling_size, conca_plot, num_hashtables, hash_size_percentage,
    #              gen_ts_length=0, gen_ts_dim=0):
    #     """
    #     Formats a number (greater than unity) with SI Order of Magnitude
    #     prefixes.
    #
    #     Parameters
    #     ----------
    #     ori_path  : string
    #         Path to the original time series dataset, it can be of any number of time series.
    #
    #         Example:
    #             564,563
    #             730,324LSH
    #             770,135
    #
    #     gen_path  : string
    #         Path to a directory that contains files of the generated time series.
    #
    #         For each time series, a file named 'fake{i}.csv', for example: fake0.csv (for the first time series)
    #             and fake1.csv (for the first time series)
    #
    #         Example:
    #             └── ./gen_path/
    #                 ├── fake0.csv
    #                 ├── fake1.csv
    #                 ├── fake2.csv
    #                 └── fake3.csv
    #
    #             Content of fake0.csv
    #             0,1,2,3....,500
    #             0.36852998,0.36335656,....,0.37748763
    #
    #     export_path  : string
    #         Path of the directory to export the full time series files.
    #
    #         Example of result:
    #             └── ./export_path/
    #                 ├── fake_long0.csv
    #                 ├── fake_long1.csv
    #                 └── fake_long_complete.csv
    #
    #
    #     window_size  : Integer
    #         Size of the generation window
    #
    #
    #     nb_fragments : Integer
    #         Number of the first generate sequences to consider for each time series
    #
    #
    #     Returns
    #     -------
    #     original    : Pandas Dataframe
    #         Dataframe containing full original time series.
    #
    #     total_generation    : Pandas Dataframe
    #         Dataframe containing full generated time series.
    #
    #     """
    #
    #     # load original data and create its windows
    #     export_path +=  'lsh/'
    #
    #     if tr_sampling_size > window_size:
    #         df = pd.read_csv(ori_path, delimiter=',', header=None, nrows=tr_sampling_size)
    #     else:
    #         df = pd.read_csv(ori_path, delimiter=',', header=None)
    #     # x = np.genfromtxt(ori_path, delimiter=',', dtype=np.float32)
    #     x = df.to_numpy()
    #
    #     ori = (x - x.min()) / (x.max() - x.min())
    #
    #     try:
    #         a = x.shape[1]
    #         del a
    #     except Exception:
    #         x = x.reshape(-1, 1)
    #         ori = ori.reshape(-1, 1)
    #
    #     # if gen_ts_length >= 2:  # NOT MEMORY EFFICIENT!
    #     #     ori_long = np.repeat(np.expand_dims(ori, axis=0), repeats=gen_ts_length, axis=0).reshape(-1, ori.shape[1])
    #
    #     # total_generation = []
    #     lsh_arr = []
    #
    #     non_found_windows = 0
    #
    #     num_cont = x.shape[1]
    #
    #     # top_n = max(top_n, gen_ts_dim)
    #     # top_n = min(top_n, 10)
    #
    #     compute_time = []
    #
    #     time_series_data_fake = []
    #     time_series_data_ori = []
    #
    #     gen_ts_dim = max(gen_ts_dim, num_cont)
    #
    #     start_LSH = time.time()
    #
    #     print('\nindexing the generated time series ')
    #
    #     # indexing generated data
    #     for ts_index in range(num_cont):
    #         # prepare the hash tables
    #         lsh_arr.append(
    #             lshash.LSHash(int(window_size * hash_size_percentage / 100), window_size,
    #                           num_hashtables=num_hashtables))
    #
    #         # prepare the windows
    #         df_ori = pd.DataFrame()
    #         for i in range(int(len(ori) / window_size)):
    #             try:
    #                 df_ori[str(i)] = [i[0] for i in ori[i * window_size:(i + 1) * window_size]]
    #             except:
    #                 df_ori[str(i)] = [i for i in ori[i * window_size:(i + 1) * window_size]]
    #
    #         # last window_size
    #         if len(ori) % window_size != 0:
    #             try:
    #                 df_ori[str(int(len(ori) / window_size))] = [i[0] for i in ori[len(ori) - window_size:len(ori)]]
    #             except:
    #                 df_ori[str(int(len(ori) / window_size))] = [i for i in ori[len(ori) - window_size:len(ori)]]
    #
    #         df_ori.columns = [i for i in range(len(df_ori.columns))]
    #
    #         df_fake = pd.read_csv(gen_path + 'fake' + str(ts_index) + '.csv', header=None)
    #         selected_columns = [i for i in range(len(df_fake.columns))]
    #         # if nb_fragments is not None:
    #         #     selected_columns = selected_columns[:nb_fragments]
    #         #     df_fake = df_fake[df_fake.columns.intersection(selected_columns)]
    #
    #         # CREATING Windows
    #         time_series_data_fake.append(self._dataframeToWindows(df_fake, window_size))
    #         time_series_data_ori.append(self._dataframeToWindows(df_ori, window_size))
    #
    #         # Building the Hashing tables for series
    #         # print('\nindexing the generated time series ', ts_index + 1)
    #         for i in tqdm(range(int(len(time_series_data_fake[-1])))):
    #             # for i in tqdm(range(int(len(time_series_data_fake[-1])))):
    #             lsh_arr[ts_index].index(time_series_data_fake[-1][i][0])
    #
    #     print('indexing is done\n'
    #           + 'querying begins...')
    #     total_query_results = []
    #     for ts_index in range(num_cont):
    #         query_results = []
    #         # print('\nquerying ts: ', ts_index + 1)
    #         start1 = time.time()
    #         for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
    #             # for i in tqdm(range(int(len(time_series_data_ori[ts_index])))):  # - 1)):
    #             counter = 5
    #             while counter > 0:
    #                 try:
    #                     gen = [j[0][0] for j in
    #                            lsh_arr[ts_index].query(time_series_data_ori[ts_index][i][0], num_results=top_n,
    #                                                    distance_func="euclidean")]
    #                     # print('gen', gen)
    #                     if gen:
    #                         query_results.append(gen)
    #                         break
    #                 except Exception as e:
    #                     pass
    #                     # print('empty output, tries left: ', counter)
    #                 counter -= 1
    #             if counter == 0:
    #                 non_found_windows += 1
    #                 query_results.append([time_series_data_ori[ts_index][i][0]])
    #
    #         total_query_results.append(query_results)
    #         compute_time.append(time.time() - start1)
    #
    #     print('\nquerying is done\nconcatenation begins...')
    #     # total_generation= []
    #     for cpt in tqdm(range(gen_ts_dim), position=0, leave=True):
    #         ts_index = cpt % num_cont
    #         generation = []
    #
    #         for r in range(gen_ts_length):
    #             gen = []
    #             # print('\nconcatenating ts: ', ts_index + 1, ', generating ts: ', cpt)
    #             for i in range(int(len(time_series_data_ori[ts_index])) - 1):
    #                 gen.extend(random.choice(total_query_results[ts_index][i]))
    #
    #             if len(gen) + window_size > len(ori):
    #                 gen = gen[:len(ori) - window_size]
    #                 gen.extend(random.choice(total_query_results[ts_index][-1]))
    #             generation.extend(gen)
    #
    #
    #         np.savetxt(export_path + "fake_long" + str(cpt) + ".csv", np.array(generation), delimiter=",")
    #         # total_generation.append(generation)
    #
    #         if conca_plot:
    #             fig, axs = plt.subplots(2, sharex=True)
    #             fig.suptitle('Original vs. Generated data for ' + export_path + str(cpt))
    #
    #             axs[0].plot([i[0] for i in
    #                          np.repeat(np.expand_dims(ori[:, ts_index], axis=0), repeats=gen_ts_length, axis=0).reshape(-1,
    #                                                                                                                     1).tolist()])
    #             axs[0].set_title('original data')
    #             axs[1].plot(generation)
    #             axs[1].set_title('generated data')
    #
    #             plt.savefig(export_path + 'ori_vs_generation' + str(cpt) + '.png')
    #
    #     print('concatenation is done\nexporting one full dataset file begins...')
    #     LSH_time = time.time() - start_LSH
    #     # file_object = open(export_path+'time_results.txt', 'a')
    #     # file_object.write("\n--- LSH Time: %s seconds ---" % (time.time() - start_LSH))
    #     # file_object.close()
    #     print("--- LSH Time: %s seconds ---" % (LSH_time))
    #
    #     try:
    #         import os
    #         full_data = ''.join([export_path + "fake_long" + str(cpt) + ".csv " for cpt in range(gen_ts_dim)])
    #         os.system("paste " +
    #                   full_data +
    #                   "-d ',' > " + export_path + "fake_long_complete.csv")
    #     except:
    #         print("couldn't generate one full file")
    #
    #     # os.system("paste foo.csv  bar.csv -d ',' > output.csv")
    #
    #
    #
    #     # total_generation = pd.DataFrame(total_generation).T
    #     # total_generation.to_csv(export_path + "fake_long_complete.csv", index=False, header=False)
    #
    #     print('\nNumber of used original windows is: {} (or {}% of the generated data).'.format(non_found_windows,
    #                                                                                             100 * float(
    #                                                                                                 non_found_windows) / float(
    #                                                                                                 df_ori.shape[
    #                                                                                                     1] * gen_ts_dim)))
    #     print('Average hash searching time: ', round((sum(compute_time) / len(compute_time)), 2), 's')
    #
    #     return LSH_time
    #     # return pd.DataFrame(ori), 'fake_long_complete.csv'

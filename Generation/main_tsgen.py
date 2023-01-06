import traceback
import warnings

warnings.filterwarnings("ignore")

import json
import multiprocessing as multiprocessing
import os
import warnings
import matplotlib

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
import matplotlib.pyplot as plt
import pandas as pd
from gan.infogan import train, generate


# def normalize_original_data(data_path):
#     original = np.genfromtxt(data_path, delimiter=',', dtype=np.float32)
#     # original = original[1:]
#     # normalize data
#     original = (original - original.min()) / (original.max() - original.min())
#     # print (original)
#     # print('data normalized')
#     return original

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def plot_dataframe(df, xlabdel='', ylabel='', exportPath='plot.png'):
    plt.figure()
    plt.plot(df)
    plt.legend()
    plt.ylabel(xlabdel)
    plt.xlabel(ylabel)
    plt.savefig(exportPath)


# def plot_file(file, exportPath):
#     df = pd.read_csv(file)
#     if 'timestamp' in df.columns:
#         df = df.drop(columns='timestamp', axis=1)
#     plot_dataframe(df, exportPath=exportPath)


# def load_input_data(data_path, window, exportPath, shift, num_cont):
#     x = np.genfromtxt(data_path, delimiter=',', dtype=np.float32)
#     # normalize data
#     x = x[1:, x.shape[1] - num_cont:]
#     x = (x - x.min()) / (x.max() - x.min())
#     # ori = np.array([i[0] for i in x])
#     # delete zero pad data
#     n = ((np.where(np.any(x, axis=1))[0][-1] + 1) // window) * window
#
#     # # normalize data between 0 and 1
#     # scaler.fit(x[:n])
#     # x = scaler.transform(x[:n])
#
#     # make to matrix
#     # X = np.asarray([x[i:i + window] for i in range(n - window)])
#     X = np.asarray([x[i:i + window] for i in range(0, n - window + 1, shift)])
#
#     np.random.shuffle(X)
#     if X.shape[1] == 1:
#         X = X.reshape(X.shape[0], X.shape[1])
#
#     pd = pandas.DataFrame(X)
#     pd = pd.T
#
#     nbplots = min(10, int(pd.shape[1]))
#     # plot result
#     _, ax = plt.subplots(nbplots, nbplots, sharex=True, sharey=True)
#     for i in range(nbplots):
#         for j in range(nbplots):
#             try:
#                 ax[i][j].plot(pd.iloc[:, i * nbplots + j], linewidth=1)
#             except:
#                 print("plotting out of bound:", i, j, pd.shape)
#     plt.savefig(exportPath + "original_ts_windows.png", dpi=1500)
#     pd.columns = [i for i in range(len(pd.columns))]
#     pd.to_csv(exportPath + "original_ts_windows.csv")
#     return pd, ori


if __name__ == "__main__":

    # load parameters
    with open("./parameters.json", "r") as f:
        queue_fake = multiprocessing.Queue()
        para_dict = json.load(f)
        data_paths = para_dict["input_data_path"]  # dataset path
        window = para_dict["window"]
        model_path = para_dict["model_path"]  # model path
        autocorr_lag = int(para_dict["autocorr_lag"])  # model path
        # batch_size_generation = para_dict["batch_size_generation"]  # batch_size_generation
        winShift = para_dict["winShift"]
        winShift = [i for i in range(winShift[0], winShift[1], winShift[2])]
        # num_cont = para_dict["num_cont"]
        bool_train = para_dict["train"] == 1
        bool_generate = para_dict["generate"] == 1
        # bool_MP = para_dict["MP"] == 1
        bool_LSH = para_dict["lsh_conca"] == 1
        bool_metrics = para_dict["bool_metrics"] == 1
        gen_ts_length = para_dict["gen_ts_length"]
        if gen_ts_length < 2: gen_ts_length = 1
        gen_ts_dim = para_dict["gen_ts_dim"]
        nb_fragments = para_dict["nb_fragments"]
        top_n = 0.01 * nb_fragments
        sampling_size = para_dict["sampling_size"]
        train_ep = para_dict["train_ep"]
        conca_plot = para_dict["conca_plot"] == 1
        num_hashtables = para_dict["num_hashtables"]
        hash_size_percentage = para_dict["hash_size_percentage"]


    for data_path in data_paths:
        print("(dataset: " + data_path)
        df = pd.read_csv(data_path, header=None, nrows= 2)
        num_cont = df.shape[1]
        del df
        data_length = file_len(data_path)
        if sampling_size < window:
            sampling_size = data_length
        if gen_ts_dim < num_cont:
            gen_ts_dim = num_cont
        # train_ep = para_dict["train_ep"] * num_cont
        # train_ep = 1

        batch_size_generation = int((sampling_size / window) * 200)


        res_metrics = []
        for shift in winShift:
            try:
                # create folders
                from pathlib import Path

                export_path = './results/' + Path(data_path).stem + '/' + 'win=' + str(window) \
                              + '_ep=' + str(train_ep) +  '/' \
                              + 'sampling_size=' + str(sampling_size) + '/'
                # \
                #               + 'gen_ts_length=' + str(gen_ts_length) + '/' \
                #               + 'gen_ts_dim=' + str(gen_ts_dim)
                try:
                    os.makedirs(export_path)
                except Exception as e:
                    print(e)

                # plot original data
                # original, ori_full = load_input_data(data_path, window, export_path, shift, num_cont)

                # train
                if bool_train:
                    print('training size: ', sampling_size)
                    # input_data = load_input_data(data_path)
                    # train.main(data_path, export_path + "model/train/", shift)
                    p = multiprocessing.Process(target=train.main,
                                                args=(
                                                    data_path, export_path + "model/train/", shift, num_cont, train_ep, sampling_size))
                    p.start()
                    p.join()

                # generate
                if bool_generate:
                    generator = generate.Generator(export_path + "model/train/", batch_size_generation, num_cont)
                    processus_generate = multiprocessing.Process(target=generator.generate,
                                                                 args=(queue_fake,))
                    # args=(queue_fake_list[i], queue_classfied_list[i],)))
                    print('generating .. ')
                    processus_generate.start()
                    fake = queue_fake.get()
                    processus_generate.join()
                    print('done\nexporting .. ')
                    generator.export(fake)
                    print('done.')

                # Hashing for long time series
                if bool_LSH:
                    import stream.hashing.lsh_main as lsh
                    lsh = lsh.LSH_conca()
                    time = lsh.lsh_main(data_path, export_path + model_path, export_path, window, top_n,
                                                   sampling_size, conca_plot, num_hashtables, hash_size_percentage, None,
                                                   gen_ts_length=gen_ts_length, gen_ts_dim=gen_ts_dim)
                    print('LSH time : %s', time)
                    # lsh.lsh_main(data_path, export_path + model_path, export_path, window)

                    # ori, generation = lsh.main(export_path, data_path, export_path + model_path, )

                    # ori, generation = lsh.main(export_path, data_path, export_path + model_path, num_cont,
                    #                           batch_size_generation, learn=False)

                    # compute metrics between original vs generated time series & compare :

                    # NMI, MI, Dist, Autocorr, RMSE

                if bool_metrics and gen_ts_length < 2 and gen_ts_dim == num_cont:
                    print('computing metrics... ')
                    import metrics.metrics as metr

                    re = metr.run(ori, generation, export_path, autocorr_lag)
                    # re["shift"] = shift
                    print(re)
                    res_metrics.append(re)

                # gen_infogan = pd.read_csv(export_path + 'model/train/fake.csv')

                # print(original.shape)
                # print(gen_infogan.shape)
            except Exception as exception:
                traceback.print_exc()

        if bool_metrics and gen_ts_length < 2 and gen_ts_dim == num_cont:
            # export metrics
            all_metrics = pd.DataFrame(res_metrics)
            all_metrics.to_csv('./results/' + Path(data_path).stem + '/' + 'win=' + str(window) \
                               + '_ep=' + str(train_ep) + '_nbTS=' + str(batch_size_generation) + '/' + "metrics.csv")
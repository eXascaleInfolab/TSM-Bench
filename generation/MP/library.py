import pandas
import numpy as np
import matplotlib.pyplot as plt


def save_object(obj, filename):
    try:
        import cPickle as pickle
    except ModuleNotFoundError:
        import pickle

    # dirname = os.path.dirname(filename)
    # if not os.path.exists(dirname):
    #     os.makedirs(dirname)

    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    try:
        import cPickle as pickle
    except ModuleNotFoundError:
        import pickle
    with open(filename, 'rb') as input:  # Overwrites any existing file.
        obj = pickle.load(input)
        return obj


def chunks(l, len_tricklet):
    """Yield successive n-sized chunks from l."""
    res = []
    for i in range(0, len(l), len_tricklet):
        if (len(l[i:i + len_tricklet]) == len_tricklet):
            res.append(l[i:i + len_tricklet])
    return res


def dataframeToTricklets(data, len_tricklet):
    ts = [[] for i in range(len(data.columns))]
    for column in data:
        # print(data[column].tolist())
        # pprint.pprint(list(chunks(data[column].tolist(), len_tricklet)))
        ts[data.columns.get_loc(column)].extend(chunks(data[column].tolist(), len_tricklet))



    return ts


def learnDictionary(X, nbAtoms, alpha, n_iter, fname):
    from sklearn.decomposition import DictionaryLearning
    # , fit_algorithm = 'lars', 'cd'
    dico = DictionaryLearning(n_components=nbAtoms, alpha=alpha, max_iter=n_iter)

    D = dico.fit(X).components_
    save_object(D, fname)
    return D


def sparse_code_without_correlation(ts, Dictionary, nonzero_coefs, transform_algorithm):
    from sklearn.decomposition import SparseCoder

    coder = SparseCoder(dictionary=Dictionary, transform_n_nonzero_coefs=nonzero_coefs
                        , transform_algorithm=transform_algorithm)

    # For each time series, for each tricklet, transform the tricklet and store it
    result = []
    for t in ts:
        result.append(coder.transform(t))

    # transformation of result to [id_A, coef_A]
    tricklets = []
    for index in range(len(result)):
        temp = []
        for t in range(result[index].shape[0]):
            x = []
            for i, e in enumerate(result[index][t]):
                if e != 0:
                    x.append([i, e])
            temp.append(x)
        tricklets.append(temp)

    for index in range(len(result)):
        tricklets[index] = np.array([np.array(xi) for xi in tricklets[index]])

    return tricklets


def reconstructDataMulti_without_correlation(sparseData, Dictionary):
    # sparseData [n, m] : n = tricklets number; m: nb atoms
    # Dictionary [n, m] : n = tricklet length; m: nb atoms
    # print(result.shape)
    # print(sparseData.shape)
    # print(Dictionary.T.shape)
    result = []
    # result = [[] for i in range(len(sparseData))]
    # print(sparseData)
    for index in range(len(sparseData)):
        out = []
        # print(sparseData[index])
        # print()
        for t in range(sparseData[index].shape[0]):
            # print(t)
            sum = np.zeros(Dictionary.T.shape[0])

            for i, e in sparseData[index][t]:
                # print(Dictionary.T[:,int(i)])
                # print(e)
                # print('\n')
                sum += Dictionary.T[:, int(i)] * e

            out.append(sum.tolist())
            # print(out)
        # print(out)
        result.append(out)
        # print(result)

        # out.append(np.sum(Dictionary.T * sparseData[n], axis=1))

    # print(len(out))
    # print(len(result[0]))
    return result


def normalized(ts):
    # pop = np.array([np.array(xi) for xi in ts])
    # return (pop - np.min(pop)) / (np.max(pop) - np.min(pop))
    from scipy import stats
    return stats.zscore(ts)


def calculate_RMSE(orig_sig, reconstructed_sig):
    return (np.square(np.array(orig_sig) - np.array(reconstructed_sig))).mean(axis=None)


def compress_without_correlation(ts, Dictionary, nbAtoms, transform_algorithm):
    # Transforming test data into sparse representation using the transform algorithm
    print("Transforming test data into sparse representation without correlation ... ", end='')
    sparseData = sparse_code_without_correlation(ts, Dictionary, nbAtoms, transform_algorithm)
    # print(atoms_coded_tricklets)
    print("done!")

    print("Reconstructing data...", end="")
    recons = reconstructDataMulti_without_correlation(sparseData, Dictionary)
    print("done!")
    # print(recons)
    errors = []
    # print("Error's norm of the correlation-aware method: ", end="")
    for i in range(len(ts)):
        errors.append(calculate_RMSE(ts[i], recons[i]))
        # errors.append(np.square(np.array(normalized(ts[i]) - np.array(normalized(recons[i]))) ** 2).mean(axis=None))

        # for j in range(len(ts[i])):
        #     plt.plot(ts[i][j])
        #     plt.plot(recons[i][j])
        #     plt.title(str(i) + str(j))
        # plt.show()

        # errors.append(calculate_RMSE(ts[i], np.array(recons[i])))
    # print(errors)
    # print(len(recons))
    return sparseData, recons, errors


def runSparseCoder(Dictionary, test_data, nonzero_coefs, transform_algorithm):
    from sklearn.decomposition import SparseCoder

    coder = SparseCoder(dictionary=Dictionary, transform_n_nonzero_coefs=nonzero_coefs,
                        transform_alpha=None, transform_algorithm=transform_algorithm)

    print('test_data')
    print(test_data)
    result = coder.transform(test_data)

    tricklets = []
    # tricklets = np.array([np.array([[i,e] for i, e in enumerate(result[t]) if e != 0 for t in range(result.shape[0])])])

    for t in range(result.shape[0]):
        x = []
        for i, e in enumerate(result[t]):
            if e != 0:
                x.append([i, e])

        # print(type(x))
        tricklets.append(x)
        # tricklets= np.append(tricklets, np.array([[i, e] for i, e in enumerate(result[t]) if e != 0]))

    # print(tricklets)
    # print("result size: " + str( *jnu9n *juuricklets.shape))
    # print("result")
    tricklets = np.array([np.array(xi) for xi in tricklets])
    # np.set_printoptions(threshold=np.inf)
    # print(tricklets)
    # print(result)
    # print(result.shape)
    return tricklets


# print('fake:', df_fake.head(1))

def load_input_dataA(data_path, window, exportPath):
    x = np.genfromtxt(data_path, delimiter=',', dtype=np.float32)
    # normalize data
    # x = x[1:, 1:]
    x = (x - x.min()) / (x.max() - x.min())

    # delete zero pad data
    n = ((np.where(np.any(x, axis=1))[0][-1] + 1) // window) * window

    # # normalize data between 0 and 1
    # scaler.fit(x[:n])
    # x = scaler.transform(x[:n])

    # make to matrix
    X = np.asarray([x[i:i + window] for i in range(0, n - window, window)])
    # np.random.shuffle(X)
    X = X.reshape(X.shape[0], X.shape[1])

    pd = pandas.DataFrame(X)
    pd = pd.T

    nbplots = min(10, int(pd.shape[0]))
    pd.columns = [i for i in range(len(pd.columns))]
    pd.to_csv("original.csv")
    return pd


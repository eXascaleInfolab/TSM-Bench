import os
import random
import warnings
from math import sqrt

from dtw import accelerated_dtw
from numpy import pi
from scipy import ndimage
from scipy.integrate._bvp import EPS
from scipy.linalg import det
from scipy.special import gamma, psi
from scipy.stats import pearsonr, spearmanr
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors

warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
import pandas as pd
from mjc import MJC
import sys


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def nearest_distances(X, k=1):
    '''
    X = array(N,M)
    N = number of points
    M = number of dimensions
    returns the distance to the kth nearest neighbor for every point in X
    '''
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(X)
    d, _ = knn.kneighbors(X)  # the first nearest neighbor is itself
    return d[:, -1]  # returns the distance to the kth nearest neighbor


def entropy_gaussian(C):
    '''
    Entropy of a gaussian variable with covariance matrix C
    '''
    if np.isscalar(C):  # C is the variance
        return .5 * (1 + np.log(2 * pi)) + .5 * np.log(C)
    else:
        n = C.shape[0]  # dimension
        return .5 * n * (1 + np.log(2 * pi)) + .5 * np.log(abs(det(C)))


def entropy_gaussian(C):
    '''
    Entropy of a gaussian variable with covariance matrix C
    '''
    if np.isscalar(C):  # C is the variance
        return .5 * (1 + np.log(2 * pi)) + .5 * np.log(C)
    else:
        n = C.shape[0]  # dimension
        return .5 * n * (1 + np.log(2 * pi)) + .5 * np.log(abs(det(C)))


def entropy(X, k=1):
    ''' Returns the entropy of the X.
    Parameters
    ===========
    X : array-like, shape (n_samples, n_features)
        The data the entropy of which is computed
    k : int, optional
        number of nearest neighbors for density estimation
    Notes
    ======
    Kozachenko, L. F. & Leonenko, N. N. 1987 Sample estimate of entropy
    of a random vector. Probl. Inf. Transm. 23, 95-101.
    See also: Evans, D. 2008 A computationally efficient estimator for
    mutual information, Proc. R. Soc. A 464 (2093), 1203-1215.
    and:
    Kraskov A, Stogbauer H, Grassberger P. (2004). Estimating mutual
    information. Phys Rev E 69(6 Pt 2):066138.
    '''

    # Distance to kth nearest neighbor
    r = nearest_distances(X, k)  # squared distances
    n, d = X.shape
    volume_unit_ball = (pi ** (.5 * d)) / gamma(.5 * d + 1)
    '''
    F. Perez-Cruz, (2008). Estimation of Information Theoretic Measures
    for Continuous Random Variables. Advances in Neural Information
    Processing Systems 21 (NIPS). Vancouver (Canada), December.
    return d * mean(log(r))+log(volume_unit_ball)+log(n-1)-log(k)
    '''
    return (d * np.mean(np.log(r + np.finfo(X.dtype).eps)) +
            np.log(volume_unit_ball) + psi(n) - psi(k))


def mutual_information_2d(x, y, sigma=1, normalized=False):
    """
    Computes (normalized) mutual information between two 1D variate from a
    joint histogram.
    Parameters
    ----------
    x : 1D array
        first variable
    y : 1D array
        second variable
    sigma: float
        sigma for Gaussian smoothing of the joint histogram
    Returns
    -------
    nmi: float
        the computed similariy measure
    """
    bins = (256, 256)

    jh = np.histogram2d(x, y, bins=bins)[0]

    # smooth the jh with a gaussian filter of given sigma
    ndimage.gaussian_filter(jh, sigma=sigma, mode='constant',
                            output=jh)

    # compute marginal histograms
    jh = jh + EPS
    sh = np.sum(jh)
    jh = jh / sh
    s1 = np.sum(jh, axis=0).reshape((-1, jh.shape[0]))
    s2 = np.sum(jh, axis=1).reshape((jh.shape[1], -1))

    # Normalised Mutual Information of:
    # Studholme,  jhill & jhawkes (1998).
    # "A normalized entropy measure of 3-D medical image alignment".
    # in Proc. Medical Imaging 1998, vol. 3338, San Diego, CA, pp. 132-143.
    if normalized:
        mi = ((np.sum(s1 * np.log(s1)) + np.sum(s2 * np.log(s2)))
              / np.sum(jh * np.log(jh))) - 1
    else:
        mi = (np.sum(jh * np.log(jh)) - np.sum(s1 * np.log(s1))
              - np.sum(s2 * np.log(s2)))

    return mi


def mutual_information(variables, k=1):
    '''
    Returns the mutual information between any number of variables.
    Each variable is a matrix X = array(n_samples, n_features)
    where
      n = number of samples
      dx,dy = number of dimensions
    Optionally, the following keyword argument can be specified:
      k = number of nearest neighbors for density estimation
    Example: mutual_information((X, Y)), mutual_information((X, Y, Z), k=5)
    '''
    if len(variables) < 2:
        raise AttributeError(
            "Mutual information must involve at least 2 variables")
    all_vars = np.hstack(variables)
    return (sum([entropy(X, k=k) for X in variables]) -
            entropy(all_vars, k=k))


def test_mutual_information_2d():
    # Mutual information between two correlated gaussian variables
    # Entropy of a 2-dimensional gaussian variable
    n = 50000
    rng = np.random.RandomState(0)
    # P = np.random.randn(2, 2)
    P = np.array([[1, 0], [.9, .1]])
    C = np.dot(P, P.T)
    U = rng.randn(2, n)
    Z = np.dot(P, U).T
    X = Z[:, 0]
    X = X.reshape(len(X), 1)
    Y = Z[:, 1]
    Y = Y.reshape(len(Y), 1)
    # in bits
    MI_est = mutual_information_2d(X.ravel(), Y.ravel())
    MI_th = (entropy_gaussian(C[0, 0]) +
             entropy_gaussian(C[1, 1]) -
             entropy_gaussian(C))
    print(MI_est, MI_th)
    # Our estimator should undershoot once again: it will undershoot more
    # for the 2D estimation that for the 1D estimation
    np.testing.assert_array_less(MI_est, MI_th)
    np.testing.assert_array_less(MI_th, MI_est + .2)

# def autocorr(x):
#     result = np.correlate(x, x, mode='full')
#     return result[result.size/2:]

def run(ori, gen, exportPath, autocorr_lag):
    metrics = {}
    # print('hello')
    metrics['rmse'] = []
    metrics['pcorr'] = []
    metrics['scorr'] = []
    metrics['NMI'] = []
    metrics['ano_original'] = []
    metrics['ano_generated'] = []
    # metrics['ano_distance'] = []

    for col_ori in range(ori.shape[1]):
        original = ori.iloc[:,col_ori]
        generated = gen.iloc[:,col_ori]

        from sklearn.metrics import mean_squared_error
        metrics['rmse'].append(float(sqrt(mean_squared_error(original, generated))))
        # print('RMSE: %f' % metrics['rmse'])  # # original = original.iloc[0]

        # metrics['DTW'], cost_matrix, acc_cost_matrix, path = float(accelerated_dtw(np.array(original), np.array(generated),
        #                                                                      dist='euclidean'))
        # # print('DTW Distance: %f' % metrics['DTW'])
        #
        # with HiddenPrints():
        #     metrics['MJC'], _ = float(MJC(original, generated))
        # # metrics['MJC'], _ =  1, 1
        #
        metrics['pcorr'].append(float(pearsonr(original, generated)[0]))
        # # # print('Pearsons correlation: %.3f' % metrics['pcorr'])
        # #
        metrics['scorr'].append(float(spearmanr(original, generated)[0]))
        # # # print('Spearmans correlation: %.3f' % metrics['scorr'])
        # #
        metrics['NMI'].append(float(mutual_information_2d(np.array(original), np.array(generated), sigma=1, normalized=False)))
        # # # print('NMI: %.3f' % metrics['NMI'])
        # #
        # plt.clf()
        # plt.title("Autocorrelation Plot")
        # plt.xlabel("Lags")
        # plt.acorr(generated, maxlags = 10)
        # plt.grid(True)
        # plt.savefig(exportPath + "autocorr_generated.png")
        # plt.clf()

        from statsmodels.graphics import tsaplots
        import matplotlib.pyplot as plt

        plt.clf()
        fig = tsaplots.plot_acf(generated, lags=autocorr_lag)
        plt.savefig(exportPath + "autocorr_generated.png")
        plt.clf()
        fig = tsaplots.plot_acf(original, lags=autocorr_lag)
        plt.savefig(exportPath + "autocorr_original.png")
        plt.clf()
        # plt.title("Autocorrelation Plot")
        # plt.xlabel("Lags")
        # plt.acorr(original, maxlags = 10)
        # plt.grid(True)
        # plt.savefig(exportPath + "autocorr_ori.png")


        # metrics['Skewness ori'] = float(pd.DataFrame(original).skew())
        # metrics['Skewness gen'] = float(pd.DataFrame(generated).skew())
        # metrics['Kurtosis ori'] = float(pd.DataFrame(original).kurt())
        # metrics['Kurtosis gen'] = float(pd.DataFrame(generated).kurt())
        # # print("Skewness: %f" % df.skew())
        # # print("Kurtosis: %f" % df.kurt())
        #
        metrics['ano_original'].append(anomaly_score(pd.Series(original)))
        # # # print('ano_original: %.3f' % metrics['ano_original'])

        metrics['ano_generated'].append(float(anomaly_score(pd.Series(generated))))
        # print('ano_generated: %.3f' % metrics['ano_generated'])

        # metrics['ano_distance'].append(abs(metrics['ano_original'] - metrics['ano_generated']))
        # print('ano_distance: %.3f' % metrics['ano_distance'])

    metrics['rmse'] = sum(metrics['rmse']) / len(metrics['rmse'])
    metrics['pcorr'] = sum(metrics['pcorr']) / len(metrics['pcorr'])
    metrics['scorr'] = sum(metrics['scorr']) / len(metrics['scorr'])
    metrics['NMI'] = sum(metrics['NMI']) / len(metrics['NMI'])
    metrics['ano_original'] = sum(metrics['ano_original']) / len(metrics['ano_original'])
    metrics['ano_generated'] = sum(metrics['ano_generated']) / len(metrics['ano_generated'])
    # metrics['ano_distance'] = sum(metrics['ano_distance']) / len(metrics['ano_distance'])

    return metrics


def runWindow(original, gen_infogan, gen_anogen, export_path=''):
    #  compares single ramdomly picked windows
    export_path = export_path + 'runWindow/'
    try:
        # os.makedirs(export_path)
        os.makedirs(export_path + 'distribution/')
    except:
        pass

    plot_dist_univariate_dataset(original, export_path + 'distribution/original')
    plot_dist_univariate_dataset(gen_infogan, export_path + 'distribution/gen_infogan')
    plot_dist_univariate_dataset(gen_anogen, export_path + 'distribution/gen_anogen')

    gen_infogan = gen_infogan.iloc[:, 0].tolist()
    gen_anogen = gen_anogen.iloc[:, 0].tolist()[:len(gen_infogan)]
    original = original.tolist()
    idx = random.randint(0, len(original) - len(gen_infogan) - 1)
    original = original[idx:idx + len(gen_infogan)]
    try:
        original = [original[i][0] for i in range(len(original))]
    except:
        pass

    plt.figure()
    plt.plot(original, label='original')
    plt.plot(gen_infogan, label='gen_infogan')
    plt.plot(gen_anogen, label='gen_anogen')
    plt.legend(loc="upper left")
    plt.savefig(export_path + 'original_vs_infogan_vs_anogen.png')
    plt.close()

    metricsInfoGAN = run(original, gen_infogan)
    metricsAnoGEN = run(original, gen_anogen)

    metrics = pd.DataFrame([metricsInfoGAN, metricsAnoGEN], index=['AnoGEN', 'infogan'])
    # normalize DTW column
    metrics["DTW"] = (metrics["DTW"] / metrics["DTW"].mean())
    metrics["MJC"] = (metrics["MJC"] / metrics["MJC"].mean())

    metrics = metrics.astype(float)

    metrics = metrics.T

    metrics.plot.bar()

    metrics.to_csv(export_path + 'metrics.csv')
    plt.savefig(export_path + 'metrics.png')
    plt.close()


def runMultiWindows(original, gen_infogan, gen_anogen, export_path=''):
    #  compares multiple windows

    export_path = export_path + 'runMultiWindows/'
    try:
        # os.makedirs(export_path)
        os.makedirs(export_path + 'distribution/')
    except:
        pass

    plot_dist_univariate_dataset(original, export_path + 'distribution/original')
    plot_dist_univariate_dataset(gen_infogan, export_path + 'distribution/gen_infogan')
    plot_dist_univariate_dataset(gen_anogen, export_path + 'distribution/gen_anogen')

    # gen_infogan = gen_infogan.iloc[:, 0].tolist()
    # gen_anogen = gen_anogen.iloc[:, 0].tolist()[:len(gen_infogan)]
    original = original.tolist()
    idx = random.randint(0, len(original) - len(gen_infogan) - 1)
    original = original[idx:idx + len(gen_infogan)]
    try:
        original = [original[i][0] for i in range(len(original))]
    except:
        pass
    # plot windows

    figure, axes = plt.subplots(nrows=3, ncols=1, figsize=(20, 10))
    pd.Series(original).plot(ax=axes[0], label='original')
    gen_infogan.plot(ax=axes[1], label='gen_infogan')
    gen_anogen.plot(ax=axes[2], label='gen_anogen')
    plt.legend()
    plt.savefig(export_path + 'original_vs_infogan_vs_anogen.png')
    plt.close()

    # plt.figure()
    # plt.plot(original, label='original')
    # plt.plot(gen_infogan, label='gen_infogan')
    # plt.plot(gen_anogen, label='gen_anogen')
    # plt.legend(loc="upper left")
    # plt.savefig(export_path + 'original_vs_infogan_vs_anogen.png')
    # plt.close()

    # allInfoGAN = run(original, gen_infogan.iloc[:, 0])
    # allAnoGEN = run(original, gen_anogen.iloc[:, 0])
    # creating a list of dataframe columns
    resultsAnoGEN = []
    resultsInfoGAN = []
    for i in range(len(list(gen_infogan))):
        resultsInfoGAN.append(run(original, gen_infogan.iloc[:, i].tolist()))
        resultsAnoGEN.append(run(original, gen_anogen.iloc[:, i].tolist()))

    metricsAnoGEN = pd.DataFrame(resultsAnoGEN)
    metricsInfoGAN = pd.DataFrame(resultsInfoGAN)

    metrics = pd.DataFrame([metricsInfoGAN.mean(), metricsAnoGEN.mean()], index=['infogan', 'AnoGEN'])
    print(metrics)
    # normalize DTW column
    metrics["DTW"] = (metrics["DTW"] / metrics["DTW"].mean())
    metrics["MJC"] = (metrics["MJC"] / metrics["MJC"].mean())
    metrics = metrics.astype(float)

    metrics = metrics.T

    metrics.plot.bar()

    metrics.to_csv(export_path + 'metrics.csv')
    plt.savefig(export_path + 'metrics.png')
    plt.close()


def runLong(original, gen_infogan, gen_anogen, export_path=''):
    #  compares single ramdomly picked windows
    export_path = export_path + 'runLong/'
    try:
        # os.makedirs(export_path)
        os.makedirs(export_path + 'distribution/')
    except:
        pass

    plot_dist_univariate_dataset(original, export_path + 'distribution/original')
    plot_dist_univariate_dataset(gen_infogan, export_path + 'distribution/gen_infogan')
    plot_dist_univariate_dataset(gen_anogen, export_path + 'distribution/gen_anogen')

    original = original.tolist()
    try:
        original = [original[i][0] for i in range(len(original))]
    except:
        pass
    gen_infogan = gen_infogan.unstack().reset_index(drop=True).tolist()[:len(original)]
    gen_anogen = gen_anogen.unstack().reset_index(drop=True).tolist()[:len(original)]

    # print(original)
    # print(gen_infogan)
    # print(gen_anogen)
    # gen_infogan = gen_infogan.iloc[:, 0].tolist()
    # gen_anogen = gen_anogen.iloc[:, 0].tolist()[:len(gen_infogan)]
    # original = original.tolist()
    # original = original[:len(gen_infogan)]
    # original = [original[i][0] for i in range(len(original))]
    #
    plt.figure()
    plt.plot(original, label='original')
    plt.plot(gen_infogan, label='gen_infogan')
    plt.plot(gen_anogen, label='gen_anogen')
    plt.legend(loc="upper left")
    plt.savefig(export_path + 'original_vs_infogan_vs_anogen.png')
    plt.close()

    metricsInfoGAN = run(original, gen_infogan)
    metricsAnoGEN = run(original, gen_anogen)

    metrics = pd.DataFrame([metricsInfoGAN, metricsAnoGEN], index=['AnoGEN', 'infogan'])
    # normalize DTW column
    metrics["DTW"] = (metrics["DTW"] / metrics["DTW"].mean())
    metrics["MJC"] = (metrics["MJC"] / metrics["MJC"].mean())
    metrics = metrics.astype(float)

    metrics = metrics.T

    metrics.plot.bar()

    metrics.to_csv(export_path + 'metrics.csv')
    plt.savefig(export_path + 'metrics.png')
    plt.close()


def runALL(original, gen_infogan, gen_anogen, export_path=''):
    export_path = export_path + 'InfoGAN_vs_AnoGEN/'
    try:
        os.makedirs(export_path)
    except:
        pass

    options = {0: runWindow(original, gen_infogan, gen_anogen, export_path),
               1: runMultiWindows(original, gen_infogan, gen_anogen, export_path),
               2: runLong(original, gen_infogan, gen_anogen, export_path),
               }
    for i in range(3):
        print('iteration :' + str(i))
        options[i]


############################################################################

def plot_dist_univariate_dataset(df, exportFile):
    # print(df.describe())

    try:
        plt.scatter(range(df.shape[0]), np.sort(df.values))
    except:
        df = pd.DataFrame(df).iloc[:,0]
        plt.scatter(range(df.shape[0]), np.sort(df.values))

    plt.xlabel('index')
    plt.ylabel('value')
    plt.title("value distribution")
    sns.despine()
    plt.savefig(exportFile + '_dist1.png')
    plt.close()

    sns.distplot(df)
    plt.title("Distribution of value")
    sns.despine()
    plt.savefig(exportFile + '_dist2.png')
    plt.close()

    # print("Skewness: %f" % df.skew())
    # print("Kurtosis: %f" % df.kurt())


def anomaly_plot(df, anos, title = 'figure'):
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.plot(df, label='anomaly score')
    plt.fill_between([i for i in range(len(anos))], np.min(df), np.max(df),
                     where=anos == True, color='r',
                     alpha=.4, label='outlier region')
    plt.title(title)
    plt.legend()
    plt.ylabel('anomaly score')
    plt.xlabel('value')
    # plt.show()
    plt.savefig('anomaly_detection/IsolationForest/'+ title+ '.png')


def anomaly_detection(df):
    final = []
    for i in range(1):
        isolation_forest = IsolationForest(n_estimators=100)
        isolation_forest.fit(df.values.reshape(-1, 1))
        xx = np.linspace(df.min(), df.max(), len(df)).reshape(-1, 1)
        # anomaly_score = isolation_forest.decision_function(xx)
        outlier = isolation_forest.predict(xx)

        # getting anomaly score for each value
        anos = []
        for index, v in df.items():
            idx = int((v - df.min()) / ((df.max() - df.min()) / len(xx)) - 1)
            # idx = idx.fillna(0)
            # idx = idx.astype(int)
            anos.append(outlier[idx] == -1)
        anos = np.array(anos)
        final.append(len(anos[anos == True]) / len(anos))
    return anos, sum(final) / len(final)


def anomaly_score(df):
    final = []
    for i in range(1):
        isolation_forest = IsolationForest(n_estimators=100)
        isolation_forest.fit(df.values.reshape(-1, 1))
        xx = np.linspace(df.min(), df.max(), len(df)).reshape(-1, 1)
        # anomaly_score = isolation_forest.decision_function(xx)
        outlier = isolation_forest.predict(xx)

        # getting anomaly score for each value
        anos = []
        for index, v in df.items():
            idx = int((v - df.min()) / ((df.max() - df.min()) / len(xx))) - 1
            anos.append(outlier[idx] == -1)
        anos = np.array(anos)
        final.append(len(anos[anos == True]) / len(anos))
    # return len(anos[anos == True]) / len(anos)
    return sum(final) / len(final)


###############################################################################
# Tests

def test_entropy():
    # Testing against correlated Gaussian variables
    # (analytical results are known)
    # Entropy of a 3-dimensional gaussian variable
    rng = np.random.RandomState(0)
    n = 50000
    d = 3
    P = np.array([[1, 0, 0], [0, 1, .5], [0, 0, 1]])
    C = np.dot(P, P.T)
    Y = rng.randn(d, n)
    X = np.dot(P, Y)
    H_th = entropy_gaussian(C)
    H_est = entropy(X.T, k=5)
    # Our estimated entropy should always be less that the actual one
    # (entropy estimation undershoots) but not too much
    np.testing.assert_array_less(H_est, H_th)
    np.testing.assert_array_less(.9 * H_th, H_est)


def test_mutual_information():
    # Mutual information between two correlated gaussian variables
    # Entropy of a 2-dimensional gaussian variable
    n = 50000
    rng = np.random.RandomState(0)
    # P = np.random.randn(2, 2)
    P = np.array([[1, 0], [0.5, 1]])
    C = np.dot(P, P.T)
    U = rng.randn(2, n)
    Z = np.dot(P, U).T
    X = Z[:, 0]
    X = X.reshape(len(X), 1)
    Y = Z[:, 1]
    Y = Y.reshape(len(Y), 1)
    # in bits
    MI_est = mutual_information((X, Y), k=5)
    MI_th = (entropy_gaussian(C[0, 0]) +
             entropy_gaussian(C[1, 1]) -
             entropy_gaussian(C))
    # Our estimator should undershoot once again: it will undershoot more
    # for the 2D estimation that for the 1D estimation
    print(MI_est, MI_th)
    np.testing.assert_array_less(MI_est, MI_th)
    np.testing.assert_array_less(MI_th, MI_est + .3)


def test_degenerate():
    # Test that our estimators are well-behaved with regards to
    # degenerate solutions
    rng = np.random.RandomState(0)
    x = rng.randn(50000)
    X = np.c_[x, x]
    assert np.isfinite(entropy(X))
    assert np.isfinite(mutual_information((x[:, np.newaxis],
                                           x[:, np.newaxis])))
    assert 2.9 < mutual_information_2d(x, x) < 3.1


def test_mmd():
    # Test that our estimators are well-behaved with regards to
    # degenerate solutions
    rng = np.random.RandomState(0)
    x = rng.randn(50000)


test_entropy()
test_mutual_information()
test_degenerate()
test_mutual_information_2d()
test_mmd()



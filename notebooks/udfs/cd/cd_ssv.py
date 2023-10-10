import numpy as np
import time
from numpy import linalg as LA
from datetime import datetime

# Calculate maximizing sign vector z
def LSV(x, n, m):
    D = x[0, :]
    z = np.ones((n, 1))
    for i in range(1, n):
        change_plus = LA.norm(D + x[i, :]) ** 2
        change_minus = LA.norm(D - x[i, :]) ** 2
        if (change_plus < change_minus):
            z[i] = -1
        D = D + z[i] * x[i, :]
    return z


def SSV_init(x, n, m):
    pos = -1
    z = LSV(x, n, m)
    s = np.dot(x, np.dot(np.transpose(x), z))
    xxt = z * np.sum(x * x, axis=1).reshape(n, 1);
    v = (s - xxt).reshape((n, 1));
    # print v
    ssv_iter = 1
    var_bool = True
    while (var_bool or (pos != -1)):
        var_bool = False
        # Change sign
        if pos != -1:
            z[pos] = z[pos] * -1
            v = v + (2 * z[pos] * (np.dot(x, x[pos]))).reshape(n, 1)
            v[pos] = v[pos] - (2 * z[pos] * (np.dot(x[pos], x[pos])))
            # Search next element
        val = z * v
        ssv_iter = ssv_iter + 1
        if val[val < 0].size != 0:
            pos = np.argmin(val)
        else:
            pos = -1
    return z


# Calculate maximizing sign vector z
def SSV(x, n, m):
    pos = -1
    z = np.ones((n, 1))
    v = (np.dot(x, np.transpose(np.sum(x, axis=0))) - np.sum(x * x, axis=1)).reshape((n, 1))
    # print v
    ssv_iter = 1
    var_bool = True
    while (var_bool or (pos != -1)):
        var_bool = False
        # Change sign
        if pos != -1:
            z[pos] = z[pos] * -1
            v = v + (2 * z[pos] * (np.dot(x, x[pos]))).reshape(n, 1)
            v[pos] = v[pos] - (2 * z[pos] * (np.dot(x[pos], x[pos])))
            # Search next element
        val = z * v
        ssv_iter = ssv_iter + 1
        if val[val < 0].size != 0:
            pos = np.argmin(val)
        else:
            pos = -1
    return z


# Calculate centroid decomposition
def CD(x, n, m):
    L = np.zeros((n, m))
    z = np.zeros((n, m))
    R = np.zeros((m, m))
    for i in range(0, m):
        if (n < 5000):
            z[:, [i]] = SSV(x, n, m)
        else:
            z[:, [i]] = SSV_init(x, n, m)
        norm  = LA.norm(np.dot(np.transpose(x), z[:, [i]]))
        if norm <= 0.0:
            break
        R[:, [i]] = np.dot(np.transpose(x), z[:, [i]]) / norm
        L[:, i] = np.dot(x, R[:, i])
        x = x - np.dot(L[:, [i]], np.transpose(R[:, [i]]))
    return L, R, z

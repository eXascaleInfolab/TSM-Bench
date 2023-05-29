#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import numpy as np
import time
from numpy import linalg as LA

import warnings

#import xrange
#from scipy import stats

# Calculate maximizing sign vector z
def LSV(x,n,m):
    D=x[0,:]
    z = np.ones((n,1))
    for i in range(1,n):
        change_plus=LA.norm(D+x[i,:])**2
        change_minus=LA.norm(D-x[i,:])**2
        if(change_plus<change_minus):
            z[i]=-1
        D=D+z[i]*x[i,:]
    return z

def SSV_init(x,n,m):
  pos = -1
  z=LSV(x,n,m)
  s=np.dot(x,np.dot(np.transpose(x),z))
  xxt =z* np.sum(x * x, axis=1).reshape(n,1);
  v = (s - xxt).reshape((n, 1));
  #print v
  ssv_iter=1
  var_bool=True
  while (var_bool or (pos!=-1)):
    var_bool=False
    #Change sign
    if pos!=-1:
      z[pos] = z[pos]*-1
      v=v+(2*z[pos]*(np.dot(x,x[pos]))).reshape(n,1)
      v[pos]=v[pos]-(2*z[pos]*(np.dot(x[pos],x[pos])))
    #Search next element
    val=z*v
    ssv_iter=ssv_iter+1
    if val[val<0].size!=0:
      pos=np.argmin(val)
    else:
      pos=-1
  return z

#Calculate maximizing sign vector z
def SSV(x,n,m):
  pos = -1
  z = np.ones((n,1))
  v = (np.dot(x,np.transpose(np.sum(x, axis=0)))- np.sum(x*x,axis=1)).reshape((n,1))
  #print v
  ssv_iter=1
  var_bool=True
  while (var_bool or (pos!=-1)):
    var_bool=False
    #Change sign
    if pos!=-1:
      z[pos] = z[pos]*-1
      v=v+(2*z[pos]*(np.dot(x,x[pos]))).reshape(n,1)
      v[pos]=v[pos]-(2*z[pos]*(np.dot(x[pos],x[pos])))
    #Search next element
    val=z*v
    ssv_iter=ssv_iter+1
    if val[val<0].size!=0:
      pos=np.argmin(val)
    else:
      pos=-1
  return z

#Calculate centroid decomposition
def CD(x,k,n,m):
  L =np.zeros((n,m))
  z=np.zeros((n,m))
  R =np.zeros((m,m))
  for i in range (0,k):
    if (n<5000):
        z[:,[i]] = SSV(x,n,m)
    else:
        z[:,[i]] = SSV_init(x,n,m)
    R[:,[i]]  = np.dot(np.transpose(x),z[:,[i]])/LA.norm(np.dot(np.transpose(x),z[:,[i]]))
    L[:,i] = np.dot(x,R[:,i])
    x = x - np.dot(L[:,[i]],np.transpose(R[:,[i]]))
  return L,R,z

#cd with z as input
def ZCD(x,z,k,n,m):
  L =np.zeros((n,m))
  R =np.zeros((m,m))
  for i in range (0,k):
    R[:,[i]]  = np.dot(np.transpose(x),z[:,[i]])/LA.norm(np.dot(np.transpose(x),z[:,[i]]))
    L[:,i] = np.dot(x,R[:,i])
    x = x - np.dot(L[:,[i]],np.transpose(R[:,[i]]))
  return L,R


def zcd_recovery(X_tilde,n,m,trunc_col,epsilon,missing_rows,missing_cols,z):
    iteration=1
    X_init = np.zeros([n, m])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        while (((LA.norm(X_init[missing_rows,missing_cols]-X_tilde[missing_rows,missing_cols]))/len(missing_rows))>epsilon) and (iteration<200):
            iteration+=1
            X_init=X_tilde.copy()
            L,R = ZCD(X_tilde,z,(X_tilde.shape[1]-trunc_col),n,m)
            X_new=np.dot(L,np.transpose(R))
            X_tilde[missing_rows,missing_cols]=X_new[missing_rows,missing_cols]
    return X_tilde,iteration

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0],lambda z1: z1.nonzero()[1]

def linear_interpolated_base_series_values(matrix, base_series_index, rows):
    mb_start = -1;
    prev_value = np.nan;
    step = 0;#init

    for i in range(0, rows):
        if (np.isnan(matrix[i][base_series_index])):
            # current value is missing - we either start a new block, or we are in the middle of one

            if (mb_start == -1): # new missing block
                mb_start = i;
                mb_end = mb_start + 1;

                #lookahead to find the end
                # INDEX IS NEXT NON-np.nan ELEMENT, NOT THE LAST np.nan
                # INCLUDING OUT OF BOUNDS IF THE BLOCK ENDS AT THE END OF TS
                while ((mb_end < rows) and np.isnan(matrix[mb_end][base_series_index])): mb_end += 1;

                next_value = np.nan if mb_end == rows else matrix[mb_end][base_series_index];

                # special case #1: block starts with array
                if (mb_start == 0): prev_value = next_value;

                # special case #2: block ends with array
                if (mb_end == rows): next_value = prev_value;

                step = (next_value - prev_value) / (mb_end - mb_start + 1);
            #end if
            matrix[i][base_series_index] = prev_value + step * (i - mb_start + 1);
        else:
            # missing block either ended just new or we're traversing normal data
            prev_value = matrix[i][base_series_index];
            mb_start = -1;
        #end if
    #end for
    return matrix;

def recovery(input_matrix,n,m,trunc_col,perc,col_drop):
   #input_matrix=stats.zscore(input_matrix)
   X_tilde=input_matrix.copy()
   for perc_col in range(0,col_drop):
       X_tilde[int((perc_col*perc*n)-(perc_col*0.05*n)+500):int(((perc_col+1)*perc*n)-(perc_col*0.05*n)+500),perc_col]=np.NaN
       #print int((perc_col*perc*n)-(perc_col*0.02*n)+500),int(((perc_col+1)*perc*n)-(perc_col*0.02*n)+500)
   nans, index0,index1= nan_helper(X_tilde)
   missing_rows=index0(nans)
   missing_cols=index1(nans)
   for i in range(0, m):
       X_tilde = linear_interpolated_base_series_values(X_tilde, i, n);

   #recovery of missing values
   epsilon=1
   ts1 = time.time()
   L,R,z = CD(X_tilde,(X_tilde.shape[1]-trunc_col),n,m)
   X_rec,iteration= zcd_recovery(X_tilde,n,m,trunc_col,epsilon,missing_rows,missing_cols,z)
   ts2 = time.time()
   return (ts2 - ts1),iteration,rmse((X_rec/1e5), (input_matrix/1e5)),X_rec

def rmse(predictions, targets):
    return np.sqrt(np.sum((predictions - targets) ** 2)/predictions.shape[0])

def MAD(predictions, targets):
    return abs(np.sum((predictions - targets)))/predictions.shape[0]

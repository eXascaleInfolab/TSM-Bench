from datetime import datetime
from tqdm import tqdm
import argparse
import os
import time
import statistics as stats
import numpy as np
import random


def str_time_prop(start, end, time_format, prop):
	"""Get a time at a proportion of a range of two formatted times.
	start and end should be strings specifying times formatted in the
	given format (strftime-style), giving an interval [start, end].
	prop specifies how a proportion of the interval to be taken after
	start.  The returned time will be in the specified format.
	"""

	stime = time.mktime(time.strptime(start, time_format))
	etime = time.mktime(time.strptime(end, time_format))

	ptime = stime + prop * (etime - stime)

	return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop, dform = '%Y-%m-%dT%H:%M:%S'):
	return str_time_prop(start, end, dform, prop)
	
def get_list(elm, n_elm, max_r = 10, prefix = '', suffix = '', apostrophe = True):
	res = ''
	elms = random.sample(range(max_r), n_elm)
	for i in range(n_elm): 
		item = prefix + elm + str(elms[i]) +  suffix 
		if apostrophe: 
			item = "'" + item + "'"
		res += item 
		if i < n_elm - 1: 
			res += ", "
	return 
	
def to_pm(v):
		return str(int(v[0][0])) + "$" + '\\' + "pm$" + str(int(v[1][0]))


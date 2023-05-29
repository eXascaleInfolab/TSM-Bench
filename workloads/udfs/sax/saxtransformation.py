from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize

def saxrepresentation(matrix):
	result = []
	index_ts = 0
	for ts in matrix.T:
		sax_representation = znorm(ts)
		dat_paa_3 = paa(sax_representation, 3)
		a = ts_to_string(dat_paa_3, cuts_for_asize(3))
		result.append(a)

	return result

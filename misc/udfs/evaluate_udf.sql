-- MonetDB --------------------------------------------------------------------
CREATE OR REPLACE FUNCTION test_matrix() RETURNS TABLE(runtime DOUBLE PRECISION)
LANGUAGE PYTHON
{
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/mnt/hdd/ABench-IoT/Algorithms/centroid_decomposition")
    import cd_ssv
    start = timeit.default_timer()
    matrix= numpy.random.rand(700, 700)
    m = matrix.shape[0]
    n = matrix.shape[1]
    matrix_l, matrix_r, z = cd_ssv.CD(matrix, m, n)
    return timeit.default_timer() - start
};
SELECT * FROM test_matrix();
-------------------------------------------------------------------------------

-- TimescaleDB ----------------------------------------------------------------
CREATE TYPE result_type_matrix AS ( d DOUBLE PRECISION ARRAY );
CREATE OR REPLACE FUNCTION test_matrix() RETURNS DOUBLE PRECISION AS $$
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/localdata/ABench-IoT/Algorithms/centroid_decomposition")
    import cd_ssv
    start = timeit.default_timer()
    matrix= numpy.random.rand(700, 700)
    m = matrix.shape[0]
    n = matrix.shape[1]
    matrix_l, matrix_r, z = cd_ssv.CD(matrix, m, n)
    return timeit.default_timer() - start
$$ LANGUAGE plpython3u;
SELECT * FROM test_matrix();
-------------------------------------------------------------------------------

-- eXtremeDB ------------------------------------------------------------------
drop function test_matrix;
create function test_matrix() RETURNS DOUBLE in 'python' as '
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/localdata/ABench-IoT/Algorithms/centroid_decomposition")
    import cd_ssv
    start = timeit.default_timer()
    matrix= numpy.random.rand(700, 700)
    m = matrix.shape[0]
    n = matrix.shape[1]
    matrix_l, matrix_r, z = cd_ssv.CD(matrix, m, n)
    return timeit.default_timer() - start
';
select test_matrix();
-------------------------------------------------------------------------------


























-- MonetDB --------------------------------------------------------------------
CREATE OR REPLACE FUNCTION test_matrix() RETURNS TABLE(runtime DOUBLE PRECISION)
LANGUAGE PYTHON
{
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/mnt/hdd/ABench-IoT/Algorithms/hot_sax")
    import hotsax
    start = timeit.default_timer()
    matrix= numpy.random.rand(200, 200)
    m = matrix.shape[0]
    n = matrix.shape[1]
    discord = hotsax.hotsax(matrix)
    return timeit.default_timer() - start
};
SELECT * FROM test_matrix();
-------------------------------------------------------------------------------

-- TimescaleDB ----------------------------------------------------------------
CREATE TYPE result_type_matrix AS ( d DOUBLE PRECISION ARRAY );
CREATE OR REPLACE FUNCTION test_matrix() RETURNS DOUBLE PRECISION AS $$
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/localdata/ABench-IoT/Algorithms/hot_sax")
    import hotsax
    start = timeit.default_timer()
    matrix= numpy.random.rand(200, 200)
    m = matrix.shape[0]
    n = matrix.shape[1]
    discord = hotsax.hotsax(matrix)
    return timeit.default_timer() - start
$$ LANGUAGE plpython3u;
SELECT * FROM test_matrix();
-------------------------------------------------------------------------------

-- eXtremeDB ------------------------------------------------------------------
drop function test_matrix;
create function test_matrix() RETURNS DOUBLE in 'python' as '
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/localdata/ABench-IoT/Algorithms/hot_sax")
    import hotsax
    start = timeit.default_timer()
    matrix= numpy.random.rand(200, 200)
    m = matrix.shape[0]
    n = matrix.shape[1]
    discord = hotsax.hotsax(matrix)
    return timeit.default_timer() - start
';
select test_matrix();
-------------------------------------------------------------------------------


























-- MonetDB --------------------------------------------------------------------
CREATE OR REPLACE FUNCTION test_matrix() RETURNS TABLE(runtime DOUBLE PRECISION)
LANGUAGE PYTHON
{
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/mnt/hdd/ABench-IoT/Algorithms/kmeans")
    import kmeans
    start = timeit.default_timer()
    matrix= numpy.random.rand(5000, 5000)
    m = matrix.shape[0]
    n = matrix.shape[1]
    clusters = kmeans.kmeans(matrix, 10, 20).T
    return timeit.default_timer() - start
};
SELECT * FROM test_matrix();
-------------------------------------------------------------------------------

-- TimescaleDB ----------------------------------------------------------------
CREATE TYPE result_type_matrix AS ( d DOUBLE PRECISION ARRAY );
CREATE OR REPLACE FUNCTION test_matrix() RETURNS DOUBLE PRECISION AS $$
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/localdata/ABench-IoT/Algorithms/kmeans")
    import kmeans
    start = timeit.default_timer()
    matrix= numpy.random.rand(5000, 5000)
    m = matrix.shape[0]
    n = matrix.shape[1]
    clusters = kmeans.kmeans(matrix, 10, 20).T
    return timeit.default_timer() - start
$$ LANGUAGE plpython3u;
SELECT * FROM test_matrix();
-------------------------------------------------------------------------------

-- eXtremeDB ------------------------------------------------------------------
drop function test_matrix;
create function test_matrix() RETURNS DOUBLE in 'python' as '
    import numpy
    import timeit
    from datetime import datetime
    import sys
    sys.path.append("/localdata/ABench-IoT/Algorithms/kmeans")
    import kmeans
    start = timeit.default_timer()
    matrix= numpy.random.rand(5000, 5000)
    m = matrix.shape[0]
    n = matrix.shape[1]
    clusters = kmeans.kmeans(matrix, 10, 20).T
    return timeit.default_timer() - start
';
select test_matrix();
-------------------------------------------------------------------------------




import numpy
import timeit
from datetime import datetime
import sys
sys.path.append("/localdata/ABench-IoT/Algorithms/kmeans")
import kmeans
start = timeit.default_timer()
matrix= numpy.random.rand(5000, 5000)
m = matrix.shape[0]
n = matrix.shape[1]
clusters = kmeans.kmeans(matrix, 10, 20).T
print(timeit.default_timer() - start)








------ ALL Queries MonetDB 

CREATE FUNCTION pysqrt ( i INTEGER ) RETURNS REAL
LANGUAGE PYTHON 
{
	return numpy.sqrt (i)
};
SELECT pysqrt (id_station * 2) FROM datapoints ;


DROP FUNCTION query1;
CREATE FUNCTION query1 ( x1 DOUBLE, x2 DOUBLE, x3 DOUBLE ) RETURNS REAL
LANGUAGE PYTHON 
{
	return numpy.sqrt (x1 + x2 * x3)
};
SELECT query1 (temperature, pH, oxygen) FROM datapoints where id_station = 0;

DROP FUNCTION query2;
CREATE FUNCTION query2 ( id_station INTEGER, x DOUBLE ) RETURNS REAL
LANGUAGE PYTHON 
{
	return numpy.dot (id_station, x)
};
SELECT query2 (id_station, pH) FROM datapoints where id_station = 1;

DROP FUNCTION query3;
CREATE FUNCTION query3 ( x1 DOUBLE, x2 DOUBLE, x3 DOUBLE, x4 DOUBLE ) RETURNS TABLE (d1 REAL, d2 REAL)
LANGUAGE PYTHON 
{
	return numpy.dot(numpy.array([x1, x2]), numpy.array([x3, x4]).T)
};
SELECT * from query3 ((select temperature, pH, oxygen, oxygen_saturation FROM datapoints where id_station = 1));






------ ALL Queries EXtremeDB







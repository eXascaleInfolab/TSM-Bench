
----- extremedb ----------------------------------------------------------------
drop function current_time;
drop table metrics_udf;
CREATE TABLE metrics_udf (current_time DOUBLE);
create function current_time() returns double in 'python' as '
        from datetime import datetime
        return(datetime.now() - datetime(1970, 1, 1)).total_seconds()
';
CREATE TABLE matrixr (t TIMESTAMP, d ARRAY(DOUBLE));
drop function udf_cd;
create function udf_cd() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        sys.path.append("cd")
        import cd_ssv
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        cur.execute("select seq_search(t,1559390400 - 20 * 60 * 60,1559390400) as tt, id_station, water_temperature@tt from datapoints_v where id_station < 50")
        print(cur)
        water_temperature = []
        stations = []
        dictio = {}
        for row in cur:
                times = [p for p in row[0] ]
                dictio[row[1]] = [w for w in row[2]]
        matrix = np.vstack(list(dictio.values())).T
        m = matrix.shape[0]
        n = matrix.shape[1]
        print(matrix)
        start = timeit.default_timer()
        matrix_l, matrix_r, z = cd_ssv.CD(matrix, m, n)
        for i in range(len(matrix_r)):
                cur.execute("INSERT INTO matrixr(t, d) VALUES (?, ?)", (times[i], tuple(matrix_r[i])))
        stop = timeit.default_timer()
        #print(matrix_r)
        #print(matrix_l)
        print("Runtime: ", stop - start)
        return "success"
';
INSERT INTO metrics_udf VALUES(current_time());
SELECT udf_cd();
INSERT INTO metrics_udf VALUES(current_time());
SELECT MAX(current_time) - MIN(current_time) AS cd_time FROM metrics_udf;







drop function current_time;
drop table metrics_udf;
CREATE TABLE metrics_udf (current_time DOUBLE);
create function current_time() returns double in 'python' as '
        from datetime import datetime
        return(datetime.now() - datetime(1970, 1, 1)).total_seconds()
';
CREATE TABLE matrixr (t TIMESTAMP, d ARRAY(DOUBLE));
drop function udf_cd;
create function udf_cd() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        sys.path.append("cd")
        import cd_ssv
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        cur.execute("select seq_search(t,1559390400 - 20 * 60 * 60,1559390400) as tt, id_station, water_temperature@tt from datapoints_v where id_station < 50")
        print(cur)
        water_temperature = []
        stations = []
        dictio = {}
        for row in cur:
                times = [p for p in row[0] ]
                dictio[row[1]] = [w for w in row[2]]
        matrix = np.vstack(list(dictio.values())).T
        m = matrix.shape[0]
        n = matrix.shape[1]
        print(matrix)
        start = timeit.default_timer()
        matrix_l, matrix_r, z = cd_ssv.CD(matrix, m, n)
        stop = timeit.default_timer()
        for i in range(len(matrix_r)):
                cur.execute("INSERT INTO matrixr(t, d) VALUES (?, ?)", (times[i], tuple(matrix_r[i])))
        #print(matrix_r)
        #print(matrix_l)
        print("Runtime: ", stop - start)
        return "success"
';
INSERT INTO metrics_udf VALUES(current_time());
SELECT udf_cd();
INSERT INTO metrics_udf VALUES(current_time());
SELECT MAX(current_time) - MIN(current_time) AS cd_time FROM metrics_udf;





drop function udf_hotsax;
drop table metrics_udf;
CREATE TABLE metrics_udf (current_time DOUBLE);
CREATE TABLE result_anomalies(t TIMESTAMP, index_timeseries INTEGER, d DOUBLE);
create function udf_hotsax() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        sys.path.append("hot_sax")
        import hotsax
        import timeit
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        cur.execute("select seq_search(t,1559390400 - 60 * 60,1559390400) as tt, id_station, water_temperature@tt from datapoints_v where id_station < 50")
        print(cur)
        water_temperature = []
        stations = []
        dictio = {}
        for row in cur:
                times = [p for p in row[0] ]
                dictio[row[1]] = [w for w in row[2]]
        matrix = np.vstack(list(dictio.values())).T
        m = matrix.shape[0]
        n = matrix.shape[1]
        print(matrix)
        
        start = timeit.default_timer()
        discord = hotsax.hotsax(matrix)
        stop = timeit.default_timer()
        for i in range(len(discord)):
                cur.execute("INSERT INTO result_anomalies VALUES (?,?,?)", (times[i], discord[i][0], discord[i][2]))
        print("Runtime: ", stop - start)
        return "success"
';
INSERT INTO metrics_udf VALUES(current_time());
SELECT udf_hotsax();
INSERT INTO metrics_udf VALUES(current_time());
SELECT MAX(current_time) - MIN(current_time) AS cd_time FROM metrics_udf;







drop function udf_screen;
drop table metrics_udf;
CREATE TABLE metrics_udf (current_time DOUBLE);
DROP TABLE screen;
CREATE TABLE screen (t TIMESTAMP, d ARRAY(DOUBLE));
DROP function udf_screen;
create function udf_screen() RETURNS string in 'python' as '
        import sys
        import numpy as np
        from datetime import datetime
        sys.path.append("/home/abdel/ABench-IoT/Algorithms/screen_python/")
        import screen
        from datetime import datetime
        import timeit
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        cur.execute("select seq_search(t,1559390400 - 10 * 60 * 60,1559390400) as tt, id_station, water_temperature@tt from datapoints_v where id_station < 50")
        print(cur)
        water_temperature = []
        stations = []
        dictio = {}
        for row in cur:
                times = [p for p in row[0] ]
                dictio[row[1]] = [w for w in row[2]]
        matrix = np.vstack(list(dictio.values())).T
        m = matrix.shape[0]
        n = matrix.shape[1]
        
        start = timeit.default_timer()
        s = screen.screen(matrix, times, 0.1, -0.1, 300)
        stop = timeit.default_timer()
        for i in range(len(s)):
                cur.execute("INSERT INTO screen(t, d) VALUES (?, ?)", (times[i], tuple(s[i])))
        print("Runtime: ", stop - start)
        return "success"
';
INSERT INTO metrics_udf VALUES(current_time());
SELECT udf_screen();
INSERT INTO metrics_udf VALUES(current_time());
SELECT MAX(current_time) - MIN(current_time) AS cd_time FROM metrics_udf;

--------------------------------------------------------------------------------




----- monetdb ------------------------------------------------------------------

DROP FUNCTION cd_alg;
CREATE OR REPLACE FUNCTION cd_alg(time TIMESTAMP, id_station INTEGER, temperature DOUBLE PRECISION) RETURNS TABLE(runtime DOUBLE PRECISION)
LANGUAGE PYTHON
{
    import sys
    import numpy as np
    sys.path.append('/home/abdel/ABench-IoT/Algorithms/cd/')
    import cd_ssv
    import timeit
    
    def create_dict(a, b):
        id_stations = list(dict.fromkeys(a))
        dictio = {i: [] for i in id_stations}
        for i in range(len(b)):
            dictio[a[i]].append(b[i])
        return dictio
    
    #a = [1, 1, 2, 2, 3, 3, 4, 1, 5, 6]
    #b = random.sample(range(10, 30), len(a))
    dictio = create_dict(id_station,temperature)
    print(dictio)
    matrix = np.vstack(list(dictio.values())).T
    print(matrix)
    n = matrix.shape[0]
    m = matrix.shape[1]
    
    start = timeit.default_timer()
    matrix_l, matrix_r, z = cd_ssv.CD(matrix, n, m)
    stop = timeit.default_timer()
    
    print('Time: ', stop - start)
    
    return stop - start
};

SET initial_time_cd = get_time();
SELECT * FROM cd_alg( (SELECT time, id_station, temperature FROM datapoints where id_station < 50 and time < str_to_timestamp('2019-05-26 12:00:00', '%Y-%m-%d %H:%M:%S') and time> str_to_timestamp('2019-05-26 12:00:00', '%Y-%m-%d %H:%M:%S') - (interval '20' hour )) ) ;     
SET final_time_cd = get_time();

SELECT final_time_cd - initial_time_cd as Time_seconds;










DROP FUNCTION sax_alg;
CREATE OR REPLACE FUNCTION sax_alg(time TIMESTAMP, id_station INTEGER, temperature DOUBLE PRECISION) RETURNS TABLE(runtime DOUBLE PRECISION)
LANGUAGE PYTHON
{
    import sys
    import numpy as np
    sys.path.append('/home/abdel/ABench-IoT/Algorithms/hot_sax/')
    import hotsax
    import timeit

    def create_dict(a, b):
        id_stations = list(dict.fromkeys(a))
        dictio = {i: [] for i in id_stations}
        for i in range(len(b)):
            dictio[a[i]].append(b[i])
        return dictio
    dictio = create_dict(id_station,temperature)
    matrix = np.vstack(list(dictio.values())).T
    
    start = timeit.default_timer()
    discord = hotsax.hotsax( matrix )

    r_time = []
    r_index = []
    r_value = []
    for i in range(len(discord)):
        r_time.append( time[ discord[i][1] ] )
        r_index.append( discord[i][0] )
        r_value.append( discord[i][2] )
    stop = timeit.default_timer()
    return stop - start
};
SELECT * FROM sax_alg( (SELECT time, id_station, temperature FROM datapoints where id_station < 50 and time < str_to_timestamp('2019-05-26 12:00:00', '%Y-%m-%d %H:%M:%S') and time> str_to_timestamp('2019-05-26 12:00:00', '%Y-%m-%d %H:%M:%S') - (interval '1' HOUR )) ) ;     



DROP FUNCTION screen_alg;
CREATE OR REPLACE FUNCTION screen_alg(time TIMESTAMP, id_station INTEGER, temperature DOUBLE PRECISION) RETURNS TABLE(runtime DOUBLE PRECISION)
LANGUAGE PYTHON
{
    import sys
    import numpy as np
    sys.path.append('/home/abdel/ABench-IoT/Algorithms/screen_python/')
    import screen
    import datetime
    import timeit

    def create_dict(a, b):
        id_stations = list(dict.fromkeys(a))
        dictio = {i: [] for i in id_stations}
        for i in range(len(b)):
            dictio[a[i]].append(b[i])
        return dictio
    dictio = create_dict(id_station,temperature)
    matrix = np.vstack(list(dictio.values())).T

    time = [( datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime(1970, 1, 1)).total_seconds() for x in time]
    time = [int(x) for x in time]
    
    start = timeit.default_timer()
    results = screen.screen(matrix, time, 0.1, -0.1, 300).T
    stop = timeit.default_timer()

    sys.path = sys.path[:-1]
    return stop - start
};
SELECT * FROM screen_alg( (SELECT time, id_station, temperature FROM datapoints where id_station < 50 and time < str_to_timestamp('2019-05-26 12:00:00', '%Y-%m-%d %H:%M:%S') and time> str_to_timestamp('2019-05-26 12:00:00', '%Y-%m-%d %H:%M:%S') - (interval '10' HOUR )) ) ;     




















--------------------------------------------------------------------------------






----- timescaledb --------------------------------------------------------------
DROP TYPE IF EXISTS result_type CASCADE;
CREATE TYPE result_type AS ( d DOUBLE PRECISION ARRAY );
CREATE TABLE matrix_r OF result_type;
DROP FUNCTION cd();
DROP TABLE IF EXISTS matrix_r;
CREATE TABLE matrix_r OF result_type;
CREATE OR REPLACE FUNCTION cd() RETURNS DOUBLE PRECISION AS $$
    import sys
    import numpy as np
    sys.path.append('/mnt/hdd/ABench-IoT_timescaledb/ABench-IoT/Algorithms/cd/')
    import cd_ssv
    import timeit
    
    nb_minutes = 100
    rows = 6 * nb_minutes
    a = plpy.execute("SELECT time, id_station, temperature FROM datapoints where id_station < 50 and time > TIMESTAMP '2019-06-01 00:00:00' - INTERVAL '" + str(20) + "' HOUR and time < TIMESTAMP '2019-06-01 00:00:00';")
    water_temperature = []
    dictio = {}
    for i in range(len(a)):
        dictio[int(a[i]['id_station'])] = []
    
    matrix = []
    for i in range(len(a)):
        dictio[int(a[i]['id_station'])].append(float(a[i]['temperature']))
    matrix = np.vstack(list(dictio.values())).T
    m = matrix.shape[0]
    n = matrix.shape[1]
    
    start = timeit.default_timer()
    matrix_l, matrix_r, z = cd_ssv.CD(matrix, m, n)
    stop = timeit.default_timer()  
    print("Runtime: ", stop - start)
    result = []
    for i in range(n):
        result.append( [matrix_r[i].tolist()] )
    return stop - start
$$ LANGUAGE plpython3u;

DO $cd$
DECLARE
    start_time TIMESTAMP WITH TIME ZONE;
    end_time TIMESTAMP WITH TIME ZONE;
    delta DOUBLE PRECISION;
BEGIN
    start_time := clock_timestamp();
    SELECT * FROM cd();
    end_time := clock_timestamp();
    delta = extract(epoch from end_time) - extract(epoch from start_time);

    RAISE NOTICE 'CentroidDecomposition time seconds = %', delta;
END;
$cd$;


DROP TABLE IF EXISTS discords;
DROP TYPE IF EXISTS result_type CASCADE;
CREATE TYPE result_type AS ( time TIMESTAMP WITHOUT TIME ZONE, index_timeseries INTEGER, value DOUBLE PRECISION );
CREATE TABLE discords OF result_type;
CREATE OR REPLACE FUNCTION hotsax() RETURNS DOUBLE PRECISION AS $$
    import sys
    import numpy as np
    sys.path.append('hot_sax')
    import hotsax
    import timeit
    nb_minutes = 20
    rows = 6 * nb_minutes
    a = plpy.execute("SELECT time, id_station, temperature FROM datapoints where id_station < 50 and time > TIMESTAMP '2019-06-01 00:00:00' - INTERVAL '" + str(1) + "' HOUR and time < TIMESTAMP '2019-06-01 00:00:00';")
    water_temperature = []
    dictio = {}
    for i in range(len(a)):
        dictio[int(a[i]['id_station'])] = []
    
    matrix = []
    for i in range(len(a)):
        dictio[int(a[i]['id_station'])].append(float(a[i]['temperature']))
    matrix = np.vstack(list(dictio.values())).T
    m = matrix.shape[0]
    n = matrix.shape[1]
    start = timeit.default_timer()  
    discord = hotsax.hotsax(matrix)
    stop = timeit.default_timer()  
    result = []
    for i in range(len(discord)):
        result.append( [ a[ discord[i][1] ]['time'], discord[i][0], discord[i][2] ] )
    return stop - start
$$ LANGUAGE plpython3u;

DO $hotsax$
DECLARE
    start_time TIMESTAMP WITH TIME ZONE;
    end_time TIMESTAMP WITH TIME ZONE;
    delta DOUBLE PRECISION;
BEGIN
    start_time := clock_timestamp();
    INSERT INTO discords SELECT * FROM hotsax();
    end_time := clock_timestamp();
    delta = extract(epoch from end_time) - extract(epoch from start_time);
    RAISE NOTICE 'HOT-SAX time seconds = %', delta;
END;
$hotsax$;



DROP FUNCTION IF EXISTS screen;
DROP TYPE IF EXISTS result_type CASCADE;
CREATE TYPE result_type AS ( d DOUBLE PRECISION ARRAY );
CREATE TABLE screen OF result_type;
CREATE OR REPLACE FUNCTION screen() RETURNS SETOF result_type AS $$
    import sys
    import numpy as np
    sys.path.append('<implementation_path>/')
    import screen
    from datetime import datetime

    a = plpy.execute("SELECT * FROM datapoints ORDER BY time ASC;")

    rows = <rows>
    columns = <columns>
    matrix = []
    timestamps = []
    for i in range(rows):
        matrix.append( a[i]['d'] )
        timestamps.append( a[i]['time'] )
    timestamps = [ int( (datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - datetime(1970, 1, 1)).total_seconds() ) for x in timestamps]
    matrix = np.array( matrix )

    result = screen.screen(matrix, timestamps, 0.1, -0.1, 300)

    return [ [x] for x in result ]
$$ LANGUAGE plpython3u;
--------------------------------------------------------------------------------










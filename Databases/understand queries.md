# I- druid


## 1 - range 
```sql
-- SELECT count(*) from (select * FROM datapoints where id_station in (32, 54, 98, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-26 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-26 00:00:00') as res;
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '1' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' 
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' 
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' 
```


## 2 - filter 

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and pH < 8.04
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and ph BETWEEN 7.90 and 10.04
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and pH = 8.04 
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and pH = 8.04 and temperature > 407.282
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.04 and temperature = 407.282
```

## 3 - queries  
### select
```sql

```
### source 
```sql
select id_station, __time  FROM bafu_comma where __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.6
```

### agg 

```sql
select AVG(pH),AVG(pH)  FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00'
```

### count 
```sql
SELECT id_station, count(*) FROM bafu_comma where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) group by id_station
```

### full scan
```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
```
### group by 
```sql
select id_station, avg(pH) FROM bafu_comma 
where __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00'
group by id_station
```
### down 
```sql
SELECT id_station, TIME_EXTRACT(__time, 'YEAR')  AS "yearP",
TIME_EXTRACT(__time, 'MONTH') AS "month", 
TIME_EXTRACT(__time, 'DAY') AS "day", 
TIME_EXTRACT(__time, 'HOUR') AS "hour", 
AVG(pH) AS avg_ph 
FROM bafu_comma where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND __time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY 1,2,3,4,5
```
### up 
```json
{
  "queryType": "timeseries",
  "dataSource": "bafu_comma",
  "intervals": [
    "2019-03-01T00:00:00.000/2019-06-21T00:00:00.000"
  ],
  "granularity": {"type": "duration", "duration": "5000"},
  "aggregations": [
    {
      "type": "doubleMean",
      "name": "pH",
      "fieldName": "pH"
    }
  ],
  "filter": {
        "type": "in",
        "dimension": "id_station",
        "values": ["32", "54", "8", "25", "95", "13", "80", "16", "83", "27"]
  },
  "context": {
    "grandTotal": false
  }
}
```

### loop 
```sql

```



## 4 - stations 

```sql
select * FROM bafu_comma where id_station in (32)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00'
```

```sql
select * FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00'
```

```sql
select * FROM bafu_comma where id_station in 
(45,60,56,40,21,91,52,2,87,83,9,61,31,23,75,19,26,47,17,16,39,58,66,85,65,53,80,29,68,93,10,12,15,84,14,81,3,59,28,7,54,94,0,34,89,71,99,50,67,18,69,30,48,46,95,8,43,74,24,35,79,62,76,37,82,88,5,63,77,1,92,6,41,51,42,44,33,20,4,73,98,57,38,70,27,97,64,36,78,11,72,0,86,90,22,13,32,49,96,25)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00'
```










# II- extreme


## 1 - range 

### 1 day
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 1 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';

select udf_query_with();
```

### 10 days
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```
### 100 days
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 90 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```


## 2 - filter 
### >
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, !seq_filter_search(pH@tt > 8.04, tt) as fe, water_temperature@fe, Discharge@fe, pH@fe, oxygen@fe, oxygen_saturation@fe FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```

### BETWEEN

```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, !seq_filter_search(pH@tt > 7.90 and pH@tt < 10.04, tt) as fe, water_temperature@fe, Discharge@fe, pH@fe, oxygen@fe, oxygen_saturation@fe FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```
### =

```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, id_station, !seq_filter_search(pH@tt = 8.04, tt) as fe, water_temperature@fe, Discharge@fe, pH@fe, oxygen@fe, oxygen_saturation@fe FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```

### = and > on another
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, !seq_filter_search(pH@tt = 8.04 and water_temperature@tt > 407.282, tt) as fe, water_temperature@fe, Discharge@fe, pH@fe, oxygen@fe, oxygen_saturation@fe FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();

```


### select
```sql

```
### source 
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select id_station, seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, !seq_filter_search(pH@tt > 8.6, tt) as fe FROM datapoints_v")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[0]] = [w for w in row[1]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();

# select id_station, time FROM datapoints where time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.6;

```

### agg 

```sql

drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("SELECT ! seq_search(t,1560988800 - 90 * 24 * 60 * 60,1560988800) as tt, seq_dev(pH@tt), seq_avg(pH@tt) 
FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[0]] = [w for w in row[1]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();


SELECT AVG(pH),stddev_pop(pH) 
FROM datapoints 
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' ;
```

### count 
```sql
select id_station, sum(seq_count(t)) from datapoints_v where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) group by id_station; 
```

### full scan
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select  id_station,  seq_search(t,1560988800 - 90 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```

### group by 

```sql

drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("SELECT  id_station, avg(pH) FROM datapoints_v group by id_station")
        stations = []
        dictio = {}
        for row in cur:
                try: 
                  dictio[row[0]] = [w for w in row[1]]
                except: 
                  dictio[row[0]] = row[1]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
SELECT  id_station, avg(pH) FROM datapoints_v group by id_station;
```

### down 
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select id_station, seq_search(t,1559390400 - 90 * 24 * 60 * 60,1559390400) as tt, t@tt/3600 as hour, seq_group_agg_dev(pH@tt, t@tt/3600) FROM datapoints_v WHERE id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                try: 
                  dictio[row[0]] = [w for w in row[1]]
                except: 
                  dictio[row[0]] = row[1]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```
### up 
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_aprogres_datetime(1551398400, 5, 90 * 24 * 60 * 60) as ts5,seq_stretch(ts5,t,pH) from datapoints_v where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                stations = [w for w in row[0]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();

;

```

### loop 
```sql

```


## 4 - stations 

### 1 station
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 1 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```

### 10 station
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 10 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```

### 100 station
```sql
drop function udf_query_with;
create function udf_query_with() RETURNS string in 'python' as '
        import sys
        import numpy as np
        import timeit
        from datetime import datetime
        exdb.init_runtime(skip_load=True)
        cur = current_session.cursor()
        start = timeit.default_timer()
        cur.execute("select seq_search(t,1560988800 - 100 * 24 * 60 * 60,1560988800) as tt, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)")
        stations = []
        dictio = {}
        for row in cur:
                dictio[row[1]] = [w for w in row[2]]
        stop = timeit.default_timer()
        print("Runtime: ", stop - start)
        return "success"
';
select udf_query_with();
```




# III- influx 1.7



## 1 - range 
```sql
-- SELECT count(*) from (select * FROM datapoints where id_station in (32, 54, 98, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00') as res;
```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 1d AND  time < '2019-06-01T00:00:00Z'
```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 10d AND  time < '2019-06-01T00:00:00Z'
```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 90d AND  time < '2019-06-01T00:00:00Z'
```


## 2 - filter 

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and pH > 8.04
```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and pH > 7.64 and pH < 10.04

```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and pH = 8.04 

```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and pH > 8.04 and temperature = 407.67

```


## 3 - queries  
### select
```sql

```
### source 
```sql
explain analyze SELECT "id_station", "temperature" FROM "puncteF"."autogen"."datapoints" WHERE time > '2019-06-20 00:00:00' - 10d and  time < '2019-06-20 00:00:00' AND "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ and temperature > 407.67 
```

### agg 

```sql
explain analyze SELECT mean("temperature") AS "mean_temperature", stddev("temperature") AS "stddev_temperature" FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 90d and  time < '2019-06-20 00:00:00' 

```

### count 
```sql
explain analyze SELECT count("temperature") FROM "puncteF"."autogen"."datapoints" WHERE time > '2019-06-20 00:00:00' - 90d AND  time < '2019-06-20 00:00:00' AND id_station  =~ /32|54|98|25|95|13|80|16|83|27/ GROUP BY "id_station"
```

### full scan
```sql
explain analyze SELECT * FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/
```

### group by 
```sql
explain analyze SELECT mean("temperature") FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 90d AND time < '2019-06-20 00:00:00' GROUP BY "id_station"

```

### downsampling
```sql
explain analyze SELECT mean(*) FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 90d AND time < '2019-06-20 00:00:00' GROUP BY time(1h) FILL(linear)
```

### upsampling
```sql
explain analyze SELECT mean(*) FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 90d AND time < '2019-06-20 00:00:00' GROUP BY time(5s) FILL(linear)
```




### 4 - stations

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32/ AND time > '2019-06-01T00:00:00Z' - 10d AND  time < '2019-06-01T00:00:00Z'
```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 10d AND  time < '2019-06-01T00:00:00Z'
```

```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /45|60|56|40|21|91|52|2|87|83|9|61|31|23|75|19|26|47|17|16|39|58|66|85|65|53|80|29|68|93|10|12|15|84|14|81|3|59|28|7|54|94|0|34|89|71|99|50|67|18|69|30|48|46|95|8|43|74|24|35|79|62|76|37|82|88|5|63|77|1|92|6|41|51|42|44|33|20|4|73|98|57|38|70|27|97|64|36|78|11|72|0|86|90|22|13|32|49|96|25/ AND time > '2019-06-01T00:00:00Z' - 10d AND  time < '2019-06-01T00:00:00Z'
```






## 1 - range 
```sql
-- SELECT count(*) from (select * FROM datapoints where id_station in (32, 54, 98, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00') as res;
```

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=select * from "datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 1d AND  time < '2019-06-01T00:00:00Z'" > /dev/null
```

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=select * from "datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 10d AND  time < '2019-06-01T00:00:00Z'" > /dev/null
```

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=select * from "datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-01T00:00:00Z' - 90d AND  time < '2019-06-01T00:00:00Z'" > /dev/null
```


## 2 - filter 

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=select * from "datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and temperature < 407.67" > /dev/null
```

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=select * from "datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and temperature < 410.67 and temperature >  405.67" > /dev/null

```

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=select * from "datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 10d AND  time < '2019-06-20T00:00:00Z' and temperature > 407.67" > /dev/null

```


## 3 - queries  
### select
```sql

```
### source 
```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=SELECT \"id_station\", \"temperature\" FROM \"puncte\".\"autogen\".\"datapoints\" WHERE time > '2019-06-20 00:00:00' - 10d and  time < '2019-06-20 00:00:00' AND \"id_station\"  =~ /32|54|98|25|95|13|80|16|83|27/ and temperature > 407.67 " > /dev/null
```

### agg 

```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=SELECT mean(\"temperature\") AS \"mean_temperature\", stddev(\"temperature\") AS \"stddev_temperature\" FROM \"puncte\".\"autogen\".\"datapoints\" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 10d and  time < '2019-06-20 00:00:00' " > /dev/null

```

### count 
```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=SELECT count(\"temperature\") FROM \"puncte\".\"autogen\".\"datapoints\" WHERE time > '2019-06-20 00:00:00' - 10d AND  time < '2019-06-20 00:00:00' AND id_station  =~ /32|54|98|25|95|13|80|16|83|27/ GROUP BY \"id_station\"" > /dev/null
```

### full scan
```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=SELECT * FROM \"puncte\".\"autogen\".\"datapoints\" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/" > /dev/null
```

### group by 
```sql
time curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=puncte" --data-urlencode "q=SELECT mean(\"temperature\") FROM \"puncte\".\"autogen\".\"datapoints\" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 10d AND time < '2019-06-20 00:00:00' GROUP BY \"id_station\"" > /dev/null

```

### down 
```sql
SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(pH) AS avg_ph 
FROM datapoints where  id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station, "year", "month", "day", "hour";
```
### up 
```sql
explain analyse SELECT
  time_bucket_gapfill('5 second', time) AS NEWTIME,
  id_station,
  avg(pH) AS avg_value,
  locf(avg(pH))
FROM datapoints
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) AND time < '2019-06-21 00:00:00' AND time > timestamp '2019-06-21 00:00:00' - interval '90 day'
GROUP BY NEWTIME, id_station
ORDER BY NEWTIME;
```

### loop 
```sql

```



## 4 - stations 

```sql
select * FROM datapoints where id_station in (32)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (45,60,56,40,21,91,52,2,87,83,9,61,31,23,75,19,26,47,17,16,39,58,66,85,65,53,80,29,68,93,10,12,15,84,14,81,3,59,28,7,54,94,0,34,89,71,99,50,67,18,69,30,48,46,95,8,43,74,24,35,79,62,76,37,82,88,5,63,77,1,92,6,41,51,42,44,33,20,4,73,98,57,38,70,27,97,64,36,78,11,72,0,86,90,22,13,32,49,96,25)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

# IV- influx 2.1 

## 1 - range 
```sql

```

## 2 - filter 
```sql

```

## 3 - queries  


## 4 - stations 
```sql

```

# V- monetdb

```sql
sql>\f rowcount
```

## 1 - range 
```sql
-- SELECT count(*) from (select * FROM datapoints where id_station in (32, 54, 98, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-26 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-26 00:00:00') as res;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '1' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```


## 2 - filter 

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH < 8.04;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and ph BETWEEN 7.90 and 10.04;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and  pH = 8.04 ;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH = 8.04 and temperature > 407.282;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.04 and temperature = 407.282;
```

## 3 - queries  
### select
```sql

```
### source 
```sql
select id_station, time FROM datapoints where time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.6;
```

### agg 

```sql
SELECT AVG(pH),stddev_pop(pH) 
FROM datapoints 
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' ;
```

### count 
```sql
SELECT id_station, count(*) FROM datapoints where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) group by id_station;
```

### full scan
```sql
SELECT * FROM datapoints where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27);
```
### group by 
```sql
SELECT id_station, avg(pH) FROM datapoints 
WHERE time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station;
```
### down 
```sql
SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(pH) AS avg_ph 
FROM datapoints where  id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station, "year", "month", "day", "hour";
```
### up 
```sql
/
```

### loop 
```sql

```



## 4 - stations 

```sql
select * FROM datapoints where id_station in (32)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (45,60,56,40,21,91,52,2,87,83,9,61,31,23,75,19,26,47,17,16,39,58,66,85,65,53,80,29,68,93,10,12,15,84,14,81,3,59,28,7,54,94,0,34,89,71,99,50,67,18,69,30,48,46,95,8,43,74,24,35,79,62,76,37,82,88,5,63,77,1,92,6,41,51,42,44,33,20,4,73,98,57,38,70,27,97,64,36,78,11,72,0,86,90,22,13,32,49,96,25)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```


# VI- timescale



## 1 - range 
```sql
-- SELECT count(*) from (select * FROM datapoints where id_station in (32, 54, 98, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-26 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-26 00:00:00') as res;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '1' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```


## 2 - filter 

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH < 8.04;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and ph BETWEEN 7.90 and 10.04;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and  pH = 8.04 ;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH = 8.04 and temperature > 407.282;
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.04 and temperature = 407.282;
```

## 3 - queries  
### select
```sql

```
### source 
```sql
select id_station, time FROM datapoints where time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH > 8.6;
```

### agg 

```sql
SELECT AVG(pH),stddev_pop(pH) 
FROM datapoints 
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' ;
```

### count 
```sql
SELECT id_station, count(*) FROM datapoints where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) group by id_station;
```

### full scan
```sql
SELECT * FROM datapoints where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27);
```
### group by 
```sql
SELECT id_station, avg(pH) FROM datapoints 
WHERE time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station;
```
### down 
```sql
SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(pH) AS avg_ph 
FROM datapoints where  id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station, "year", "month", "day", "hour";
```
### up 
```sql
explain analyse SELECT
  time_bucket_gapfill('5 second', time) AS NEWTIME,
  id_station,
  avg(pH) AS avg_value,
  locf(avg(pH))
FROM datapoints
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) AND time < '2019-06-21 00:00:00' AND time > timestamp '2019-06-21 00:00:00' - interval '90 day'
GROUP BY NEWTIME, id_station
ORDER BY NEWTIME;
```

### loop 
```sql

```



## 4 - stations 

```sql
select * FROM datapoints where id_station in (32)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

```sql
select * FROM datapoints where id_station in (45,60,56,40,21,91,52,2,87,83,9,61,31,23,75,19,26,47,17,16,39,58,66,85,65,53,80,29,68,93,10,12,15,84,14,81,3,59,28,7,54,94,0,34,89,71,99,50,67,18,69,30,48,46,95,8,43,74,24,35,79,62,76,37,82,88,5,63,77,1,92,6,41,51,42,44,33,20,4,73,98,57,38,70,27,97,64,36,78,11,72,0,86,90,22,13,32,49,96,25)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

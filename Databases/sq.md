# I- druid


## Q1 - full scan 


```sql
select * FROM bafu_comma3 where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' 
```

## Q2 - filter


```sql
select id_station, pH FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00' and pH < 8.04
```


## Q3 - agg group order by station

```sql
select id_station,AVG(pH)  FROM bafu_comma where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and __time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '10' DAY
and __time < TIMESTAMP '2019-06-20 00:00:00'
GROUP BY id_station
```

## Q4 - downsampling

 
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


## Q5 - upsampling

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



# II- extreme






## Q1 - full scan 


```sql
select flattened seq_search(t,1560988800 - 90 * 24 * 60 * 60,1560988800) as tt, id_station, water_temperature@tt, Discharge@tt, pH@tt, oxygen@tt, oxygen_saturation@tt FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27);
```

## Q2 - filter


```sql
select flattened seq_search(t,1560988800 - 2 * 24 * 60 * 60,1560988800) as tt, !seq_filter_search(pH@tt > 8.04, tt) as fe, water_temperature@fe, Discharge@fe, pH@fe, oxygen@fe, oxygen_saturation@fe FROM datapoints_v WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27);
```


## Q3 - agg group order by station

```sql
SELECT flattened id_station, avg(pH) FROM datapoints_v group by id_station;
```

## Q4 - downsampling

 
```sql
select flattened id_station, seq_search(t,1559390400 - 20 * 24 * 60 * 60,1559390400) as tt, t@tt/3600 as hour, seq_group_agg_dev(pH@tt, t@tt/3600) FROM datapoints_v WHERE id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27);
```

## Q5 - upsampling

```sql
select flattened seq_aprogres_datetime(1551398400, 5, 90 * 24 * 60 * 60) as ts5,seq_stretch(ts5,t,pH) from datapoints_v where id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27);
```






# III- influx 1.7




## Q1 - full scan 


```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-21T00:00:00Z' - 90d AND  time < '2019-06-01T00:00:00Z'
```

## Q2 - filter


```sql
explain analyze select * FROM "puncteF"."autogen"."datapoints" where "id_station"  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20T00:00:00Z' - 2d AND  time < '2019-06-20T00:00:00Z' and pH > 8.04
```


## Q3 - agg group order by station

```sql
explain analyze SELECT mean("temperature") FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 20d AND time < '2019-06-20 00:00:00' GROUP BY "id_station"
```

## Q4 - downsampling

 
```sql
explain analyze SELECT mean(*) FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 80d AND time < '2019-06-20 00:00:00' GROUP BY time(1h) FILL(linear)
```

## Q5 - upsampling

```sql
explain analyze SELECT mean(*) FROM "puncteF"."autogen"."datapoints" WHERE id_station  =~ /32|54|98|25|95|13|80|16|83|27/ AND time > '2019-06-20 00:00:00' - 20d AND time < '2019-06-20 00:00:00' GROUP BY time(5s) FILL(linear)
```




# IV- influx 2.1 

## Q1 - full scan 


```sql
```

## Q2 - filter


```sql
```


## Q3 - agg group order by station

```sql
```

## Q4 - downsampling

 
```sql
```

## Q5 - upsampling

```sql
```



# V- monetdb

```sql
sql>\f rowcount
```


## Q1 - full scan 


```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '100' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

## Q2 - filter


```sql
select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '2' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH < 8.04;
```


## Q3 - agg group order by station

```sql
SELECT id_station, AVG(pH)
FROM datapoints 
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '20' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00'
GROUP BY (id_station)
ORDER BY (id_station);
```

## Q4 - downsampling

 
```sql
SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(pH) AS avg_ph 
FROM datapoints where  id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '20' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station, "year", "month", "day", "hour";
```

## Q5 - upsampling

```sql
```


# VI- timescale




## Q1 - full scan 


```sql
explain analyze select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '90' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00';
```

## Q2 - filter


```sql
explain analyze select * FROM datapoints where id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
AND time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '4' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' and pH < 8.04;
```

### group by 
```sql
explain analyze SELECT id_station, avg(pH) FROM datapoints 
WHERE time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '20' DAY 
AND time < TIMESTAMP '2019-06-20 00:00:00' 
GROUP BY id_station;
```
### down 
```sql
explain analyze SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(pH) AS avg_ph 
FROM datapoints where  id_station IN (32, 54, 8, 25, 95, 13, 80, 16, 83, 27)
and time > TIMESTAMP '2019-06-20 00:00:00' - INTERVAL '20' DAY 
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
WHERE id_station in (32, 54, 8, 25, 95, 13, 80, 16, 83, 27) AND time < '2019-06-21 00:00:00' AND time > timestamp '2019-06-21 00:00:00' - interval '20 day'
GROUP BY NEWTIME, id_station
ORDER BY NEWTIME;
```


# I- druid

```sql
Load: 
time ./apache-druid-0.22.0/bin/post-index-task --file import-config.json --url http://localhost:8081
```


## Q1 - full scan 



```sql
select * FROM d1 where id_station in ('st5') and s='s14'
and __time > TIMESTAMP '2019-03-20 00:00:00' - INTERVAL '1' DAY
and __time < TIMESTAMP '2019-03-20 00:00:00' 
```

## Q2 - filter


```sql
SELECT
  "__time",
  "value"
FROM d1
WHERE  id_station in ('st5')
AND __time > TIMESTAMP '2019-03-20 00:00:00' - INTERVAL '7' DAY
and __time < TIMESTAMP '2019-03-20 00:00:00' AND "value" > 0.95 AND s = 's8'
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
SELECT "id_station", TIME_EXTRACT(__time, 'YEAR')  AS "yearP",
TIME_EXTRACT(__time, 'MONTH') AS "month", 
TIME_EXTRACT(__time, 'DAY') AS "day", 
TIME_EXTRACT(__time, 'HOUR') AS "hour", 
AVG("value") 
FROM d1 where __time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '7' DAY 
AND __time < TIMESTAMP '2019-04-20 00:00:00' GROUP BY 1,2,3,4,5

```


## Q5 - upsampling

```json
{
  "queryType": "timeseries",
  "dataSource": "d1",
  "granularity": {"type": "duration", "duration": 5000},
  "aggregations": [
    { "type": "doubleFirst", "name": "value", "fieldName": "value" }
  ],
  "filter": { "type": "selector", "dimension": "s", "value": 's4' },
  "intervals": [ "2019-03-01T00:00:00.000/2019-03-04T00:00:00.000" ],
  "context" : {
    "skipEmptyBuckets": "false"
  }
}

```



# II- extreme
```

export MCO_ROOT=/opt/mcobject/eXtremeDB
find ~ -name libmcopythonapi.so
export MCO_PYTHONAPILIB=/corresponding-path....../libmcopythonapi.so
export MCO_ROOT=/home/abdel/TS-Benchmark/databases/extremedb/eXtremeDB/                                                                               
export LD_LIBRARY_PATH=/home/abdel/TS-Benchmark/databases/extremedb/eXtremeDB/target/bin.so/     
export MCO_LIBRARY_PATH=/home/abdel/TS-Benchmark/databases/extremedb/eXtremeDB/target/bin.so/                                                        

Run before running Jupyter on the same terminal session!!!

./xsql -i -c xsql.cfg -p 5001
trace on


awk -F, '{ print $2 "," $1 "," $3 "," $4 "," $5 "," $6 "," $7 "," $8 "," $9 "," $10 "," $11 "," $12 "," $13 "," $14 "," $15 "," $16 "," $17 "," $18 "," $19 "," $20 "," $21 "," $22 "," $23 "," $24 "," $25 "," $26 "," $27 "," $28 "," $29 "," $30 "," $31 "," $32 "," $33 "," $34 "," $35 "," $36 "," $37 "," $38 "," $39 "," $40 "," $41 "," $42 "," $43 "," $44 "," $45 "," $46 "," $47 "," $48 "," $49 "," $50 "," $51 "," $52 "," $53 "," $54 "," $55 "," $56 "," $57 "," $58 "," $59 "," $60 "," $61 "," $62 "," $63 "," $64 "," $65 "," $66 "," $67 "," $68 "," $69 "," $70 "," $71 "," $72 "," $73 "," $74 "," $75 "," $76 "," $77 "," $78 "," $79 "," $80 "," $81 "," $82 "," $83 "," $84 "," $85 "," $86 "," $87 "," $88 "," $89 "," $90 "," $91 "," $92 "," $93 "," $94 "," $95 "," $96 "," $97 "," $98 "," $99}' d1.csv > d1_inversed.csv

drop table d1_h; 
drop table d1_v; 

set append_mode = true;

CREATE TABLE d1_h ( t string, id_station string, s0 DOUBLE, s1 DOUBLE, s2 DOUBLE, s3 DOUBLE, s4 DOUBLE, s5 DOUBLE, s6 DOUBLE, s7 DOUBLE, s8 DOUBLE, s9 DOUBLE, s10 DOUBLE, s11 DOUBLE, s12 DOUBLE, s13 DOUBLE, s14 DOUBLE, s15 DOUBLE, s16 DOUBLE, s17 DOUBLE, s18 DOUBLE, s19 DOUBLE, s20 DOUBLE, s21 DOUBLE, s22 DOUBLE, s23 DOUBLE, s24 DOUBLE, s25 DOUBLE, s26 DOUBLE, s27 DOUBLE, s28 DOUBLE, s29 DOUBLE, s30 DOUBLE, s31 DOUBLE, s32 DOUBLE, s33 DOUBLE, s34 DOUBLE, s35 DOUBLE, s36 DOUBLE, s37 DOUBLE, s38 DOUBLE, s39 DOUBLE, s40 DOUBLE, s41 DOUBLE, s42 DOUBLE, s43 DOUBLE, s44 DOUBLE, s45 DOUBLE, s46 DOUBLE, s47 DOUBLE, s48 DOUBLE, s49 DOUBLE, s50 DOUBLE, s51 DOUBLE, s52 DOUBLE, s53 DOUBLE, s54 DOUBLE, s55 DOUBLE, s56 DOUBLE, s57 DOUBLE, s58 DOUBLE, s59 DOUBLE, s60 DOUBLE, s61 DOUBLE, s62 DOUBLE, s63 DOUBLE, s64 DOUBLE, s65 DOUBLE, s66 DOUBLE, s67 DOUBLE, s68 DOUBLE, s69 DOUBLE, s70 DOUBLE, s71 DOUBLE, s72 DOUBLE, s73 DOUBLE, s74 DOUBLE, s75 DOUBLE, s76 DOUBLE, s77 DOUBLE, s78 DOUBLE, s79 DOUBLE, s80 DOUBLE, s81 DOUBLE, s82 DOUBLE, s83 DOUBLE, s84 DOUBLE, s85 DOUBLE, s86 DOUBLE, s87 DOUBLE, s88 DOUBLE, s89 DOUBLE, s90 DOUBLE, s91 DOUBLE, s92 DOUBLE, s93 DOUBLE, s94 DOUBLE, s95 DOUBLE, s96 DOUBLE, s97 DOUBLE, s98 DOUBLE, s99 DOUBLE);

CREATE TABLE d1_v (id_station string PRIMARY KEY, t sequence(TIMESTAMP asc), s0 sequence(DOUBLE), s1 sequence(DOUBLE), s2 sequence(DOUBLE), s3 sequence(DOUBLE), s4 sequence(DOUBLE), s5 sequence(DOUBLE), s6 sequence(DOUBLE), s7 sequence(DOUBLE), s8 sequence(DOUBLE), s9 sequence(DOUBLE), s10 sequence(DOUBLE), s11 sequence(DOUBLE), s12 sequence(DOUBLE), s13 sequence(DOUBLE), s14 sequence(DOUBLE), s15 sequence(DOUBLE), s16 sequence(DOUBLE), s17 sequence(DOUBLE), s18 sequence(DOUBLE), s19 sequence(DOUBLE), s20 sequence(DOUBLE), s21 sequence(DOUBLE), s22 sequence(DOUBLE), s23 sequence(DOUBLE), s24 sequence(DOUBLE), s25 sequence(DOUBLE), s26 sequence(DOUBLE), s27 sequence(DOUBLE), s28 sequence(DOUBLE), s29 sequence(DOUBLE), s30 sequence(DOUBLE), s31 sequence(DOUBLE), s32 sequence(DOUBLE), s33 sequence(DOUBLE), s34 sequence(DOUBLE), s35 sequence(DOUBLE), s36 sequence(DOUBLE), s37 sequence(DOUBLE), s38 sequence(DOUBLE), s39 sequence(DOUBLE), s40 sequence(DOUBLE), s41 sequence(DOUBLE), s42 sequence(DOUBLE), s43 sequence(DOUBLE), s44 sequence(DOUBLE), s45 sequence(DOUBLE), s46 sequence(DOUBLE), s47 sequence(DOUBLE), s48 sequence(DOUBLE), s49 sequence(DOUBLE), s50 sequence(DOUBLE), s51 sequence(DOUBLE), s52 sequence(DOUBLE), s53 sequence(DOUBLE), s54 sequence(DOUBLE), s55 sequence(DOUBLE), s56 sequence(DOUBLE), s57 sequence(DOUBLE), s58 sequence(DOUBLE), s59 sequence(DOUBLE), s60 sequence(DOUBLE), s61 sequence(DOUBLE), s62 sequence(DOUBLE), s63 sequence(DOUBLE), s64 sequence(DOUBLE), s65 sequence(DOUBLE), s66 sequence(DOUBLE), s67 sequence(DOUBLE), s68 sequence(DOUBLE), s69 sequence(DOUBLE), s70 sequence(DOUBLE), s71 sequence(DOUBLE), s72 sequence(DOUBLE), s73 sequence(DOUBLE), s74 sequence(DOUBLE), s75 sequence(DOUBLE), s76 sequence(DOUBLE), s77 sequence(DOUBLE), s78 sequence(DOUBLE), s79 sequence(DOUBLE), s80 sequence(DOUBLE), s81 sequence(DOUBLE), s82 sequence(DOUBLE), s83 sequence(DOUBLE), s84 sequence(DOUBLE), s85 sequence(DOUBLE), s86 sequence(DOUBLE), s87 sequence(DOUBLE), s88 sequence(DOUBLE), s89 sequence(DOUBLE), s90 sequence(DOUBLE), s91 sequence(DOUBLE), s92 sequence(DOUBLE), s93 sequence(DOUBLE), s94 sequence(DOUBLE), s95 sequence(DOUBLE), s96 sequence(DOUBLE), s97 sequence(DOUBLE), s98 sequence(DOUBLE), s99 sequence(DOUBLE));

trace on

insert or update into d1_v select id_station,(substr(t,1,10)||' '||substr(t,12,8))::timestamp::bigint,s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42,s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73,s74,s75,s76,s77,s78,s79,s80,s81,s82,s83,s84,s85,s86,s87,s88,s89,s90,s91,s92,s93,s94,s95,s96,s97,s98,s99 from foreign table(path='/home/abdel/d1_data/d1.csv', skip=1) as d1_h;


```



## Q1 - full scan 


```sql
select seq_search(t,1556457832 - 2 * 3600,1556457832) as tt, id_station, s5@tt FROM d1_v WHERE id_station = 'st3';

```

## Q2 - filter


```sql
SELECT flattened id_station, avg(s5) FROM d1_v group by id_station;
    ```


## Q3 - agg group order by station

```sql
SELECT id_station, avg(s5) FROM d1_v \
            group by id_station;
    ```

## Q4 - downsampling

 
```sql
select flattened id_station, seq_search(t,<timestamp> - 20 * 24 * 60 * 60,<timestamp>) as tt, t@tt/3600 as hour, seq_group_agg_dev(s45@tt, t@tt/3600) FROM d1_v WHERE id_station = 'st9'
```

## Q5 - upsampling

```sql
select flattened seq_aprogres_datetime(1551398400, 5, 90 * 24 * 60 * 60) as ts5,seq_stretch(ts5,t,pH) from d1_v where id_station = 'st3';
```






# III- influx 1.7
```sql

sudo ./influxd
./influx 

influx -import -path=/localdata/influxdb.csv -precision=ms

cd root@diufrm118:~/.influxdb/data/
```




## Q1 -


```sql
explain analyze select * FROM "d1"."autogen"."datapoints" where "id_station" ='st8' AND "s" ='s8' AND time > '2019-03-23T00:00:00Z' - 1d AND  time < '2019-03-23T00:00:00Z'
```

## Q2 - filter


```sql
explain analyze select * FROM "d1"."autogen"."datapoints" where "id_station" ='st8' AND "s" ='s8' AND time > '2019-03-23T00:00:00Z' - 1w AND  time < '2019-03-23T00:00:00Z' and value > 0.95
```


## Q3 - agg group order by station

```sql
explain analyze SELECT mean(value) FROM "d1"."autogen"."datapoints" WHERE  "s" ='s8' AND time > '2019-04-20 00:00:00' - 30d AND time < '2019-04-20 00:00:00' GROUP BY "id_station"   
```

## Q4 - downsampling

 
```sql
explain analyze SELECT first(id_station), mean(value) FROM "d1"."autogen"."datapoints" WHERE time > '2019-04-20 00:00:00' - 7d AND s='s7' and time < '2019-04-20 00:00:00' GROUP BY id_station,time(1h)

```

## Q5 - upsampling

```sql
explain analyze SELECT id_station, mean_value FROM (SELECT mean(value) as mean_value FROM "d1"."autogen"."datapoints" WHERE time > '2019-03-20 00:00:00' - 15m AND time < '2019-03-20 00:00:00' GROUP BY id_station,time(5s) FILL(0)) GROUP BY id_station
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
mclient -p54320 -u monetdb -d mydb --interactive --timer=performance
sql>\f rowcount
```

```
CREATE TABLE d1 ( 
        time TIMESTAMP NOT NULL, 
        id_station STRING, s0 DOUBLE PRECISION , s1 DOUBLE PRECISION , s2 DOUBLE PRECISION , s3 DOUBLE PRECISION , s4 DOUBLE PRECISION , s5 DOUBLE PRECISION , s6 DOUBLE PRECISION , s7 DOUBLE PRECISION , s8 DOUBLE PRECISION , s9 DOUBLE PRECISION , s10 DOUBLE PRECISION , s11 DOUBLE PRECISION , s12 DOUBLE PRECISION , s13 DOUBLE PRECISION , s14 DOUBLE PRECISION , s15 DOUBLE PRECISION , s16 DOUBLE PRECISION , s17 DOUBLE PRECISION , s18 DOUBLE PRECISION , s19 DOUBLE PRECISION , s20 DOUBLE PRECISION , s21 DOUBLE PRECISION , s22 DOUBLE PRECISION , s23 DOUBLE PRECISION , s24 DOUBLE PRECISION , s25 DOUBLE PRECISION , s26 DOUBLE PRECISION , s27 DOUBLE PRECISION , s28 DOUBLE PRECISION , s29 DOUBLE PRECISION , s30 DOUBLE PRECISION , s31 DOUBLE PRECISION , s32 DOUBLE PRECISION , s33 DOUBLE PRECISION , s34 DOUBLE PRECISION , s35 DOUBLE PRECISION , s36 DOUBLE PRECISION , s37 DOUBLE PRECISION , s38 DOUBLE PRECISION , s39 DOUBLE PRECISION , s40 DOUBLE PRECISION , s41 DOUBLE PRECISION , s42 DOUBLE PRECISION , s43 DOUBLE PRECISION , s44 DOUBLE PRECISION , s45 DOUBLE PRECISION , s46 DOUBLE PRECISION , s47 DOUBLE PRECISION , s48 DOUBLE PRECISION , s49 DOUBLE PRECISION , s50 DOUBLE PRECISION , s51 DOUBLE PRECISION , s52 DOUBLE PRECISION , s53 DOUBLE PRECISION , s54 DOUBLE PRECISION , s55 DOUBLE PRECISION , s56 DOUBLE PRECISION , s57 DOUBLE PRECISION , s58 DOUBLE PRECISION , s59 DOUBLE PRECISION , s60 DOUBLE PRECISION , s61 DOUBLE PRECISION , s62 DOUBLE PRECISION , s63 DOUBLE PRECISION , s64 DOUBLE PRECISION , s65 DOUBLE PRECISION , s66 DOUBLE PRECISION , s67 DOUBLE PRECISION , s68 DOUBLE PRECISION , s69 DOUBLE PRECISION , s70 DOUBLE PRECISION , s71 DOUBLE PRECISION , s72 DOUBLE PRECISION , s73 DOUBLE PRECISION , s74 DOUBLE PRECISION , s75 DOUBLE PRECISION , s76 DOUBLE PRECISION , s77 DOUBLE PRECISION , s78 DOUBLE PRECISION , s79 DOUBLE PRECISION , s80 DOUBLE PRECISION , s81 DOUBLE PRECISION , s82 DOUBLE PRECISION , s83 DOUBLE PRECISION , s84 DOUBLE PRECISION , s85 DOUBLE PRECISION , s86 DOUBLE PRECISION , s87 DOUBLE PRECISION , s88 DOUBLE PRECISION , s89 DOUBLE PRECISION , s90 DOUBLE PRECISION , s91 DOUBLE PRECISION , s92 DOUBLE PRECISION , s93 DOUBLE PRECISION , s94 DOUBLE PRECISION , s95 DOUBLE PRECISION , s96 DOUBLE PRECISION , s97 DOUBLE PRECISION , s98 DOUBLE PRECISION , 
        s99 DOUBLE PRECISION
        );
        
COPY OFFSET 2 INTO d1 FROM '/home/abdel/d1_data/d1.csv' USING DELIMITERS ',','\n';

```

## Q1


```sql
select time, s91 FROM d1 where id_station='st4' 
AND time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '1' DAY 
AND time < TIMESTAMP '2019-04-20 00:00:00';
```

## Q2 - filter


```sql
select time, s91 FROM d1 where id_station='st4' 
AND time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '7' DAY 
AND time < TIMESTAMP '2019-04-20 00:00:00' AND s91>0.95;
```


## Q3 - agg group order by station

```sql
SELECT id_station, avg(s4) FROM d1 
WHERE time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '30' DAY 
AND time < TIMESTAMP '2019-04-20 00:00:00' 
GROUP BY id_station;
```

## Q4 - downsampling

 
```sql
SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(s9) AS avg_s9
FROM d1 where  time > TIMESTAMP '2019-04-25 00:00:00' - INTERVAL '7' DAY 
AND time < TIMESTAMP '2019-04-25 00:00:00' 
GROUP BY id_station, "year", "month", "day", "hour";
```

## Q5 - upsampling

```sql
```




# VII- questdb

```sql
cairo.sql.copy.root=
vim /root/.questdb/conf/server.conf 
# https://questdb.io/docs/operations/capacity-planning/#max-virtual-memory-areas-limit
http://diufrm108:9000/#

COPY d1temp FROM '/home/abdel/d1_data/d1.csv'
CREATE TABLE d1 AS (
SELECT
    cast(time AS timestamp) ts, 
    cast(id_station AS symbol) id_station,
    s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38, s39, s40, s41, s42, s43, s44, s45, s46, s47, s48, s49, s50, s51, s52, s53, s54, s55, s56, s57, s58, s59, s60, s61, s62, s63, s64, s65, s66, s67, s68, s69, s70, s71, s72, s73, s74, s75, s76, s77, s78, s79, s80, s81, s82, s83, s84, s85, s86, s87, s88, s89, s90, s91, s92, s93, s94, s95, s96, s97, s98, s99
FROM 'd1temp' 
), index (id_station) timestamp(ts) PARTITION BY MONTH;
DROP TABLE d1temp;


COPY d2temp FROM '/home/abdel/d2_data/short_ts/short_ts_date.csv'

CREATE TABLE d2 AS (
SELECT
    cast(f0 AS timestamp) ts, 
    cast(f1 AS symbol) id_station,
    f2 as s0,f3 as s1,f4 as s2,f5 as s3,f6 as s4,f7 as s5,f8 as s6,f9 as s7,f10 as s8,f11 as s9,f12 as s10,f13 as s11,f14 as s12,f15 as s13,f16 as s14,f17 as s15,f18 as s16,f19 as s17,f20 as s18,f21 as s19,f22 as s20,f23 as s21,f24 as s22,f25 as s23,f26 as s24,f27 as s25,f28 as s26,f29 as s27,f30 as s28,f31 as s29,f32 as s30,f33 as s31,f34 as s32,f35 as s33,f36 as s34,f37 as s35,f38 as s36,f39 as s37,f40 as s38,f41 as s39,f42 as s40,f43 as s41,f44 as s42,f45 as s43,f46 as s44,f47 as s45,f48 as s46,f49 as s47,f50 as s48,f51 as s49,f52 as s50,f53 as s51,f54 as s52,f55 as s53,f56 as s54,f57 as s55,f58 as s56,f59 as s57,f60 as s58,f61 as s59,f62 as s60,f63 as s61,f64 as s62,f65 as s63,f66 as s64,f67 as s65,f68 as s66,f69 as s67,f70 as s68,f71 as s69,f72 as s70,f73 as s71,f74 as s72,f75 as s73,f76 as s74,f77 as s75,f78 as s76,f79 as s77,f80 as s78,f81 as s79,f82 as s80,f83 as s81,f84 as s82,f85 as s83,f86 as s84,f87 as s85,f88 as s86,f89 as s87,f90 as s88,f91 as s89,f92 as s90,f93 as s91,f94 as s92,f95 as s93,f96 as s94,f97 as s95,f98 as s96,f99 as s97,f100 as s98,f101 as s99
FROM 'd2temp' 
), index (id_station) timestamp(ts) PARTITION BY MONTH WITH maxUncommittedRows=250000, commitLag=240s;


INSERT INTO d2
SELECT
    cast(f0 AS timestamp) ts, 
    cast(f1 AS symbol) id_station,
    f2 as s0,f3 as s1,f4 as s2,f5 as s3,f6 as s4,f7 as s5,f8 as s6,f9 as s7,f10 as s8,f11 as s9,f12 as s10,f13 as s11,f14 as s12,f15 as s13,f16 as s14,f17 as s15,f18 as s16,f19 as s17,f20 as s18,f21 as s19,f22 as s20,f23 as s21,f24 as s22,f25 as s23,f26 as s24,f27 as s25,f28 as s26,f29 as s27,f30 as s28,f31 as s29,f32 as s30,f33 as s31,f34 as s32,f35 as s33,f36 as s34,f37 as s35,f38 as s36,f39 as s37,f40 as s38,f41 as s39,f42 as s40,f43 as s41,f44 as s42,f45 as s43,f46 as s44,f47 as s45,f48 as s46,f49 as s47,f50 as s48,f51 as s49,f52 as s50,f53 as s51,f54 as s52,f55 as s53,f56 as s54,f57 as s55,f58 as s56,f59 as s57,f60 as s58,f61 as s59,f62 as s60,f63 as s61,f64 as s62,f65 as s63,f66 as s64,f67 as s65,f68 as s66,f69 as s67,f70 as s68,f71 as s69,f72 as s70,f73 as s71,f74 as s72,f75 as s73,f76 as s74,f77 as s75,f78 as s76,f79 as s77,f80 as s78,f81 as s79,f82 as s80,f83 as s81,f84 as s82,f85 as s83,f86 as s84,f87 as s85,f88 as s86,f89 as s87,f90 as s88,f91 as s89,f92 as s90,f93 as s91,f94 as s92,f95 as s93,f96 as s94,f97 as s95,f98 as s96,f99 as s97,f100 as s98,f101 as s99
FROM 'd2temp'

CREATE TABLE ddd (
    ts timestamp, 
    id_station symbol,
    s0 DOUBLE, s1 DOUBLE, s2 DOUBLE, s3 DOUBLE, s4 DOUBLE, s5 DOUBLE, s6 DOUBLE, s7 DOUBLE, s8 DOUBLE, s9 DOUBLE, s10 DOUBLE, s11 DOUBLE, s12 DOUBLE, s13 DOUBLE, s14 DOUBLE, s15 DOUBLE, s16 DOUBLE, s17 DOUBLE, s18 DOUBLE, s19 DOUBLE, s20 DOUBLE, s21 DOUBLE, s22 DOUBLE, s23 DOUBLE, s24 DOUBLE, s25 DOUBLE, s26 DOUBLE, s27 DOUBLE, s28 DOUBLE, s29 DOUBLE, s30 DOUBLE, s31 DOUBLE, s32 DOUBLE, s33 DOUBLE, s34 DOUBLE, s35 DOUBLE, s36 DOUBLE, s37 DOUBLE, s38 DOUBLE, s39 DOUBLE, s40 DOUBLE, s41 DOUBLE, s42 DOUBLE, s43 DOUBLE, s44 DOUBLE, s45 DOUBLE, s46 DOUBLE, s47 DOUBLE, s48 DOUBLE, s49 DOUBLE, s50 DOUBLE, s51 DOUBLE, s52 DOUBLE, s53 DOUBLE, s54 DOUBLE, s55 DOUBLE, s56 DOUBLE, s57 DOUBLE, s58 DOUBLE, s59 DOUBLE, s60 DOUBLE, s61 DOUBLE, s62 DOUBLE, s63 DOUBLE, s64 DOUBLE, s65 DOUBLE, s66 DOUBLE, s67 DOUBLE, s68 DOUBLE, s69 DOUBLE, s70 DOUBLE, s71 DOUBLE, s72 DOUBLE, s73 DOUBLE, s74 DOUBLE, s75 DOUBLE, s76 DOUBLE, s77 DOUBLE, s78 DOUBLE, s79 DOUBLE, s80 DOUBLE, s81 DOUBLE, s82 DOUBLE, s83 DOUBLE, s84 DOUBLE, s85 DOUBLE, s86 DOUBLE, s87 DOUBLE, s88 DOUBLE, s89 DOUBLE, s90 DOUBLE, s91 DOUBLE, s92 DOUBLE, s93 DOUBLE, s94 DOUBLE, s95 DOUBLE, s96 DOUBLE, s97 DOUBLE, s98 DOUBLE, s99 DOUBLE
), index (id_station) timestamp(ts);
insert batch 7000000 commitLag 1800d into ddd


drop table 'd1temp';
```

## Q1

```sql
select ts, s9 FROM d1 where id_station='st4' AND ts IN '2019-03-27;1d'
```


## Q2

```sql
select ts, s9 FROM d1 where id_station='st4' AND ts IN '2019-03-27;7d' and s9 > 0.95;
```


## Q3 

```sql
SELECT id_station, avg(s4) FROM d1 
WHERE ts IN '2019-03-27;30d'
GROUP BY id_station;
```

## Q4 - Downsamling 

```sql
SELECT ts, avg(s9)
FROM d1
WHERE ts IN '2019-02-27;1w'
SAMPLE BY 1h;
```


## Q5 - Upsampling

```sql
SELECT id_station, ts, avg(s0)
FROM d1
WHERE ts IN '2019-03-07;15m'
SAMPLE BY 5s FILL(LINEAR)
GROUP BY id_station,ts
ORDER BY id_station, ts;

```



# VI- timescale



```
set jit = off;
psql -U postgres postgres

CREATE TABLE d1 ( 
        time TIMESTAMP NOT NULL, 
        id_station VARCHAR(4) NOT NULL, s0 DOUBLE PRECISION , s1 DOUBLE PRECISION , s2 DOUBLE PRECISION , s3 DOUBLE PRECISION , s4 DOUBLE PRECISION , s5 DOUBLE PRECISION , s6 DOUBLE PRECISION , s7 DOUBLE PRECISION , s8 DOUBLE PRECISION , s9 DOUBLE PRECISION , s10 DOUBLE PRECISION , s11 DOUBLE PRECISION , s12 DOUBLE PRECISION , s13 DOUBLE PRECISION , s14 DOUBLE PRECISION , s15 DOUBLE PRECISION , s16 DOUBLE PRECISION , s17 DOUBLE PRECISION , s18 DOUBLE PRECISION , s19 DOUBLE PRECISION , s20 DOUBLE PRECISION , s21 DOUBLE PRECISION , s22 DOUBLE PRECISION , s23 DOUBLE PRECISION , s24 DOUBLE PRECISION , s25 DOUBLE PRECISION , s26 DOUBLE PRECISION , s27 DOUBLE PRECISION , s28 DOUBLE PRECISION , s29 DOUBLE PRECISION , s30 DOUBLE PRECISION , s31 DOUBLE PRECISION , s32 DOUBLE PRECISION , s33 DOUBLE PRECISION , s34 DOUBLE PRECISION , s35 DOUBLE PRECISION , s36 DOUBLE PRECISION , s37 DOUBLE PRECISION , s38 DOUBLE PRECISION , s39 DOUBLE PRECISION , s40 DOUBLE PRECISION , s41 DOUBLE PRECISION , s42 DOUBLE PRECISION , s43 DOUBLE PRECISION , s44 DOUBLE PRECISION , s45 DOUBLE PRECISION , s46 DOUBLE PRECISION , s47 DOUBLE PRECISION , s48 DOUBLE PRECISION , s49 DOUBLE PRECISION , s50 DOUBLE PRECISION , s51 DOUBLE PRECISION , s52 DOUBLE PRECISION , s53 DOUBLE PRECISION , s54 DOUBLE PRECISION , s55 DOUBLE PRECISION , s56 DOUBLE PRECISION , s57 DOUBLE PRECISION , s58 DOUBLE PRECISION , s59 DOUBLE PRECISION , s60 DOUBLE PRECISION , s61 DOUBLE PRECISION , s62 DOUBLE PRECISION , s63 DOUBLE PRECISION , s64 DOUBLE PRECISION , s65 DOUBLE PRECISION , s66 DOUBLE PRECISION , s67 DOUBLE PRECISION , s68 DOUBLE PRECISION , s69 DOUBLE PRECISION , s70 DOUBLE PRECISION , s71 DOUBLE PRECISION , s72 DOUBLE PRECISION , s73 DOUBLE PRECISION , s74 DOUBLE PRECISION , s75 DOUBLE PRECISION , s76 DOUBLE PRECISION , s77 DOUBLE PRECISION , s78 DOUBLE PRECISION , s79 DOUBLE PRECISION , s80 DOUBLE PRECISION , s81 DOUBLE PRECISION , s82 DOUBLE PRECISION , s83 DOUBLE PRECISION , s84 DOUBLE PRECISION , s85 DOUBLE PRECISION , s86 DOUBLE PRECISION , s87 DOUBLE PRECISION , s88 DOUBLE PRECISION , s89 DOUBLE PRECISION , s90 DOUBLE PRECISION , s91 DOUBLE PRECISION , s92 DOUBLE PRECISION , s93 DOUBLE PRECISION , s94 DOUBLE PRECISION , s95 DOUBLE PRECISION , s96 DOUBLE PRECISION , s97 DOUBLE PRECISION , s98 DOUBLE PRECISION , 
        s99 DOUBLE PRECISION
        );
SELECT create_hypertable('d1', 'time', chunk_time_interval=>'7 days'::INTERVAL);
time timescaledb-parallel-copy -file /home/abdel/d1_data/d1.csv -skip-header --table d1 -connection "host=localhost user=postgres password=postgres" --workers 20
time PGPASSWORD=postgres psql -U postgres -d postgres -c "COPY d1 FROM'/home/abdel/d1_data/d1.csv' DELIMITER ',' CSV HEADER;"; 

ALTER TABLE d1 SET (timescaledb.compress, timescaledb.compress_segmentby='id_station');
SELECT compress_chunk(i) FROM show_chunks('d1') i ORDER BY i DESC OFFSET 1;



CREATE TABLE d1_narrow ( 
        time TIMESTAMP NOT NULL, 
        id_station VARCHAR(4) NOT NULL, sid VARCHAR(4) NOT NULL, value DOUBLE PRECISION
        );
SELECT create_hypertable('d1_narrow', 'time', chunk_time_interval=>'7 days'::INTERVAL);
SELECT hypertable_size('d1_narrow') ;
time timescaledb-parallel-copy -file /home/abdel/d1_data/d1_narrow.csv -skip-header --table d1_narrow -connection "host=localhost user=postgres password=postgres" --workers 20
time PGPASSWORD=postgres psql -U postgres -d postgres -c "COPY d1_narrow FROM'/home/abdel/d1_data/d1_narrow.csv' DELIMITER ',' CSV HEADER;"; 

ALTER TABLE d1_narrow SET (timescaledb.compress, timescaledb.compress_segmentby='id_station, sid');
SELECT compress_chunk(i) FROM show_chunks('d1_narrow') i ORDER BY i DESC OFFSET 1;


time timescaledb-parallel-copy -file /home/abdel/d1_data/d1_narrow.csv -skip-header --table d1_narrow -connection "host=localhost user=postgres password=postgres" --workers 20

SELECT hypertable_size('d1') ;


# COPY d1 FROM'/home/abdel/d1_data/d1.csv' DELIMITER ',' CSV HEADER;
# WRONG: SELECT create_hypertable('d1', 'time', 'id_station', 10);
# WRONG: CREATE INDEX ON d1 (id_station, time DESC);

```

## Q1 -


```sql
explain analyze select time, s4 FROM d1 where id_station='st1'
AND time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '1' DAY 
AND time < TIMESTAMP '2019-04-20 00:00:00';
```

## Q2 - filter


```sql
explain analyze select time, s4 FROM d1 where id_station='st1'
AND time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '7' DAY 
AND time < TIMESTAMP '2019-04-20 00:00:00' and s4 > 0.95;
```

### group by 
```sql
explain analyze SELECT id_station, avg(s4) FROM d1 
WHERE time > TIMESTAMP '2019-04-20 00:00:00' - INTERVAL '30' DAY 
AND time < TIMESTAMP '2019-04-20 00:00:00' 
GROUP BY id_station;
```

### down 
```sql
explain analyze SELECT id_station, EXTRACT(YEAR FROM time) AS "year",
EXTRACT(MONTH FROM time) AS "month", 
EXTRACT(DAY FROM time) AS "day", 
EXTRACT(HOUR FROM time) 
AS "hour", AVG(s9) AS avg_s9
FROM d1 where  time > TIMESTAMP '2019-04-25 00:00:00' - INTERVAL '7' DAY 
AND time < TIMESTAMP '2019-04-25 00:00:00' 
GROUP BY id_station, "year", "month", "day", "hour";
```


### up 
```sql
explain analyse SELECT
  time_bucket_gapfill('5 second', time) AS NEWTIME,
  id_station,
  avg(s5) AS avg_value,
  locf(avg(s5))
FROM d1
WHERE time < '2019-03-21 00:00:00' AND time > timestamp '2019-03-21 00:00:00' - interval '15 minutes'
GROUP BY NEWTIME, id_station
ORDER BY NEWTIME;
```

# ClickHouse

```



sudo apt-get install -y apt-transport-https ca-certificates dirmngr
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754

echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee \
    /etc/apt/sources.list.d/clickhouse.list
sudo apt-get update

sudo apt-get install -y clickhouse-server clickhouse-client

sudo service clickhouse-server start
clickhouse-client --password
abdel


sudo vim /etc/clickhouse-server/config.xml 

<listen_host>0.0.0.0</listen_host>


CREATE TABLE IF NOT EXISTS d1 ( time DateTime64(9) CODEC(Gorilla), id_station String, sid String, value Float32) ENGINE = MergeTree() PARTITION BY toYYYYMMDD(time) ORDER BY (sid, id_station, time) Primary key (sid, id_station, time);



CREATE TABLE IF NOT EXISTS d1_wide ( 
        time DateTime64(9) CODEC(Gorilla), id_station String, s0 Float32 , s1 Float32 , s2 Float32 , s3 Float32 , s4 Float32 , s5 Float32 , s6 Float32 , s7 Float32 , s8 Float32 , s9 Float32 , s10 Float32 , s11 Float32 , s12 Float32 , s13 Float32 , s14 Float32 , s15 Float32 , s16 Float32 , s17 Float32 , s18 Float32 , s19 Float32 , s20 Float32 , s21 Float32 , s22 Float32 , s23 Float32 , s24 Float32 , s25 Float32 , s26 Float32 , s27 Float32 , s28 Float32 , s29 Float32 , s30 Float32 , s31 Float32 , s32 Float32 , s33 Float32 , s34 Float32 , s35 Float32 , s36 Float32 , s37 Float32 , s38 Float32 , s39 Float32 , s40 Float32 , s41 Float32 , s42 Float32 , s43 Float32 , s44 Float32 , s45 Float32 , s46 Float32 , s47 Float32 , s48 Float32 , s49 Float32 , s50 Float32 , s51 Float32 , s52 Float32 , s53 Float32 , s54 Float32 , s55 Float32 , s56 Float32 , s57 Float32 , s58 Float32 , s59 Float32 , s60 Float32 , s61 Float32 , s62 Float32 , s63 Float32 , s64 Float32 , s65 Float32 , s66 Float32 , s67 Float32 , s68 Float32 , s69 Float32 , s70 Float32 , s71 Float32 , s72 Float32 , s73 Float32 , s74 Float32 , s75 Float32 , s76 Float32 , s77 Float32 , s78 Float32 , s79 Float32 , s80 Float32 , s81 Float32 , s82 Float32 , s83 Float32 , s84 Float32 , s85 Float32 , s86 Float32 , s87 Float32 , s88 Float32 , s89 Float32 , s90 Float32 , s91 Float32 , s92 Float32 , s93 Float32 , s94 Float32 , s95 Float32 , s96 Float32 , s97 Float32 , s98 Float32 , s99 Float32
        ) ENGINE = MergeTree() PARTITION BY toYYYYMMDD(time) ORDER BY (id_station, time) Primary key (id_station, time);

time clickhouse-client --password --format_csv_delimiter="," --query="INSERT INTO d1 FORMAT CSVWithNames" < d1.csv
./pip install clickhouse-driver

 SELECT table,
    formatReadableSize(sum(bytes)) as size,
    min(min_date) as min_date,
    max(max_date) as max_date
    FROM system.parts
    WHERE active
GROUP BY table;

```

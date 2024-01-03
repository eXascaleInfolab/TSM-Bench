select ts, id_station, <sid> FROM <db> where id_station in <stid> AND  ts < '<timestamp>' AND ts >  '<timestamp>' - <range>*<rangesUnit>* 1000000L
select ts, id_station, <sid> FROM <db> where id_station in <stid> AND  ts < '<timestamp>' AND ts >  '<timestamp>' - <range>*<rangesUnit>* 1000000L and <sfilter>;
SELECT id_station, <avg_s> FROM <db> WHERE  ts < '<timestamp>' AND ts >  '<timestamp>' - <range>*<rangesUnit>* 1000000L AND id_station in <stid> GROUP BY id_station;
SELECT id_station, ts, <avg_s> FROM <db> WHERE ts < '<timestamp>' AND ts >  '<timestamp>' - <range>*<rangesUnit>* 1000000L AND id_station in <stid> SAMPLE BY 1h;
SELECT id_station, ts, <avg_s> FROM <db> WHERE  ts < '<timestamp>' AND ts >  '<timestamp>' - <range>*<rangesUnit>* 1000000L AND id_station in <stid> SAMPLE BY 5s FILL(LINEAR) GROUP BY ts, id_station ORDER BY ts;
SELECT ts, <sid1> as s_1, <sid2> as s_2, (<sid1>+ <sid2>)/2 from d1 WHERE ts > TIMESTAMP '<timestamp>' - <range>*<rangesUnit>* 1000000L AND ts < TIMESTAMP '<timestamp>' AND id_station in <stid>;
SELECT ((SUM(<sid1> * <sid2>) - (SUM(<sid1>) * SUM(<sid2>)) / COUNT())) / (SQRT(SUM(<sid1> * <sid1>) - (SUM(<sid1>) * SUM (<sid1>)) / COUNT()) * SQRT(SUM(<sid2> * <sid2>) - (SUM(<sid2>) * SUM(<sid2>)) / COUNT() )) AS pearson_corr FROM d1 WHERE  id_station=<stid> AND ts < '<timestamp>' AND ts >  '<timestamp>' - <range>*<rangesUnit>* 1000000L;

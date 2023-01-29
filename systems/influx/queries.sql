select time, id_station, <sid> FROM "d1_wide"."autogen"."sensor" where <stid> AND time > '<timestamp>Z' - <nb><rangesUnit> AND  time < '<timestamp>Z'
select time, id_station, <sid> FROM "d1_wide"."autogen"."sensor" where <stid> AND time > '<timestamp>Z' - <nb><rangesUnit> AND  time < '<timestamp>Z' and <sfilter>
SELECT <avg_s> FROM "d1_wide"."autogen"."sensor" WHERE  time > '<timestamp>Z' - <nb><rangesUnit> AND time < '<timestamp>Z' and <stid> GROUP BY "id_station"
SELECT first(id_station), <avg_s> FROM "d1_wide"."autogen"."sensor" WHERE time > '<timestamp>Z' - <nb><rangesUnit> and time < '<timestamp>Z' and <stid> GROUP BY id_station,time(1h)
SELECT id_station, <avg_s_> FROM (SELECT <avg_s_as> FROM "d1_wide"."autogen"."sensor" WHERE time > '<timestamp>Z' - <nb><rangesUnit> AND time < '<timestamp>Z' and <stid> GROUP BY id_station,time(5s) FILL(0)) GROUP BY id_station
EMPTY
EMPTY
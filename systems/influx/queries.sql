select time, id_station, <sid> FROM "<db>"."autogen"."sensor" where <stid> AND time > '<timestamp>Z' - <range><rangesUnit> AND  time < '<timestamp>Z'
select time, id_station, <sid> FROM "<db>"."autogen"."sensor" where <stid> AND time > '<timestamp>Z' - <range><rangesUnit> AND  time < '<timestamp>Z' and <sfilter>
SELECT <avg_s> FROM "<db>"."autogen"."sensor" WHERE  time > '<timestamp>Z' - <range><rangesUnit> AND time < '<timestamp>Z' and <stid> GROUP BY "id_station"
SELECT first(id_station), <avg_s> FROM "<db>"."autogen"."sensor" WHERE time > '<timestamp>Z' - <range><rangesUnit> and time < '<timestamp>Z' and <stid> GROUP BY id_station,time(1h)
SELECT id_station, <avg_s_> FROM (SELECT <avg_s_as> FROM "<db>"."autogen"."sensor" WHERE time > '<timestamp>Z' - <range><rangesUnit> AND time < '<timestamp>Z' and <stid> GROUP BY id_station,time(5s) FILL(0)) GROUP BY id_station
select <sid1>, <sid2>, (<sid1>+<sid2>)/2 FROM "<db>"."autogen"."sensor" where <stid> AND time > '<timestamp>Z' - <range><rangesUnit> AND  time < '<timestamp>Z'
EMPTY

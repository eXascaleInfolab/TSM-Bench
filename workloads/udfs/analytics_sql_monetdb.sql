-- znorm

WITH series AS (
   SELECT pH FROM datapoints WHERE id_station = 0
),
stats AS (
   SELECT
       avg(pH) as series_mean ,
       stddev_samp(pH) as series_stddev
   FROM
       series
)
SELECT
   pH,
   (pH - series_mean) / series_stddev as zscore
FROM
   series,
   stats;



-- anomaly detection
WITH series AS (
   SELECT pH FROM  datapoints WHERE id_station = 0
),
bounds AS (
   SELECT
       avg(pH) - stddev_samp(pH) AS lower_bound,
       avg(pH) + stddev_samp(pH) AS upper_bound
   FROM
       series
)
SELECT
   pH,
   pH NOT BETWEEN lower_bound AND upper_bound AS is_anomaly
FROM
   series,
   bounds;
   
-- anomaly on zscore

WITH series AS (
   SELECT pH FROM  datapoints WHERE id_station = 0
),
stats AS (
   SELECT
       avg(pH) series_avg,
       stddev_samp(pH) as series_stddev
   FROM
       series
),
zscores AS (
   SELECT
       pH,
       (pH - series_avg) / series_stddev AS zscore
   FROM
       series,
       stats
)
SELECT
   *,
   zscore NOT BETWEEN -1 AND 1 AS is_anomaly
FROM
   zscores;
   
   
-- anomaly vary threshold 

WITH series AS (
   SELECT pH FROM  datapoints WHERE id_station = 0
),
stats AS (
   SELECT
       avg(pH) series_avg,
       stddev_samp(pH) as series_stddev
   FROM
       series
),
zscores AS (
   SELECT
       pH,
       (pH - series_avg) / series_stddev AS zscore
   FROM
       series,
       stats
)
SELECT
   *,
   zscore NOT BETWEEN -0.5 AND 0.5 AS is_anomaly_0_5,
   zscore NOT BETWEEN -1 AND 1 AS is_anomaly_1,
   zscore NOT BETWEEN -3 AND 3 AS is_anomaly_3
FROM
   zscores;
   
   
--- weighted average 

SELECT
id_station,
avg(s1) as mean,
sum(
s1 *
(60 - extract(second from (timestamptz '2019-03-01 17:00' - interval '1' minute)))
) / (60 * 61 / 2) as weighted_mean
FROM
d1
WHERE
"time" > timestamptz '2019-03-01 17:00' - interval '1' minute
and "time" < timestamptz '2019-03-01 17:00'
GROUP BY
id_station;

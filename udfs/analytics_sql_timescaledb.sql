-- anomaly detection
WITH series AS (
   SELECT pH FROM  datapoints WHERE id_station = 0
),
bounds AS (
   SELECT
       avg(pH) - stddev(pH) AS lower_bound,
       avg(pH) + stddev(pH) AS upper_bound
   FROM
       series
)
SELECT
   pH,
   pH NOT BETWEEN lower_bound AND upper_bound AS is_anomaly
FROM
   series,
   bounds;



-- znorm
WITH series AS (
   SELECT pH FROM  datapoints WHERE id_station = 0
),
stats AS (
   SELECT
       avg(pH) series_mean,
       stddev(pH) as series_stddev
   FROM
       series
)
SELECT
   pH,
   (pH - series_mean) / series_stddev as zscore
FROM
   series,
   stats;



-- anomaly on zscore

WITH series AS (
   SELECT pH FROM  datapoints WHERE id_station = 0
),
stats AS (
   SELECT
       avg(pH) series_avg,
       stddev(pH) as series_stddev
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
       stddev(pH) as series_stddev
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


-- weighted mean

SELECT
   id_station,
   avg(pH) as mean,
   sum(
      pH *
      (60 - extract('seconds' from '2019-06-01 17:00 UTC'::timestamptz - interval '1 hour'))
   ) / (60 * 61 / 2) as weighted_mean
FROM
   datapoints
WHERE
   -- Last 60 periods
   time > '2019-06-01 17:00 UTC'::timestamptz
GROUP BY
   id_station;



-- forecasting

CREATE OR REPLACE FUNCTION fn_pH_projections(periods INT DEFAULT 60) RETURNS TABLE (
    timeP TIMESTAMP WITHOUT TIME ZONE, 
    pHP DOUBLE PRECISION
) LANGUAGE plpgsql AS $$
BEGIN
   CREATE TEMP TABLE IF NOT EXISTS temp_pH_projection AS
       SELECT time, pH
       FROM datapoints where id_station = 0
       ORDER BY time;
   FOR i IN 1 .. periods
       LOOP
           INSERT INTO temp_pH_projection
               SELECT (
                 SELECT MAX(a.time) + INTERVAL '10 second'
                 FROM temp_pH_projection a
              ) AS timeP,
              (
                  SELECT SUM(t.pH) 
                  FROM (
                      SELECT * 
                      FROM temp_pH_projection
                      ORDER BY time DESC 
                      LIMIT 6
                  ) t
              ) / 6 AS pHP;
       END LOOP;
    RETURN QUERY EXECUTE 'select * from temp_pH_projection';
    DROP TABLE temp_pH_projection;
END
$$;

SELECT * FROM fn_pH_projections(60);
SELECT count(*) FROM fn_pH_projections(60);
 

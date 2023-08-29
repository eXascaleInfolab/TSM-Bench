select id_station, seq_search(t,<timestamp> - <range> * <rangesUnit>,<timestamp>) as tt, <sid> FROM <db> WHERE id_station in <stid>;
select id_station, tfe, <sidlist> from ( select id_station, seq_search(t,<timestamp> - <range> * <rangesUnit>,<timestamp>) as tt, <sfilter> as fe, t@fe as tfe, <sid_filtered> FROM <db> WHERE id_station in <stid> );
SELECT id_station, ! seq_search(t,<timestamp> - <range> * <rangesUnit>,<timestamp>) as tt, <seq_avg> FROM <db> WHERE id_station in <stid>;
select id_station, ts, <sidlist> from ( select id_station, seq_search(t,<timestamp> - <range> * <rangesUnit>, <timestamp>) as tt, seq_group_agg_avg(t@tt , t@tt/3600) as ts, <seq_group_agg_avg> FROM <db> where id_station in <stid> );
select seq_aprogres_datetime(<timestamp> -  <range> * <rangesUnit>, 5, <range> * <rangesUnit>) as ts5, <seq_stretch> from <db> where id_station in <stid>;
EMPTY
select seq_search(t,<timestamp> - <range> * <rangesUnit>,<timestamp>) as tt, seq_corr(s<sid1>@tt,s<sid2>@tt) FROM <db> WHERE id_station in <stid>;

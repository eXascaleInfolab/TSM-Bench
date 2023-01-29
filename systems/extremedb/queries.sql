select id_station, seq_search(t,<timestamp> - <nb> * <rangesUnit>,<timestamp>) as tt, <sid> FROM d1_v WHERE id_station in <stid>;
select id_station, tfe, <sidlist> from ( select id_station, seq_search(t,<timestamp> - <nb> * <rangesUnit>,<timestamp>) as tt, <sfilter> as fe, t@fe as tfe, <sid_filtered> FROM d1_v WHERE id_station in <stid> );
SELECT id_station, ! seq_search(t,<timestamp> - <nb> * <rangesUnit>,<timestamp>) as tt, <seq_avg> FROM d1_v WHERE id_station in <stid>;
select id_station, ts, <sidlist> from ( select id_station, seq_search(t,<timestamp> - <nb> * <rangesUnit>, <timestamp>) as tt, seq_group_agg_avg(t@tt , t@tt/3600) as ts, <seq_group_agg_avg> FROM d1_v where id_station in <stid> );
select seq_aprogres_datetime(<timestamp> -  <nb> * <rangesUnit>, 5, <nb> * <rangesUnit>) as ts5, <seq_stretch> from d1_v where id_station in <stid>;
select seq_search(t,<timestamp> - <nb> * <rangesUnit>,<timestamp>) as tt, seq_wavg(s<sid1>@tt,s<sid2>@tt) FROM d1_v WHERE id_station = 'st<stid>';
select seq_search(t,<timestamp> - <nb> * <rangesUnit>,<timestamp>) as tt, seq_corr(s<sid1>@tt,s<sid2>@tt) FROM d1_v WHERE id_station = 'st<stid>';

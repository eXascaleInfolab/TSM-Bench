#time units
DAY = "day"
WEEK = "week"
HOUR = "hour"
MONTH = "month"
SECOND = "second"
MINUTE = "minute"
YEAR = "year"

TIME_UNITS = (DAY,WEEK,HOUR,MONTH,SECOND,MINUTE,YEAR)

time_abr_map  = {
	 DAY : "d",
	 WEEK : "w" ,
	 HOUR : "h",
	 SECOND : "s",
	 MINUTE : "m"
}

abr_time_map = { v: k for k,v in time_abr_map.items()}

time_as_seconds = {
           DAY  :  60 * 60* 24,
           WEEK   :  60 * 60* 24 * 7,
           MINUTE : 60,
           HOUR   :  60 * 60,
           SECOND : 1,
           MONTH  : 60 * 60 * 24 * 30,
           YEAR   :  60 * 60 * 24 * 30 * 12
}
def convert_weeks_to_days(rangeUnit,rangeL):
	if rangeUnit in ["week","w","WEEK" , WEEK]:
		rangeUnit = "day"
		rangeL = rangeL*7
	return rangeUnit,rangeL



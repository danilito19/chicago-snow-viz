from collections import defaultdict
import csv
from datetime import datetime
from time import mktime

# HOURS_PER_DAY = 24
# MINUTES_PER_HOUR = 60
# SECONDS_PER_MINUTE = 60
# SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY

# def seconds_since_epoch(date):
#     return mktime(date.timetuple())

# def days_in_range(date_start, date_end):
#     delta = seconds_since_epoch(date_end) - seconds_since_epoch(date_start)
#     return 1 + int(delta / SECONDS_PER_DAY)

def date_in_winter(date):
    if date >= datetime(date.year, 11, 1):
        return date.year
    elif date <= datetime(date.year, 3, 31):
        return date.year - 1
    return None

def is_winter_heatwave_day(days_weather):
    return (days_weather['TEMP_MIN_F'] > 32)

def is_subzero_day(days_weather):
    return (days_weather['TEMP_MAX_F'] <= 32)

def is_there_snow(days_weather):
    return (days_weather['SNOWDEPTH_INCHES'] > 0 or 
            days_weather['SNOWFALL_INCHES'] > 0)

def is_snow_and_subzero(days_weather):
    return (is_there_snow(days_weather) and
            is_subzero_day(days_weather))

winter_by_year = defaultdict(lambda: [])
with open('data/chicago_weather.csv', 'rb') as f:
    for row in csv.DictReader(f):
        date = datetime.strptime(row['DATE'], '%Y-%m-%d')
        if date_in_winter(date):
            winter_year = date_in_winter(date)
            winter_by_year[winter_year].append({
                'DATE': date,
                'TEMP_MAX_F': float(row['TEMP_MAX_F']),
                'TEMP_MIN_F': float(row['TEMP_MIN_F']),
                'SNOWDEPTH_INCHES': float(row['SNOWDEPTH_INCHES']),
                'SNOWFALL_INCHES': float(row['SNOW_INCHES']),
                'PRECIPITATION_INCHES': float(row['PRECIPITATION_INCHES'])
            })



for year, observations in winter_by_year.iteritems():
    observations.sort(key=lambda o: o['DATE'])
    print "Winter of {year}".format(
            year=observations[0]['DATE'].strftime('%Y')
        )
    print "Date range: {start} to {end}".format(
            start=observations[0]['DATE'].strftime('%A, %B %d, %Y'),
            end=observations[-1]['DATE'].strftime('%A, %B %d, %Y')
        )
    print ""
    # days_observed = len(observations)
    # days_total = days_in_range(observations[0]['DATE'], observations[-1]['DATE'])
    # if days_observed != days_total:
    #     print "{0} days missing!".format(
    #             days_total - days_observed
    #         )
    print '{0} heatwave days (ABOVE freezing all day).'.format(
            len(filter(is_winter_heatwave_day, observations))
        )
    print '{0} subzero days (BELOW freezing all day).'.format(
            len(filter(is_subzero_day, observations))
        )
    print '{0} days with snow on the ground.'.format(
            len(filter(is_there_snow, observations))
        )
    print '{0} subzero, snowy days.'.format(
            len(filter(is_snow_and_subzero, observations))
        )
    print ""
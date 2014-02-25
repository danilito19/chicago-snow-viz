from collections import defaultdict
import csv
from datetime import datetime
from time import mktime

HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY

def seconds_since_epoch(date):
    return mktime(date.timetuple())

def days_in_range(date_start, date_end):
    delta = seconds_since_epoch(date_end) - seconds_since_epoch(date_start)
    return 1 + int(delta / SECONDS_PER_DAY)

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



stats_per_year = defaultdict(lambda: {})
for year, observations in winter_by_year.iteritems():
    observations.sort(key=lambda o: o['DATE'])
    print "Winter of {year}".format(
            year=observations[0]['DATE'].strftime('%Y')
        )
    stats_per_year[year] = {
        'date_start': observations[0]['DATE'].strftime('%A, %B %d, %Y'),
        'date_end': observations[-1]['DATE'].strftime('%A, %B %d, %Y'),
        'days': days_in_range(observations[0]['DATE'], observations[-1]['DATE']),
        'heatwave days (ABOVE freezing all day)': 
            len(filter(is_winter_heatwave_day, observations)),
        'subzero days (BELOW freezing all day)':
            len(filter(is_subzero_day, observations)),
        'days with snow on the ground':
            len(filter(is_there_snow, observations)),
        'subzero, snowy days':
            len(filter(is_snow_and_subzero, observations))
    }
    for description, value in stats_per_year[year].items():
        print '{d}: {v}'.format(v=value, d=description)
    print ""


with open('descriptive_stats_per_year.csv', 'wb') as f:
    fieldnames = ['year'] + stats_per_year[stats_per_year.keys()[0]].keys()
    dw = csv.DictWriter(f, fieldnames=fieldnames)
    dw.writeheader()
    for year, stats in stats_per_year.iteritems():
        stats['year'] = year
        dw.writerow(stats)

import sys

from datetime import datetime, timedelta

def get_days_range(interval):
    def subtract_day(day):
        return day + timedelta(days=-1)

    days_range = []
    day_to_add = datetime.today() + timedelta(days=-1)
    while len(days_range) < interval:
        if day_to_add.weekday() == 5 or day_to_add.weekday() == 6:
            day_to_add = subtract_day(day_to_add)
        else:
            days_range.insert(0, day_to_add)
            day_to_add = subtract_day(day_to_add)

    return days_range

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

def print_now(message, timestamp = True):
    if timestamp:
        message = '{}    {}'.format(datetime.now().strftime(TIMESTAMP_FORMAT), message)
    print(message)
    sys.stdout.flush()
import sys

from datetime import datetime, timedelta

def get_days_range(interval):
    end = datetime.now() + timedelta(days=-1)
    start = end + timedelta(days=-1*interval+1)
    span = end - start
    days_range = [(start + timedelta(days=i)).date() for i in range(span.days + 1)]
    return days_range

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

def print_now(message, timestamp = True):
    if timestamp:
        message = '{}    {}'.format(datetime.now().strftime(TIMESTAMP_FORMAT), message)
    print(message)
    sys.stdout.flush()
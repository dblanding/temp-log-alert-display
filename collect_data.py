'''
This script collects temperature data from an ESP32 device N times/hour
at equal intervals, including 'on the hour'.
Time (H:M) and Temperature (deg F) are saved as comma separated values in a
separate file for each day.
All the data files for each month are contained in a folder for that month.
All monthly folders reside in a yearly folder.
All these files and folders are created automatically, "on the fly".
'''

from datetime import datetime
from pathlib import Path
import requests
import time

# Specify N = one of these integer numbers: 1,2,3,4,5,6,10,12,15,20,30,60
N = 10  # Number of readings (intervals) per hour

URL = "http://192.168.1.71"  # URL of ESP32
data_file = None
interval = 60 // N  # minutes
print('Data collected at %s minute intervals' % interval)

def secondsUntilNextReading():
    now = datetime.now()
    m = now.minute
    s = now.second

    flt_min = (s/60 + m)  # combine minutes & seconds to (float) minutes
    return (interval - (flt_min % interval)) * 60

def getTemperature(url):
    try:
        r = requests.get(url, timeout=5)
    except OSError as e:
        r = None
        print(e)
    if r:
        status_code = vars(r)['status_code']
        print('Getting data from server. Status code: %s' % status_code)
        text = r.text
        # 7th line of the text
        line = text.split('\n')[6]
        # 2nd 'word' in the line
        str_temp = line.split()[1]
    else:
        str_temp = '0'
    return str_temp

def set_data_file(now):
    global data_file
    year = now.year
    month = now.month
    day = now.day
    # Create folders, if needed
    Path('/share/year%s/month%s' % (year, month)).mkdir(parents=True, exist_ok=True)
    data_file = '/share/year%s/month%s/day%s.csv' % (year, month, day)


while True:
    wait_seconds = secondsUntilNextReading()
    print('Next reading will be in %s seconds' % int(wait_seconds))
    time.sleep(wait_seconds)
    temp = getTemperature(URL)
    now = datetime.now()
    set_data_file(now)
    curr_time = now.strftime("%R")
    with open(data_file, 'a') as f:
        f.write(curr_time + ', ' + temp + '\n')
    

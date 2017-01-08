import pytz, os
import datetime
import sys
from bs4 import BeautifulSoup
import requests
import time
import json

CWD             = os.path.dirname(os.path.realpath(__file__))
TZNAMES_PATH    = os.path.join(CWD, 'tznames.json')
FTTB_CACHE_PATH = os.path.join(CWD, 'fttb.cache')

def fetch_tznames():
    tznames = {}

    if os.path.exists(TZNAMES_PATH):
        with open(TZNAMES_PATH) as f:
            tznames = json.loads(f.read())
    else:
        if os.path.exists(FTTB_CACHE_PATH):
            with open(FTTB_CACHE_PATH) as f:
                content = f.read()
        else:
            content = requests.get('https://time.is/time_zones').content
            with open(FTTB_CACHE_PATH, 'w') as f:
                f.write(content)

        soup = BeautifulSoup(content, 'lxml')
        for div in soup.find_all('div', 'section'):
            tzname = div.find('h1').text
            tznames[tzname] = []
            for a in div.find_all('a'):
                tznames[tzname].append(a.text)

        with open(TZNAMES_PATH, 'w') as f:
            f.write(json.dumps(tznames))

    return tznames

if __name__ == "__main__":
  print(fetch_tznames().keys())

# http://www.citytimezones.info/pending_requests.htm
# https://time.is/time_zones
# http://www.worldtimezone.com/time/wtzstandard.php?sorttb=City&listsw=&forma=12h

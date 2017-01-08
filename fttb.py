import pytz, os
import datetime
import sys
import random

import twitter
import time
import json

LOCAL_TIMEZONE  = 'US/Eastern'
CWD             = os.path.dirname(os.path.realpath(__file__))
TZNAMES_PATH    = os.path.join(CWD, 'tznames.json')

def fetch_tznames():
  # tznames format: { "UTC-1" : [ "place0", "place1"], "UTC+1" : [ "place2", "place3"] }
  #
    with open(TZNAMES_PATH) as f:
        return json.loads(f.read())

def magic_places():
    local_tz    = pytz.timezone(LOCAL_TIMEZONE)
    now         = local_tz.localize(datetime.datetime.today())
    magic_zones = set()

    for tzname in pytz.all_timezones:
        tz  = pytz.timezone(tzname)
        tzt = now.astimezone(tz)

        if (tzt.hour == 4 or tzt.hour == 16) and tzt.minute == 20:
            tzs = tzt.strftime("%z")
            key = 'UTC' + (tzs[:3] + ':' + tzs[3:]).replace(':00', '').replace('+0', '+').replace('-0', '-')
            magic_zones.add(key)

    return [ random.choice(fetch_tznames()[zone]).encode('utf-8') for zone in magic_zones ]

def do_twitter():
    consumer_key        = 'Q8p6JnkK66HVUval9cj1G6cve'
    with open('/opt/tcs.key') as f:
        consumer_secret = f.read().strip()
    access_token_key    = '816892296679436288-ek56lZJY0LHb8HyZKJsB9LdkrfXLXm1'
    with open('/opt/ats.key') as f:
        access_token_secret = f.read().strip()

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    suffixes = (
      '',
      '.',
      '!',
      '. Blast a roach!',
      '. Boot the gong.',
      '. Burn one for Willie!',
      '. Fire it up, bud!',
      '. Time to mow the grass.',
      '. Toke up, Samwise.',
      ', buds.',
      '. Spark it up!',
      ', so chief some leaf!',
      ', time for some Pink Floyd.',
      '. Get wrecked.',
      '. Toke up!',
      '. Reefer madness!',
      '. Time to pack a bowl.',
      '. The kindest hour.',
      '. Dank.',
      '. Burn one in solidarity.',
      '. Get Bouldered!',
      '! Toke a beeze.',
      '. Spark the Dutch.',
      '. Get Blazin, yo.',
      '. Get baked.',
      '. Scuse me while I kiss the sky.',
    )

    for place in magic_places():
        suffix = random.choice(suffixes)
        if place.isalpha():
            place = "#{}".format(place.replace(' ', ''))
        api.PostUpdate("It's 4:20 in {}{}".format(place, suffix))

if __name__ == "__main__":
    do_twitter()

# http://www.citytimezones.info/pending_requests.htm
# https://time.is/time_zones
# http://www.worldtimezone.com/time/wtzstandard.php?sorttb=City&listsw=&forma=12h

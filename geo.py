import pytz, os
import datetime
import sys
import random

import twitter
import time
import json
import pprint

CWD             = os.path.dirname(os.path.realpath(__file__))
TCS_KEY_PATH    = os.path.join(CWD, 'tcs.key')
ATS_KEY_PATH    = os.path.join(CWD, 'ats.key')

PLACE_CACHE     = os.path.join(CWD, 'place.cache')

def do_twitter():
    consumer_key        = 'Q8p6JnkK66HVUval9cj1G6cve'
    with open(TCS_KEY_PATH) as f:
        consumer_secret = f.read().strip()
    access_token_key    = '816892296679436288-ek56lZJY0LHb8HyZKJsB9LdkrfXLXm1'
    with open(ATS_KEY_PATH) as f:
        access_token_secret = f.read().strip()

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    # NYC: 40.7128 N, 74.0059 W
    lat = 40.7128
    lon = 74.0059


    if os.path.exists(PLACE_CACHE):
        with open(PLACE_CACHE, 'rb') as f:
            places = json.loads(f.read())
    else:
        parameters = dict(lat=lat, long=lon)
        url = '%s/geo/reverse_geocode.json' % (api.base_url)

        resp = api._RequestUrl(url, 'GET', data=parameters)
        data = api._ParseAndCheckTwitter(resp.content.decode('utf-8'))

        key  = "{}:{}".format(lat, lon)
        places = { key : data['result'] }

        with open(PLACE_CACHE, 'wb') as f:
            f.write(json.dumps(places))

    key = places.keys()[0]
    place = places[key]['places'][0]
    print(place['name'], place['id'])

    api.PostUpdate("Hello from very far away from Manhattan".format(place['name']),
                   latitude=lat,
                   longitude=lon
                   )


if __name__ == "__main__":
    do_twitter()

# http://www.citytimezones.info/pending_requests.htm
# https://time.is/time_zones
# http://www.worldtimezone.com/time/wtzstandard.php?sorttb=City&listsw=&forma=12h

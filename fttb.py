import pytz, os
import datetime
import sys
import random

import pprint

import shapefile
import shapely.geometry

import twitter
import time
import json

LOCAL_TIMEZONE  = 'US/Eastern'
CWD             = os.path.dirname(os.path.realpath(__file__))
TCS_KEY_PATH    = os.path.join(CWD, 'tcs.key')
ATS_KEY_PATH    = os.path.join(CWD, 'ats.key')
SUFFIXES_PATH   = os.path.join(CWD, 'suffixes')
SHAPEFILE_PATH  = os.path.join(CWD, 'world', 'tz_world.shp')

class Tweeter(object):
    def __init__(self):
        consumer_key        = 'Q8p6JnkK66HVUval9cj1G6cve'
        with open(TCS_KEY_PATH) as f:
            consumer_secret = f.read().strip()
        access_token_key    = '816892296679436288-ek56lZJY0LHb8HyZKJsB9LdkrfXLXm1'
        with open(ATS_KEY_PATH) as f:
            access_token_secret = f.read().strip()

        self.api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        with open(SUFFIXES_PATH) as f:
            self.suffixes = map(str.strip, f.read().strip().split("\n"))

    def tweet_for(self, point):
        lat, lon = point.y, point.x
        parameters = dict(lat=lat, long=lon)

        # either one seems to work with this code : maybe try one if the other is rate limited?
        #
        url = '%s/geo/reverse_geocode.json' % (self.api.base_url)
        # url = '%s/geo/search.json' % (self.api.base_url)

        try:
            resp = self.api._RequestUrl(url, 'GET', data=parameters)
            data = self.api._ParseAndCheckTwitter(resp.content.decode('utf-8'))

            place = random.choice(data['result']['places'])
            name, country = place['name'].encode('utf-8'), place['country'].encode('utf-8')
        except Exception as e:
            print(e)
            pass
        else:
            if name.isalpha():
                name = "#{}".format(name)
            if country.isalpha():
                country = "#{}".format(country)

            suffix = random.choice(self.suffixes)

            if name == country:
                post = "It's 4:20 in {}{}".format(name, suffix)
            else:
                post = "It's 4:20 in {}, {}{}".format(name, country, suffix)

            self.api.PostUpdate(post, latitude=lat, longitude=lon)
            print(post)

def random_point_in(poly):
     (minx, miny, maxx, maxy) = poly.bounds
     while True:
         p = shapely.geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
         if poly.contains(p):
             return p

def find_magic_zones():
    local_tz    = pytz.timezone(LOCAL_TIMEZONE)
    now         = local_tz.localize(datetime.datetime.today())

    magic_zones = dict()

    for tzname in pytz.all_timezones:
        tz  = pytz.timezone(tzname)
        tzt = now.astimezone(tz)

        if (tzt.hour == 4 or tzt.hour == 16) and tzt.minute == 20:
            if not tzname.startswith('Etc/'):
                key = tzname.split('/')[0]
                magic_zones.setdefault(key, set()).add(tzname)

    return [ random.choice(list(v)) for v in magic_zones.values() ]

def find_magic_points():
    magic_points = []

    magic_zones = find_magic_zones()
    if magic_zones:
        shapes = {}

        for sr in shapefile.Reader(SHAPEFILE_PATH).iterShapeRecords():
            shapes.setdefault(sr.record[0], []).append(sr.shape)

        for zone in magic_zones:
            print(zone)
            if zone in shapes:
                shape = random.choice(shapes[zone])
                poly = shapely.geometry.shape(shape)
                magic_points.append(random_point_in(poly))

    return magic_points

if __name__ == "__main__":
    magic_points = find_magic_points()
    if magic_points:
        t = Tweeter()
        for point in magic_points:
            print(point)
            t.tweet_for(point)

# http://www.citytimezones.info/pending_requests.htm
# https://time.is/time_zones
# http://www.worldtimezone.com/time/wtzstandard.php?sorttb=City&listsw=&forma=12h

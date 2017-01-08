import shapefile
import pytz
import random
import shapely.geometry

def random_point_in(poly):
     (minx, miny, maxx, maxy) = poly.bounds
     while True:
         p = shapely.geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
         if poly.contains(p):
             return p


sf = shapefile.Reader("world/tz_world.shp")

zones  = set(pytz.all_timezones)
shapes = {}

for sr in sf.iterShapeRecords():
    shapes.setdefault(sr.record[0], []).append(sr.shape)

for zone in sorted(zones):
    # if not zone == 'America/Los_Angeles':
    #     continue
    if zone in shapes:
        shape = random.choice(shapes[zone])
        poly = shapely.geometry.shape(shape)
        # point = shape.representative_point()

        point = random_point_in(poly)

        print("{} : {}/{}".format(zone, point.y, point.x))

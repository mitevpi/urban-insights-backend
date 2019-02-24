import math
from flask import Flask
from flask import request
from flask.json import jsonify
import json
import os

app = Flask(__name__)

resource_path = os.path.join(app.root_path, 'models')

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/func01")
def func01():
    return "Response for func01"


@app.route("/func02")
def func02():
    flines = []
    filepath = r"models/sf.obj"
    #outputfile = r"sfParsed.obj"
    with open(filepath) as f:
        for fline in f:
            flines.append(fline.replace("\\", ""))
    return jsonify({'test': flines})
    #return flines


@app.route("/cutObj")
def cutObj():
    filepath = r"models/sf.obj"
    outputfile = r"sfParsed.obj"

    # Coordinates for focus points (rhino coordinates)
    cx = -1200.0
    cy = -18200.0
    radius = 1500.0

    flipXY = True
    moveToOrigin = True

    # output lists
    o_vertices = []
    o_faces = []
    o_verticenormals = []

    # working lists
    flines = []
    vertices = []
    verticenormals = []

    # 2d distance

    def dist(cx, cy, dx, dy):
        dx = abs(cx-dx)
        dy = abs(cy-dy)
        return math.sqrt(dx * dx + dy * dy)

    # readfile
    with open(filepath) as f:
        for fline in f:
            flines.append(fline.replace("\\", ""))

    # Main:

    # find out if split for g or o!!!
    # as test, using only objects 0-10
    objects = "".join(flines).split("g ")[1:]
    if len(objects) < 2:
        # as test, using only objects 0-10
        objects = "".join(flines).split("o ")[1:]

    # print("Parsing through {} obj objects".format(len(objects)))

    for objectnr, object in enumerate(objects):
        # # print("object {}".format(str(objectnr)))

        for linenr, line in enumerate(object.split("\n")):
            if line[0:2] == "v ":
                x, y, z = line[2:].split(" ")
                x, y, z = float(x), float(y), float(z)
                vertices.append([x, y, z])

            elif line[0:2] == "f ":
                # # print " - facenr %s" % linenr
                facevertices = line.split(" ")[1:]

                # facelist = " ,".join(facevertices)
                penalty = []
                temppoints = []
                tempvertices = []
                fv = []

                for facevertice in facevertices:
                    fv.append(int(facevertice.split("//")[0].split("/")[0])-1)

                for vn in fv:
                    vx, vy, vz = vertices[vn][0], vertices[vn][1], vertices[vn][2]

                    distance = dist(cx, cy, vx, vy)
                    if distance > radius:
                        penalty.append(True)
                    if(flipXY):
                        if(moveToOrigin):
                            tempvertices.append([vx-cx, vz, vy-cy])
                        else:
                            tempvertices.append([vx, vz, vy])
                    else:
                        if(moveToOrigin):
                            tempvertices.append([vx-cx, vy-cy, vz])
                        else:
                            tempvertices.append([vx, vy, vz])
                    temppoints.append(len(o_vertices)+len(temppoints)+1)
                if len(penalty) == 0:
                    # # print "Added to o_faces: ", temppoints
                    o_faces.append(temppoints)

                    for x in tempvertices:
                        o_vertices.append(x)
                        # # print "Added to o_vertices [%s -> %s]: %s" % (vn, len(o_vertices), x)

    nf = open(outputfile, "w")
    nf.write("""# Rhino

    o object_1""")

    for coords in o_vertices:
        x, y, z = coords
        nf.write("\nv {} {} {}".format(x, y, z))
    for faces in o_faces:
        facestring = "\nf "
        for vertice in list(reversed(faces)):
            facestring = facestring + str(vertice) + "//" + str(vertice) + " "
        nf.write(facestring)
    nf.close()

    # return json
    flines = []
    filepath = r"models/sf.obj"
    with open(filepath) as f:
        for fline in f:
            flines.append(fline.replace("\\", ""))
    return jsonify({'parsedModel': flines})

@app.route("/getSunVector")
def getSunVector():
    # UIAdresse = "ib schonbergs alle 2 valby"
    # UImonth = 6
    # UIday = 21
    # UIhour = 12

    temp = json.loads(request.data)
    print(temp['month'])

    UIAdresse = temp['address']
    UImonth = temp['month']
    UIday = temp['day']
    UIhour = temp['hour']


    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="UrbanInsight")
    location = geolocator.geocode(UIAdresse)
    # print(location.address)

    # print((location.latitude, location.longitude))

    from timezonefinder import TimezoneFinder

    tf = TimezoneFinder()

    from pytz import timezone
    import pytz
    from datetime import datetime

    utc = pytz.utc

    def offset(target):
        today = datetime.now()
        tz_target = timezone(tf.certain_timezone_at(lat=target['lat'], lng=target['lng']))
        # ATTENTION: tz_target could be None! handle error case
        today_target = tz_target.localize(datetime(2016, UImonth, UIday))
        today_utc = utc.localize(datetime(2016, UImonth, UIday))
        return (today_utc - today_target).total_seconds() / 60


    # Create location. You can also extract location data from an epw file.
    lati = location.latitude
    long = location.longitude

    timez = dict({'lat':lati, 'lng':long})
    tz =(offset(timez) / 60)
    # print(tz)

    from ladybug.sunpath import Sunpath
    from ladybug.location import Location

    city = Location('City', 'Country', latitude=lati, longitude=long, time_zone=tz)

    # Initiate sunpath
    sp = Sunpath.from_location(city)
    sun = sp.calculate_sun(month=UImonth, day=UIday, hour=UIhour)

    # print('altitude: {}, azimuth: {}'.format(sun.altitude, sun.azimuth))

    from ladybug.dt import DateTime

    _year_ = 2016
    _minute_ = 0

    mydate = DateTime(UImonth, UIday, UIhour)

    from ladybug.sunpath import Sun
    import math

    altitude = sun.altitude_in_radians
    azimuth = sun.azimuth_in_radians
    is_solar_time = "false"
    is_daylight_saving = "false"
    north_angle = 0
    sn = Sun(DateTime, altitude, azimuth, is_solar_time, is_daylight_saving, north_angle, data=None)
    # print(sun.sun_vector)
    vector = str(sun.sun_vector)
    returnRequest = str(request.data)
    
    #temp = json.loads(request.data)
    #print(temp['name'])
    return jsonify({'sunVector': vector, 'request': returnRequest})



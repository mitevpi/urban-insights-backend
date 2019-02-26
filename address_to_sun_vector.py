import math
import json
import os


def getSunVector(input_address, input_month, input_day, input_hour):

    # temp = json.loads(request.data)
    # print(temp['month'])

    # input_address = temp['address']
    # input_month = temp['month']
    # input_day = temp['day']
    # input_hour = temp['hour']


    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="UrbanInsight")
    location = geolocator.geocode(input_address)

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
        today_target = tz_target.localize(datetime(2016, input_month, input_day))
        today_utc = utc.localize(datetime(2016, input_month, input_day))
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
    sun = sp.calculate_sun(month=input_month, day=input_day, hour=input_hour)

    # print('altitude: {}, azimuth: {}'.format(sun.altitude, sun.azimuth))

    from ladybug.dt import DateTime

    _year_ = 2016
    _minute_ = 0

    mydate = DateTime(input_month, input_day, input_hour)

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

    return vector
    #return jsonify({'sunVector': vector, 'request': returnRequest})
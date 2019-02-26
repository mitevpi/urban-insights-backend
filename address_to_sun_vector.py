import math
import json
import os

from pytz import timezone
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime
from timezonefinder import TimezoneFinder

from ladybug.sunpath import Sunpath
from ladybug.location import Location
from ladybug.sunpath import Sun
from ladybug.dt import DateTime


def getSunVector(input_address, input_month, input_day, input_hour):
    geolocator = Nominatim(user_agent="UrbanInsight")
    location = geolocator.geocode(input_address)

    tf = TimezoneFinder()
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


    city = Location('City', 'Country', latitude=lati, longitude=long, time_zone=tz)

    # Initiate sunpath
    sp = Sunpath.from_location(city)
    sun = sp.calculate_sun(month=input_month, day=input_day, hour=input_hour)

    # print('altitude: {}, azimuth: {}'.format(sun.altitude, sun.azimuth))

    _year_ = 2016
    _minute_ = 0

    mydate = DateTime(input_month, input_day, input_hour)

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
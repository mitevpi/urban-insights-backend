#!/usr/bin/env python
# coding: utf-8

# In[99]:


#Input

UIAdresse = "ib schonbergs alle 2 valby"
UImonth = 6
UIday = 21
UIhour = 12


# In[100]:


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="UrbanInsight")
location = geolocator.geocode(UIAdresse)
print(location.address)

print((location.latitude, location.longitude))


# In[101]:


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
print(tz)


# In[102]:


from ladybug.sunpath import Sunpath
from ladybug.location import Location

city = Location('City', 'Country', latitude=lati, longitude=long, time_zone=tz)

# Initiate sunpath
sp = Sunpath.from_location(city)
sun = sp.calculate_sun(month=UImonth, day=UIday, hour=UIhour)

print('altitude: {}, azimuth: {}'.format(sun.altitude, sun.azimuth))


# In[103]:


from ladybug.dt import DateTime

_year_ = 2016
_minute_ = 0


mydate = DateTime(UImonth, UIday, UIhour)


# In[97]:


from ladybug.sunpath import Sun
import math

altitude = sun.altitude_in_radians
azimuth = sun.azimuth_in_radians
is_solar_time = "false"
is_daylight_saving = "false"
north_angle = 0
sn = Sun(DateTime, altitude, azimuth, is_solar_time, is_daylight_saving, north_angle, data=None)
print(sun.sun_vector)


# 

# In[ ]:





# In[ ]:





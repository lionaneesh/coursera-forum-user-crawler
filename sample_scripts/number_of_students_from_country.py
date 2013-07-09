#!/bin/python2.7
import sys
import os
import inspect

p =  os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(p)

import json
import urllib2
from ProgressBar.progress_bar import ProgressBar

data_file = "../Startup-Class-Data/user_objects.json"
country_data_file = "../Startup-Class-Data/country_stats.json"
data = {}
countries = {}
number_of_users = 0
user_counter = 0

with open(data_file) as fp:
    data = json.loads(fp.read())

number_of_users = len(data)
print "Total users ", len(data)

p = ProgressBar(number_of_users)

for user in data:
    lat = user['location_lat'] 
    lon = user['location_lng']

    if not lat or not lon:
        continue
    # begin reverse geocode
    rev_geocode_link = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&sensor=false&callback=callbackForMapsApi"

    try:
        res = urllib2.urlopen(rev_geocode_link)
        data = json.loads(res.read())
    except urllib2.HTTPError,e:
        print "Failed to reverse geocode ", user["id"], "'s location. Reason: ", e.reason 

    # now let's figure out the country
    for address in data["results"][0]["address_components"]:
        if "country" in address["types"]:
            country = address["long_name"]         
            try:
                countries[country] += 1
            except:
                countries[country]  = 1
            break
    user_counter += 1
    p.update_time(user_counter)
    print p, chr(27) + '[A'

import csv
import os
import pandas as pd
import json
from collections import OrderedDict

cities_file = open("cities.csv", "r")
cities = csv.reader(cities_file, delimiter=',')
data=None
if(os.path.exists("mean_power.json")):
    mean_power_file=open("mean_power.json", "r")
    data=json.load(mean_power_file)
    for row in cities:
        for element in data:
            if(element["wsid"] == row[0]):
                element["latitude"]=float(row[3])
                element["longitude"]=float(row[4])
    mean_power_file.close()

#print(data)
#print(len(data))
sort_order = ['wsid', 'latitude', 'longitude', 'E-115/3000', 'E-126/4200']
ordered = [OrderedDict(sorted(d.iteritems(), key= lambda (k, v): sort_order.index(k)))
                    for d in data]
#print(data)


if(not data is None):
    mean=data
mean_power_file=open("mean_power.json", "w")
json.dump(ordered, mean_power_file, indent=4)

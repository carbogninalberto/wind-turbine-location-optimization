from src.fitness import distance
from src.fitness import generate_power_plants
from math import sin, cos, sqrt, atan2, radians
import unittest
import json
import random

"""
To run the test from the project folder run:
python3 -m unittest tests/calculate_distance.py
"""

class TestDistance(unittest.TestCase):
    def test(self):
        cities_file= open("dataParsingScripts/mean_power.json", "r")
        data=json.load(cities_file)
        maxd = 0
        for element in data:
            for element2 in data:
                temp = distance(element["latitude"],element["longitude"], element2["latitude"], element2["longitude"])
                if(temp>maxd):
                    maxd=temp
        print(maxd)
        lat1 = radians(52.2296756)
        lon1 = radians(21.0122287)
        lat2 = radians(52.406374)
        lon2 = radians(16.9251681)
        result = int(distance(lat1, lon1, lat2, lon2))
        print(result)
        for i in range(10):
            print(generate_power_plants(random.Random(i),1))

        lat=0
        lon=0
        i=0
        for element in data:
            lat+=element["latitude"]
            lon+=element["longitude"]
            i+=1
        lat/=i
        lon/=i
        print(str(lat)+" "+str(lon) )


        cities_file.close()
        self.assertEqual(result, 278)


if __name__ == '__main__':
    unittest.main()

from src.fitness import PowerPlant
import src.fitness
import unittest
import json

"""
To run the test from the project folder execute:
python3 -m unittest tests/power_plant_positioning.py
"""
class TestCost(unittest.TestCase):
    def test(self):
        cities_file= open("dataParsingScripts/mean_power.json", "r")
        data=json.load(cities_file)
        maxd = 0
        a=[]
        counter=0
        for element in data:
                a.append([1 if counter<1 else 0, 0, 0])
                counter+=1
        cities=[]
        for element in data:
                cities.append([element["latitude"],element["longitude"]])

        a=list(map(list, zip(*a)))

        n_power_plant = 4
        b=PowerPlant(a, cities, n_power_plant)
        c=b.run()
        for i in range(n_power_plant):
            print(c.candidate[0+i*2],",",c.candidate[1+i*2])

        result=0

        cities_file.close()
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()

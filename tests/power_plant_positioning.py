from src.fitness import calculate_distance_cost
import src.fitness
import unittest

"""
To run the test from the project folder execute:
python3 -m unittest tests/power_plant_positioning.py
"""

class TestCost(unittest.TestCase):
    def test(self):
        a=[[0,1,0],[0,2,4]]
        b=calculate_distance_cost(a)
        print(b)
        self.assertEqual(result, 278)


if __name__ == '__main__':
    unittest.main()

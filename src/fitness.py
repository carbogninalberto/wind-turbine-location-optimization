'''
src/fitness.py

this file contains the fitness functions of the multi-objectives problem
'''
# IMPORT LIBS
import numpy as np
import json
from math import sin, cos, sqrt, atan2, radians
from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
from inspyred.ec import terminators


# FUNCTIONS

#################### OBJECTIVE 1: F(S) ####################
'''
Fitness function for turbine placing:
F(S) = sum_turbines sum_cities S_t,n f(t,n) z(n)
'''
def wind_turbine_power_fitness(matrix, matrix_power):
    matrix_t = matrix.transpose()
    matrix_power_t = matrix_power.transpose()
    result = np.array([0.0001], dtype=np.float32)
    row_index = 0
    for city in matrix_t:
        result = np.append(result, [np.sum(city*matrix_power_t[row_index,:]*degradation_coefficient(matrix, row_index), dtype=np.float32)])
        row_index += 1
    return np.sum(result, dtype=np.float32)#**(-1)

'''
coefficient of degradation for placing more than one turbine z(x)
'''
def degradation_coefficient(matrix, city):
    return 1.2**-(np.sum(matrix[:,city], dtype=np.float32)-1)

'''
load pre-calculated matrix_power to speedup calculation
- filename: name of json file
- wind_turbines: array of turbines listed in the json
'''
def load_matrix_power(filename, wind_turbines):
    matrix = np.array([[]], dtype=np.float32)
    # load json
    try:
        mean_power_file=open(filename, "r")
        data=json.load(mean_power_file)
        matrix = np.zeros((len(data), len(wind_turbines)), dtype=np.float32)
        matrix_cities = np.zeros((len(data), 2), dtype=np.float32)
        n = 0
        t = 0
        for element in data:
            matrix_cities[n][0] = element["latitude"]
            matrix_cities[n][1] = element["longitude"]
            for turbine in wind_turbines:
                matrix[n][t] = element[turbine]
                t += 1
            t = 0
            n += 1
    except IOError:
        print("Error on reading JSON file, check that file exists!")
    except:
        print("Something goes wrong in file manipulation.")
    finally:
        mean_power_file.close()

    return matrix.transpose(), matrix_cities

###########################################################


#################### OBJECTIVE 2: T_c(S) ####################
'''
Fitness function for turbine cost:
Given a matrix S, calculate the aggregate cost of this layout
and return the tuple:
(cost, list of cities with turbines)
'''
def wind_turbine_cost_fitness(matrix, turbines_cost):
    matrix_t = matrix.transpose()
    cities_with_turbines = np.array([], dtype=np.int32)
    fitness = np.array([])
    city_index = 0
    
    for city in matrix_t:
        for i in range(len(city)):
            if city[i] > 0:
                cities_with_turbines = np.append(cities_with_turbines, city_index)
            fitness = np.append(fitness, city[i]*turbines_cost[i])
        city_index += 1

    return (np.sum(fitness, dtype=np.float32), cities_with_turbines)

###########################################################

#################### OBJECTIVE 3: PP(S) ####################

class PowerPlant():

    def __init__(self, turbines_matrix, cities, number):
        self.turbines_matrix = turbines_matrix
        self.cities = cities
        self.contains_turbines = [False] * len(turbines_matrix[0])
        self.n_power_plants = number


    def distance(self, lat1, lon1, lat2, lon2):
        """
        calculates the distance between two coordinates
        """
        R = 6371.0
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def distancec(self, p1, p2):
        """
        calculates the distance between two coordinates
        """
        return self.distance(p1[0], p1[1], p2[0], p2[1])

    def generate_power_plants(self, random, *args):
        base_lat = -20.41
        base_lon = -44.95
        k=2
        return [base_lat + random.uniform(-k,k), base_lon + random.uniform(-k,k)] * self.n_power_plants


    def evaluate_power_plants(self, candidates, *args):
        turbine_cables_weight = 3.4
        fitness = []
        for cs in candidates:
            d=0
            for i in range(len(self.cities)):
                k = 1
                if(self.contains_turbines[i]):
                    k = turbine_cables_weight

                min = 999999999
                dist = 999999999
                for j in range(self.n_power_plants):

                    t = [cs[0+j*2], cs[1+j*2]]
                    dist = self.distancec(self.cities[i], t) * k
                    if (dist<min):
                        min=dist
                d+=min
            fitness.append(d)
        return fitness


    def run(self):
        for i in range(len(self.turbines_matrix)):
            for j in range(len(self.turbines_matrix[i])):
                found = self.turbines_matrix[i][j] > 0
                self.contains_turbines[j] = (self.contains_turbines[j] or found)

        rand = Random()
        rand.seed(int(time()))
        es = ec.ES(rand)

        es.terminator = terminators.evaluation_termination
        final_pop = es.evolve(generator=self.generate_power_plants,
                              evaluator=self.evaluate_power_plants,
                              pop_size=20,
                              maximize=False,
                              max_evaluations=100)

        # Sort and print the best individual, who will be at index 0.
        final_pop.sort(reverse=True)
        return final_pop[0]

###########################################################

#TESTS

if __name__ == "__main__":
    print("\n[RUNNING TESTING FUNCTIONS]")

    #testing wind_turbine_power_fitness
    print("\n\n<EXECUTE OUTPUT> \t\t\twind_turbine_power_fitness()")
    print("-----------------------------------------------------------------------")
    test_matrix = np.array([[0,3,1],[0,2,0],[1,5,1]])
    test_matrix_power = np.array([[0,0,0],[5,10,20],[5,10,20]])

    print("fitness: ")
    print(wind_turbine_power_fitness(test_matrix, test_matrix_power))

    #testing degradation_coefficient
    print("\n\n<EXECUTE OUTPUT> \t\t\tdegradation_coefficient()")
    print("-----------------------------------------------------------------------")
    print("col. n. 0")
    print(degradation_coefficient(test_matrix,0))

    #testing load_matrix_power
    print("\n\n<EXECUTE OUTPUT> \t\t\tload_matrix_power()")
    print("-----------------------------------------------------------------------")
    print("generated matrix:")
    loaded_matrix = load_matrix_power("../dataParsingScripts/mean_power.json", ["E-115/3000"])
    print(loaded_matrix, "shape: ", loaded_matrix.shape)

    #testing wind_turbine_cost_fitness
    print("\n\n<EXECUTE OUTPUT> \t\t\wind_turbine_cost_fitness()")
    print("-----------------------------------------------------------------------")
    print("random matrix:")
    print(loaded_matrix.shape)
    random_matrix = np.random.randint(2, size=loaded_matrix.shape)
    print(random_matrix)

    print("\ncost tuple:")
    cost_tuple = wind_turbine_cost_fitness(random_matrix, [1.25])

    print(str(float(cost_tuple[0]*10**6)) + "$")

    print("\n[END TESTS]\n")

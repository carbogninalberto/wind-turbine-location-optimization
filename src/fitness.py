'''
src/fitness.py

this file contains the fitness functions of the multi-objectives problem
'''
# IMPORT LIBS
import numpy as np

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
    return np.sum(result, dtype=np.float32)**(-1)

'''
coefficient of degradation for placing more than one turbine z(x)
'''
def degradation_coefficient(matrix, city):
    return 1.2**-(np.sum(matrix[:,city], dtype=np.float32)-1)

'''
load pre-calculated matrix_power to speedup calculation
'''
def load_matrix_power(filename):
    matrix = np.array([[]], dtype=float32)
    # load csv
    # create matrix_power
    # close csv
    return matrix

###########################################################

#################### OBJECTIVE 2: PP(S) ####################



###########################################################

#TESTS

if __name__ == "__main__":
    print("\n[RUNNING TESTING FUNCTIONS]\n")
    
    #testing wind_turbine_power_fitness
    print("<EXECUTE OUTPUT> \twind_turbine_power_fitness()\n")
    test_matrix = np.array([[0,3,1],[0,2,0],[1,5,1]])
    test_matrix_power = np.array([[0,0,0],[5,10,20],[5,10,20]])
    
    print("fitness: ")
    print(wind_turbine_power_fitness(test_matrix, test_matrix_power))
    print()

    #testing degradation_coefficient
    print("<EXECUTE OUTPUT> \tdegradation_coefficient()\n")
    print("col. n. 0")
    print(degradation_coefficient(test_matrix,0))

    print("\n[END TESTS]\n")

'''
src/fitness.py

this file contains the fitness functions of the multi-objectives problem
'''
# IMPORT LIBS
import numpy as np
import json

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
        n = 0
        t = 0
        for element in data:
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


    # create matrix_power
    # close csv
    return matrix.transpose()

###########################################################

#################### OBJECTIVE 2: PP(S) ####################



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
    print(loaded_matrix)

    print("\n[END TESTS]\n")

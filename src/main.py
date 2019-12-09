'''
src/main.py

this is the main file where tune params to find better solutions
'''

from pylab import *

from inspyred import benchmarks
from inspyred.ec import variators
from inspyred_utils import NumpyRandomWrapper
from wind_turbines_location import WindTurbines, wind_turbines_mutation, wind_turbines_blend_crossover

import multi_objective
import utils
import time

import sys, os

""" 
-------------------------------------------------------------------------
SETTINGS
"""

display = False

# parameters for NSGA-2
args = {}
args["pop_size"] = 5
args["max_generations"] = 10
c_budget = 1200 # in milion dollars

wind_turbines=["E-115/3000", "E-126/4200", "V164/9500", "V117/3600", "V90/2000", "S152/6330", "S126/6150", "N100/2500"]
wind_turbines_costs=[6.91, 10.6, 33.25, 8.69, 4.24, 18.46, 17.73, 5.53]

"""
-------------------------------------------------------------------------
"""

problem = WindTurbines(n_turbines=len(wind_turbines), budget=c_budget, wind_turbines=wind_turbines, wind_turbines_costs=wind_turbines_costs, n_powerplants=3)
args["objective_1"] = "Produced Power (Kw/h)"
args["objective_2"] = "Cost ($)"

args["variator"] = [wind_turbines_blend_crossover, wind_turbines_mutation]

args["fig_title"] = 'NSGA-2'

if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
    
    final_pop, final_pop_fitnesses, best_guy = multi_objective.run_nsga2(rng, problem, display=display, 
                                         num_vars=2, **args)
    

    utils.vector_to_matrix(best_guy, len(wind_turbines), 110)

    #print ("Final Population\n", final_pop)
    print ("Final Population Fitnesses\n", final_pop_fitnesses)

    ioff()
    #show()
    os.mkdir('../output/')
    timestamp = str(int(round(time.time() * 1000)))
    folder = '../output/'+timestamp
    os.mkdir(folder)

    paretofront = folder + "/" + timestamp + "_pareto.png"

    output = open(folder+"/_pareto_front.csv", "w")
    for individual, fitness in zip(final_pop, final_pop_fitnesses) :
        #print(individual)
        individual_row = np.array2string(individual, formatter={'float_kind':lambda x: "%.2f" % individual})
        output.write(individual_row)
        output.write(",")
        fitness_row = str(fitness) #np.array2string(fitness, formatter={'float_kind':lambda x: "%.2f" % fitness})
        output.write(fitness_row)
        output.write("\n")
    output.close()


    best_output = open(folder+"/_best.csv", "w")
    individual_row = np.array2string(final_pop[0], formatter={'float_kind':lambda x: "%.2f" % final_pop[0]})
    best_output.write(individual_row)

    best_output.write(",")
    fitness_row = str(final_pop_fitnesses[0])
    best_output.write(fitness_row)
    
    best_output.write(",")
    best_output.write(str(problem.powerplants[:3]))

    best_output.write("\n")
    best_output.close()



    savefig(paretofront)
    

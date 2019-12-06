'''
src/main.py

this is the main file where tune params to find better solutions
'''

from pylab import *

from inspyred import benchmarks
from inspyred.ec import variators
from inspyred_utils import NumpyRandomWrapper
from wind_turbines_location import WindTurbines, wind_turbines_mutation

import multi_objective

import sys

""" 
-------------------------------------------------------------------------
SETTINGS
"""

display = False

# parameters for NSGA-2
args = {}
args["pop_size"] = 50
args["max_generations"] = 100
constrained = True
c_budget = 125 # in milion dollars

"""
-------------------------------------------------------------------------
"""

problem = WindTurbines(budget=c_budget)
if constrained :
    args["constraint_function"] = problem.constraint_function
args["objective_1"] = "Produced Power (Kw/h)"
args["objective_2"] = "Cost ($)"

args["variator"] = [variators.blend_crossover,wind_turbines_mutation]

args["fig_title"] = 'NSGA-2'

if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
    
    final_pop, final_pop_fitnesses = multi_objective.run_nsga2(rng, problem, display=display, 
                                         num_vars=2, **args)
    
    #print ("Final Population\n", final_pop)
    print ("Final Population Fitnesses\n", final_pop_fitnesses)


    '''
    output = open("exercise_1.csv", "w")
    for individual, fitness in zip(final_pop, final_pop_fitnesses) :
        output.write(reduce(lambda x,y : str(x) + "," + str(y), 
                            individual))
        output.write(",")
        output.write(reduce(lambda x,y : str(x) + "," + str(y), 
                            fitness))
        output.write("\n")
    output.close()
    
    ioff()
    show()
    '''

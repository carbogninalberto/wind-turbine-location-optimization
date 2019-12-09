'''
src/wind_turbines_location.py

this file contains the wind turbines problem class and a bunch of custom functions
'''

from inspyred import benchmarks 
from inspyred.ec.emo import Pareto
from inspyred.ec.variators import mutator
from inspyred.ec.variators import crossover
import copy
import fitness as fit
import numpy as np
import utils
import math

'''
Wind Location Optimization Problem
'''
class WindTurbines():
    def __init__(self, n_turbines=1, n_cities=110, matrix_power_filename="../dataParsingScripts/mean_power.json", wind_turbines=["E-115/3000"], wind_turbines_costs=[1.25], budget=50, n_powerplants=1):
        self.n_turbines = n_turbines
        self.n_cities = n_cities
        self.matrix_power_filename = matrix_power_filename
        self.wind_turbines = wind_turbines
        self.wind_turbines_costs = wind_turbines_costs
        self.budget = budget
        self.matrix_power, self.matrix_cities = fit.load_matrix_power(self.matrix_power_filename, self.wind_turbines)
        self.bounder = WindTurbinesBounder()
        self.objectives = 3
        self.maximize = True
        self.matrix_vector = []
        self.generation = -1
        self.n_powerplants = n_powerplants
        self.powerplants = []
        self.best_fitness = []
        self.best_fitness_power = 0


    def generator(self, random, args):
        #np.random.randint(1) 
        return utils.matrix_to_vector([[ 0 for i in range(self.n_cities)] for i in range(self.n_turbines)])[0] #np.random.randint(10, size=(self.n_turbines, self.n_cities)) #[np.random.randint(10) for _ in range(n_turbines)]

    # fitness
    def evaluator(self, candidates, args):
        fitness = []
        self.generation += 1
        for c in candidates:
            #print("c: ", c, "\n conversion: ", utils.vector_to_matrix(c, self.n_turbines, self.n_cities))
            c_power = fit.wind_turbine_power_fitness(np.array(utils.vector_to_matrix(c, self.n_turbines, self.n_cities)), self.matrix_power)

            c_cost, cities_with = fit.wind_turbine_cost_fitness(np.array(utils.vector_to_matrix(c, self.n_turbines, self.n_cities)), self.wind_turbines_costs)

            #print(c_cost, cities_with)

            power_plant = fit.PowerPlant(utils.vector_to_matrix(c, self.n_turbines, self.n_cities), self.matrix_cities.tolist(), 10).run()
            
            '''
            the cost of building transmission line for electrcity is 2.24 mil. Dollars per km
            Transporting actualy electrcity costs 3.61 dollars per km per kW. 
            '''
            c_cost_power_plant = power_plant.fitness * (3.61*10**(-6))*(c_power*10**(6)) # 0.02 -> 2 $ per km
            #c_cost_power_plant = power_plant.fitness * 0.01 # 0.02 -> 2 $ per km

            total_cost = (c_cost + c_cost_power_plant)

            # 0: lat, 1: long
            #print("lat,lon")
            for i in range(self.n_powerplants):
                #print(power_plant.candidate[0+i*2],",",power_plant.candidate[1+i*2])
                if self.best_fitness_power <= c_power and [c_power, total_cost] >=  self.best_fitness:
                    self.best_fitness = [c_power, total_cost]
                    self.best_fitness_power = c_power
                    self.powerplants.append([power_plant.candidate[0+i*2], power_plant.candidate[1+i*2]])

            '''
            penalty
            if (self.budget - total_cost) < 0:
                c_power = 0

            ''' 

            fitness.append(Pareto([c_power, total_cost], [True, False]))
        
        print("GENERATION: [", self.generation, "] | fitness of 3 individuals (not sorted): ", fitness[:3])
        return fitness    

class WindTurbinesBounder(object):    
    def __call__(self, candidate, args):

        for i in range(len(candidate)):
            candidate[i] = math.ceil(candidate[i]) #clean round up
            if float(candidate[i]) < 0:
                candidate[i] = 0        

        return candidate

@mutator    
def wind_turbines_mutation(random, candidate, args):
    '''
    Customized gaussian mutation to integer
    '''
    mut_rate = args.setdefault('mutation_rate', 0.01)
    mean = args.setdefault('gaussian_mean', 0.0)
    stdev = args.setdefault('gaussian_stdev', 0.2)
    bounder = WindTurbinesBounder()
    mutant = copy.copy(candidate)
    for i, m in enumerate(mutant):
        if random.random() < mut_rate:
            mutant[i] += math.ceil(random.gauss(mean, stdev)) # round up mutation
    mutant = bounder(mutant, args)
    #print("mutant:", mutant, end="")
    return mutant

@crossover
def wind_turbines_blend_crossover(random, mom, dad, args):
    """Return the offspring of blend crossover on the candidates.

    This function performs blend crossover (BLX), which is similar to 
    arithmetic crossover with a bit of mutation. It creates offspring
    whose values are chosen randomly from a range bounded by the
    parent alleles but that is also extended by some amount proportional
    to the *blx_alpha* keyword argument. It is this extension of the
    range that provides the additional exploration. This averaging is 
    only done on the alleles listed in the *blx_points* keyword argument. 
    If this argument is ``None``, then all alleles are used. This function 
    also makes use of the bounder function as specified in the EC's 
    ``evolve`` method.

    .. Arguments:
       random -- the random number generator object
       mom -- the first parent candidate
       dad -- the second parent candidate
       args -- a dictionary of keyword arguments

    Optional keyword arguments in args:
    
    - *crossover_rate* -- the rate at which crossover is performed 
      (default 1.0)
    - *blx_alpha* -- the blending rate (default 0.1)
    - *blx_points* -- a list of points specifying the alleles to
      recombine (default None)
    
    """
    blx_alpha = args.setdefault('blx_alpha', 0.1)
    blx_points = args.setdefault('blx_points', None)
    crossover_rate = args.setdefault('crossover_rate', 0.2)
    bounder = args['_ec'].bounder
    children = []
    if random.random() < crossover_rate:
        bro = copy.copy(dad)
        sis = copy.copy(mom)
        if blx_points is None:
            blx_points = list(range(min(len(bro), len(sis))))
        for i in blx_points:
            smallest, largest = min(mom[i], dad[i]), max(mom[i], dad[i])
            delta = blx_alpha * (largest - smallest)
            bro[i] = smallest - delta + random.random() * (largest - smallest + 2 * delta)
            sis[i] = smallest - delta + random.random() * (largest - smallest + 2 * delta)
        bro = bounder(bro, args)
        sis = bounder(sis, args)
        children.append(bro)
        children.append(sis)
    else:
        children.append(mom)
        children.append(dad)
    return children    
    
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
    def __init__(self, n_turbines=1, n_cities=110, matrix_power_filename="../dataParsingScripts/mean_power.json", wind_turbines=["E-115/3000"], wind_turbines_costs=[1.25], budget=50):
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
        self.generation = 0


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

            power_plant = fit.PowerPlant(utils.vector_to_matrix(c, self.n_turbines, self.n_cities), self.matrix_cities.tolist()).run()

            c_cost_power_plant = power_plant.fitness * 0.01 # 0.02 -> 2 $ per km

            total_cost = (c_cost + c_cost_power_plant)

            '''
            penalty
            '''

            if (self.budget - total_cost) < 0:
                c_power = 0
            
            
            '''
            fitness.append(ConstrainedPareto([c_power, total_cost],
                                             self.constraint_function(total_cost),
                                             self.maximize))
            '''

            fitness.append(Pareto([c_power, total_cost], self.maximize))
        print("GENERATION: [", self.generation, "] | fitness 3 individuals: ", fitness[:3])
        return fitness    

    def constraint_function(self,cost):
        #print("budget violation:", self.budget - cost)

        violations = 0
        if (self.budget - cost) <= 0:
            violations += 1/(self.budget - cost + 0.00001) #1/self.budget - 1/cost

        return violations #0 if (self.budget - cost) > 0 else self.budget - cost

class WindTurbinesBounder(object):    
    def __call__(self, candidate, args):
        '''
        we cannot evolve to negative values of turbines
        
        for i in range(candidate):
            for j in range(candidate[i]):
                if float(candidate[i][j]) < 0.0:
                    candidate[i][j] = 0

        '''

        for i in range(len(candidate)):
            candidate[i] = math.ceil(candidate[i]) #clean round up
            if float(candidate[i]) < 0:
                candidate[i] = 0        

        return candidate

class ConstrainedPareto(Pareto):
    def __init__(self, values=None, violations=None, ec_maximize=True):
        Pareto.__init__(self, values)
        self.violations = violations
        self.ec_maximize=ec_maximize
    
    def __lt__(self, other):
        if self.violations is None :
            return Pareto.__lt__(self, other)
        elif len(self.values) != len(other.values):
            raise NotImplementedError
        else:
            if self.violations > other.violations :
                # if self has more violations than other
                # return true if EC is maximizing otherwise false 
                return (self.ec_maximize)
            elif other.violations > self.violations :
                # if other has more violations than self
                # return true if EC is minimizing otherwise false  
                return (not self.ec_maximize)
            elif self.violations > 0 :
                # if both equally infeasible (> 0) than cannot compare
                return False
            else :
                # only consider regular dominance if both are feasible
                not_worse = True
                strictly_better = False 
                for x, y, m in zip(self.values, other.values, self.maximize):                    
                    if m:
                        if x > y:
                            not_worse = False
                        elif y > x:
                            strictly_better = True
                    else:
                        if x < y:
                            not_worse = False
                        elif y < x:
                            strictly_better = True
            return not_worse and strictly_better

@mutator    
def wind_turbines_mutation(random, candidate, args):
    '''
    Customized gaussian mutation to integer
    '''
    mut_rate = args.setdefault('mutation_rate', 0.01)
    mean = args.setdefault('gaussian_mean', 0.0)
    stdev = args.setdefault('gaussian_stdev', 0.1)
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
    
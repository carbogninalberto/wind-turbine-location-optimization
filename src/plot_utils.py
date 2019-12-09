'''
src/plot_utils.py

this file constains utils for plotting graphs
'''

from pylab import *
import sys

from inspyred_utils import CombinedObjectives
from inspyred_utils import single_objective_evaluator


def plot_results_multi_objective_PF(individuals, title) :
    num_objectives = len(individuals[0].fitness)
    
    if num_objectives < 2:
        pass
    elif num_objectives == 2:
        figure(title)
        plot([guy.fitness[0] for guy in individuals],
             [guy.fitness[1] for guy in individuals],
             '.b', markersize=7)
        xlabel('Turbines Power in MW/h')
        ylabel('Budget (in mln $)')
    else:
        # Creates two subplots and unpacks the output array immediately
        f, axes = subplots(num_objectives, num_objectives, sharex='col', sharey='row')
        for i in range(num_objectives):
            for j in range(num_objectives):
                axes[i,j].plot([guy.fitness[j] for guy in individuals],
                                [guy.fitness[i] for guy in individuals],
                               '.b', markersize=7)
                axes[i,j].set_xlabel('f'+str(j))
                axes[i,j].set_ylabel('f'+str(i))
        f.subplots_adjust(hspace=0.30)
        f.subplots_adjust(wspace=0.30)


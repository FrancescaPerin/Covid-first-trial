import numpy as np
import json
import argparse 
import os

from nation import Nation
from agent import Agent

from utils import check_file, load_JSON, load_contact, load_pop, summary_C
from plots import plot_age_compartment_comparison, plot_compartment_comparison


parser = argparse.ArgumentParser(description='Passing arguments to code.')

parser.add_argument('--agent_params',type=check_file, default='agents_SEAIRD.json',
                    help='JSON file with definition of agents parameters')
parser.add_argument('--topology', type=check_file, default='topology.json',
                    help='JSON file with topology definition of model')
parser.add_argument('--settings', type=check_file, default='settings.json',
                    help='JSON file with settings of outer model')

args = parser.parse_args()

# Loading agents from JSON file
data_agents = load_JSON(args.agent_params)
  
# Loading topology from JSON file
connections=  load_JSON(args.topology)

settings = load_JSON(args.settings)

# Saving dictionary containing Agent objects 

agents = {}

for agent in data_agents:

		cont_matrix = load_contact(agent['name'])

		population = load_pop(agent['name'], settings['age_group'])

		if settings['age_group'] == True:

			pop_perc = population/population.sum()

			for key, value in agent['state'].items():

				agent['state'][key] = pop_perc*value

		

		if settings['age_group'] == False:

			C = np.array(0.8)
		else:

			C=summary_C(cont_matrix,alpha=0.2)

		agent_obj = Nation(cont_matrix, population, C, **agent)

		agents[agent_obj.name]=agent_obj



for i in range(settings['iterations']):

	for agent in agents:
	    
		agents[agent].interact([agents.get(key) for key in connections[agent]], settings['pop_migration'])

	
	for agent in agents:

		agents[agent].set_state(agents[agent].next_state)
		

if settings['age_group']==True:
	plot_age_compartment_comparison( agents, 0, "Susceptible")
	plot_age_compartment_comparison( agents, 1, "Exposed")
	plot_age_compartment_comparison( agents, 3, "Infected")
	plot_age_compartment_comparison( agents, 4, "Recovered")

else:
	plot_compartment_comparison( agents, 0, "Susceptible")
	plot_compartment_comparison( agents, 1, "Exposed")
	plot_compartment_comparison( agents, 3, "Infected")





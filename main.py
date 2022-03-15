import numpy as np
import json
import argparse 
import os

from nation import Nation
from agent import Agent

from utils import check_file, load_JSON, load_contact, load_pop, summary_C, calc_loss_GDP
from plots import plot_age_compartment_comparison, plot_compartment_comparison, plot_loss_GDP


parser = argparse.ArgumentParser(description='Passing arguments to code.')

parser.add_argument('--agent_params',type=check_file, default='agents_SEAIRD.json',
                    help='JSON file with definition of agents parameters')
parser.add_argument('--topology', type=check_file, default='topology.json',
                    help='JSON file with topology definition of model')
parser.add_argument('--settings', type=check_file, default='settings.json',
                    help='JSON file with settings of outer model')
parser.add_argument('--cont_params', type=check_file, default='contact_settings.json',
                    help='JSON file with settings of outer model')
parser.add_argument('--economy_params', type=check_file, default='economy_settings.json',
                    help='JSON file with settings of outer model')


args = parser.parse_args()

# Loading agents from JSON file
data_agents = load_JSON(args.agent_params)
  
# Loading topology from JSON file
connections=  load_JSON(args.topology)

settings = load_JSON(args.settings)

cont_params = np.asarray(list(load_JSON(args.cont_params).values()))


economy_params = load_JSON(args.cont_params)
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

			C=summary_C(cont_matrix, cont_params, alpha=0.2)

		agent_obj = Nation(cont_matrix, cont_params, population, C, **agent)

		agents[agent_obj.name]=agent_obj


loss=np.zeros((len(agents),2))

for i in range(settings['iterations']):

	for agent in agents:
	    
		agents[agent].interact([agents.get(key) for key in connections[agent]], settings['pop_migration'])

		#if settings['economy'] == True:
			#new_loss=[loss[idx][-1]+ calc_loss_GDP(agents[agent], i, *economy_params.values(), alpha=0.2)]
			#np.append(loss[idx][:], new_loss)

	for agent in agents:

		#if settings['economy'] == True:

			#print(agents[agent].state.loss)
			#new_loss = agents[agent].state.loss+ calc_loss_GDP(agents[agent], i, *economy_params.values(), alpha=0.2)
			

		agents[agent].set_state(agents[agent].next_state(i))



		
#print(agents['Italy'].history)

if settings['age_group']==True:

	plot_loss_GDP(agents)
	plot_age_compartment_comparison( agents, 0, "Susceptible", settings['age_group_summary'])
	plot_age_compartment_comparison( agents, 1, "Exposed", settings['age_group_summary'])
	plot_age_compartment_comparison( agents, 3, "Infected", settings['age_group_summary'])
	plot_age_compartment_comparison( agents, 4, "Recovered", settings['age_group_summary'])

else:
	plot_loss_GDP(agents)
	plot_compartment_comparison( agents, 0, "Susceptible")
	plot_compartment_comparison( agents, 1, "Exposed")
	plot_compartment_comparison( agents, 3, "Infected")





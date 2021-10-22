import numpy 
import json
import argparse 

from agent import Agent, Nation, NationCities 
from utils import check_file, load_JSON
from plots import plot_compartment_comparison


parser = argparse.ArgumentParser(description='Passing arguments to code.')

parser.add_argument('--agent_params',type=check_file, default='agent_params.json',
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

		if settings['nation_def']=='Nation':

			agent_obj = Nation(**agent)

		elif settings['nation_def']=='NationCities':

			agent_obj = NationCities(**agent)


		agents[agent_obj.name]=agent_obj

for i in range(settings['iterations']):

	for agent in agents:
	    
		agents[agent].interact([agents.get(key) for key in connections[agent]], settings['pop_migration'])

	
	for agent in agents:
		agents[agent].set_state(agents[agent].next_state)
		


plot_compartment_comparison(agents, 1, "Exposed")
plot_compartment_comparison(agents, 2, "Infected")




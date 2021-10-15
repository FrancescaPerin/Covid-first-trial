import numpy 
import json
import argparse 

from agent import Agent 
from utils import check_file, load_JSON


parser = argparse.ArgumentParser(description='Passing arguments to code.')

parser.add_argument('--agent_param',type=check_file, default='agent_params.json',
                    help='JSON file with definition of agents parameters')
parser.add_argument('--topology', type=check_file, default='topology.json',
                    help='JSON file with topology definition of model')

args = parser.parse_args()

# Loading agents from JSON file
data_agents= load_JSON(args.agent_param)
  
# Loading topology from JSON file
connections= load_JSON(args.topology)

# Saving dictionary containing Agent objects 
agents= {}

for agent in data_agents:
		agent_obj=Agent(**agent)

		agents[agent_obj.name]=agent_obj

for _ in range(10):
	print(agents['a'], agents['b'], agents['c'])
	    
	agents['a']. interact([agents.get(key) for key in connections['a']], 1, 5)

	print(agents['a'], agents['b'], agents['c'])




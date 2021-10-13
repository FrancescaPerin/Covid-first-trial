import numpy 
import json

from agent import Agent 

# Loading agents from JSON file
with open('agent_params.json') as agents_json:
    data_agents = json.load(agents_json)
  
# Loading topology from JSON file
with open('topology.json') as conn_json:
    connections = json.load(conn_json)

# Saving dictionary containing Agent objects 
agents= {}
for agent in data_agents:
	agent_obj=Agent(**agent)

	agents[agent_obj.name]=agent_obj

    
agents['a']. interact([agents.get(key) for key in connections['a']], 1, 5)

print(agents['a'], agents['b'], agents['c'])

"""
agent_a=Agent('a',10, 10 ,10)
agent_b= Agent('b',20, 15, 10)
agent_c= Agent('c',20, 15, 10)

print(agent_a)
print(agent_b)

agent_a.interact([agent_b, agent_c], 1, 5)


print(agent_a)
print(agent_b)
print(agent_c)
"""



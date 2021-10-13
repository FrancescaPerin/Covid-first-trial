import numpy 
import json

from agent import Agent 


with open('agent_params.json') as json_file:
    data_agents = json.load(json_file)
  
    # Print the type of data variable
    print("Type:", type(data_agents))
  
    # Print the data of dictionary
    print("\na:", data_agents)

agents= {}
for agent in data_agents:
	agent_obj=Agent(**agent)

	agents[agent_obj.name]=agent_obj

print(agents)

    
agents['a']. interact([agents['b']],1,5)

print(agents['a'],  agents['b'])

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



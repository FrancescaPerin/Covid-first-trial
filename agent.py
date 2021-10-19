import numpy as np

from state import State

class Agent:

	def __init__(self, name, state, parameters):

		self.name= name
		self.state = State(**state)
		self.parameters = parameters


		#State(*(state.array + 10))

	
	def __repr__ (self):

		return "\nAgent %s : \n\t %s,\n\t " % (self.name, self.state)
	
	def set_state(self, state):

		self.state=state

		return self

	def emigrate (self, value):

		self.state.set_N('-',value)

		#new_state = self.state.next_state(self.parameters)
		return self

	def immigrate (self, mig_agent, value):

		print(f'Value:{value}')

		calc_new_seir =  ((mig_agent.state.SEIR * value) + (self.state.SEIR * self.state.N)) / (value + self.state.N)


		new_state = State(*calc_new_seir,  value + self.state.N)

		#print(new_state)

		#new_state=self.state.next_state(self.parameters)

		return new_state

	def interact(self, conn_agents, value):

		migration= int(self.state.N * value)

		new_self=self.emigrate(migration)

		#self=self.set_state(new_state_self)

		for agent in conn_agents:

			new_state_agent = agent.immigrate(self, migration/len(conn_agents))

		for agent in conn_agents:

			agent=agent.set_state(new_state_agent)


		return self, conn_agents



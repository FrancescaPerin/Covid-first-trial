import numpy as np

from state import State

class Agent:

	def __init__(self, name, state, parameters):

		self.name= name
		self.state = State(**state)
		self.parameters = parameters
		self.__history = [self.state.to_array, self.state.to_array]
	
	def __repr__ (self):

		return "\nAgent %s : \n\t %s,\n\t " % (self.name, self.state)
	
	def update_history(self, state):

		self.__history.append(state.to_array)

	def set_state(self, state):

		#print(self.name, state)

		self.state=state

		self.update_history(state)

		return self

	def replace_state(self, state):

		#print(self.name, state)

		self.state=state

		self.__history[-1]=state.to_array

		return self

	@property
	def history(self):

		return np.asarray(self.__history)

	def emigrate (self, value):

		new_state= np.append(self.state.SEIR,self.state.set_value('-',value))

		self.replace_state(State(*new_state))

		return self

	def immigrate (self, mig_agent, value):

		calc_new_seir = ((mig_agent.state.SEIR * value) + (self.state.SEIR * self.state.N)) / (value + self.state.N)


		new_state = State(*calc_new_seir,  value + self.state.N)

		return new_state

	def interact(self, conn_agents, value):

		migration= int(self.state.N * value)

		self.emigrate(migration)

		for agent in conn_agents:

			new_state_agent = agent.immigrate(self, migration/len(conn_agents))


			agent.replace_state(new_state_agent)


		return self,conn_agents

	@property
	def next_state(self):

		S, E, I, R, N = self.state.to_array

		a, b, g, d, r = [*self.parameters.values()]
		
		next_S = S - (r * b * S * I) + (d * R)  # Add fraction of recovered compartment.
		next_E = E + (r * b * S * I - a * E)
		next_I = I + (a * E - g * I)
		next_R = R + (g * I) - (d * R)  # Remove fraction of recovered compartment.

		return State(next_S, next_E, next_I, next_R, N)



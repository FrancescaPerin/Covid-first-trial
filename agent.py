import numpy as np

from state import State
from abc import ABC

class Agent(ABC):

	def __init__(self, name, state, parameters):

		self.name= name
		self.state = State(**state)
		self.parameters = parameters
		self.__history = [self.state.to_array, self.state.to_array]
	
	def __repr__ (self):

		return "\nAgent %s : \n\t %s,\n\t " % (self.name, self.state)
	
	def update_history(self, state):

		print(state.to_array)

		self.__history.append(state.to_array)

	def set_state(self, state):
		print(self.state)

		self.state=state

		self.update_history(state)

		return self

	def replace_state(self, state):

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

	def interact(self):

		pass

	#@property
	def next_state(self):
		pass


class Nation(Agent):

	def interact(self, conn_agents, value):

		migration= int(self.state.N * value)

		self.emigrate(migration)

		for agent in conn_agents:

			new_state_agent = agent.immigrate(self, migration/len(conn_agents))


			agent.replace_state(new_state_agent)


		return self,conn_agents

	@property
	def next_state(self):
		"""
		ß= rate of transmission
		n= natural death rate
		c(t)=mitigation policies factor
		s= measuring effect of isolation policy
		g=infected/aymptomatic recovery rate
		d=infected die rate
		e=
		k="""


		S, E, A, I, R, D, N = self.state.to_array

		b, n, c, s, g, d, e, k = [*self.parameters.values()]


		
		next_S = S - (b * S * c) * (s * I + E + A) - (n * S) + (n * (1 - D))  # Add fraction of recovered compartment.
		next_E = E + (b * c * S) * (s * I + E + A) - (k + n)*E
		next_A = A + (1 - e) * k * E - (g + n) * A
		next_I = I + (e * k * E) - (g + d + n) * I
		next_R = R + (g * (A + I)) - (n * R) 
		next_D = D + d * I  # Remove fraction of recovered compartment.

		return State(next_S, next_E, next_A, next_I, next_R, next_D, N)


























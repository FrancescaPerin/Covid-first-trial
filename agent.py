import numpy as np

from state import State
from abc import ABC

class Agent(ABC):

	def __init__(self, contact_matrix, population, name, state, parameters):

		self.contact_matrix = contact_matrix
		self.name= name
		self.state = State(population, **state)
		self.parameters = parameters
		self.__history = [self.state.to_array, self.state.to_array]
	
	def __repr__ (self):

		return "\nAgent %s :\n\t Contact matrix:\n\t %s \n\n\t %s,\n\t " % (self.name, self.contact_matrix, self.state)
	
	def update_history(self, state):

		#print(state.to_array)

		self.__history.append(state.to_array)

	def set_state(self, state):
		#print(self.state)

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





























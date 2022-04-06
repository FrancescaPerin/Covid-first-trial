import numpy as np

from state import State
from replayBuffer import replayBuffer
from abc import ABC

class Agent(ABC):

	def __init__(self, config_par, contact_matrix, cont_param, population, C,  name, state, parameters):

		self.contact_matrix = contact_matrix
		self.cont_param = cont_param
		self.population = population
		self.C= C
		self.name= name
		self.state = State(population, **state)
		self.parameters = parameters
		self.__history = [self.state.to_array, self.state.to_array]
		self.__replaybuffer = replayBuffer(config_par['maxMemSize'])
	
	def __repr__ (self):

		return "\nAgent %s :\n\t Contact matrix:\n\t %s \n\n\t %s,\n\t " % (self.name, self.contact_matrix, self.state)
	
	def update_history(self, state):

		self.__history.append(state.to_array)

	def set_state(self, action, reward ,next_state):

		transition = (self.state, action, reward, next_state)

		self.__replaybuffer.append(transition)

		#print(len(self.__replaybuffer))

		self.state = next_state

		self.update_history(self.state)

		return self

	def replace_state(self, state):

		self.state=state

		self.__history[-1]=state.to_array

		return self

	def update_C(self, C):

		self.C = C

		return self

	@property
	def history(self):

		return np.asarray(self.__history)

	def emigrate (self, value):

		new_state= State(self.state.set_value('-',value), *self.state.SEAIRDV)

		self.replace_state(new_state)

		return self

	def immigrate (self, mig_agent, value):

		calc_new_seir = ((mig_agent.state.SEAIRDV * value) + (self.state.SEAIRDV * self.state.N)) / (value + self.state.N)


		new_state = State(value + self.state.N, *calc_new_seir)

		return new_state

	def interact(self):

		pass

	#@property
	def next_state(self):
		pass

	def policy(self, alpha):

		pass

	def update():
		pass




























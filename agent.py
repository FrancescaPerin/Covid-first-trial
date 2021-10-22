import numpy as np

from state import State

class Agent:

	def __init__(self, name, state, parameters):

		self.name= name
		self.state = State(**state)
		self.parameters = parameters
		self.__history = [self.state.to_array]
	
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

		
		#self.replace_state(self.state.next_state(self.parameters))

		#for agent in conn_agents:

			#agent.replace_state(agent.state.next_state(agent.parameters))

		return self,conn_agents



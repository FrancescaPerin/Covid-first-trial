import numpy as np

from state import State
from agent import Agent

class NationCities(Agent):

	def interact(self, conn_agents, value):

		migration= int(self.state.N * 0.4)

		self.emigrate(migration)

		for agent in conn_agents:

			new_state_agent = agent.immigrate(self, migration/len(conn_agents))


			agent.replace_state(new_state_agent)


		return self,conn_agents
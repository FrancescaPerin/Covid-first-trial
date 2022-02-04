import numpy as np

from state import State
from agent import Agent

class Nation(Agent):

	def interact(self, conn_agents, value):

		migration= int(self.state.N_tot * value)

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
import numpy as np

from state import State
from agent import Agent

class Nation(Agent):

	def interact(self, conn_agents, value):

		migration= self.state.N * value

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
		e= p
		k= alpha
		w_a, w_m= environment transmission

		next_S = S - (b * S * c) * (s * I + E + A) - (n * S) + (n * (1 - D))  # Add fraction of recovered compartment.
		next_E = E + (b * c * S) * (s * I + E + A) - (k + n)*E
		next_A = A + (1 - e) * k * E - (g + n) * A
		next_I = I + (e * k * E) - (g + d + n) * I
		next_R = R + (g * (A + I)) - (n * R) 
		next_D = D + d * I  # Remove fraction of recovered compartment.
		next_V = w_a*A+w_i*I
		"""


		N, S, E, A, I, R, D, V = self.state.to_array

		b, n, c, s, g, d, e, k, w_a, w_i, p = [*self.parameters.values()]

		if self.C.shape!=(3,3):

			next_S = S - sum(b) * S * (self.C * V + self.C * (A + I)) - n * S - n * (1 - D) + 0.0035 * R

			next_E = E + sum(b) * S * (self.C * V + self.C * (A + I)) - (k + n) * E


		else:


			next_S = S - b * S * (self.C @ V + self.C @ ((A + I) / N.sum())) - n * S - n * (1 - D) + 0.0035 * R 

			next_E = E + b * S * (self.C @ V + self.C @ ((A + I) / N.sum())) - (k + n) * E

		next_A = A + (1 - e) * k * E - (g + n) * A 

		next_I = I + (e * k * E) - (g + d + n) * I

		next_R = R + (g * (A + I)) - (n * R) - 0.0035 * R

		next_D = D + d * I 

		next_V = (w_a * A) + (w_i * I) - p * V

		#if next_S+next_E+next_A+next_I+next_R+next_D>1:

			#exit(0)
		
		return State(N, next_S, next_E, next_A, next_I, next_R, next_D, next_V)

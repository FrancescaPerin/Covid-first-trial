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
		k=
		w_a, w_m= environment transmission
		"""


		S, E, A, I, R, D, V, N = self.state.to_array

		b, n, c, s, g, d, e, k, w_a, w_i = [*self.parameters.values()]


		
		next_S = S - (b * S * c) * (s * I + E + A) - (n * S) + (n * (1 - D))  # Add fraction of recovered compartment.
		next_E = E + (b * c * S) * (s * I + E + A) - (k + n)*E
		next_A = A + (1 - e) * k * E - (g + n) * A
		next_I = I + (e * k * E) - (g + d + n) * I
		next_R = R + (g * (A + I)) - (n * R) 
		next_D = D + d * I  # Remove fraction of recovered compartment.
		next_V = w_a*A+w_i*I

		"""
		next_S_i= S_i - b*S*(C*V)    - n * S_i - n * (1 - D_i)

		next_E_i = E_i 

		next_A_i = A_i + (1- e) * k * E_i - (g + n) * A_i

		next_I_i = I_i + (e * k * E_i) - (g +d + n)* A

		next_R_i = R_i +(g * (A_i + I_i)) - n * (R_i)

		next_D_i = D_i + d * I_i

		next_V_i = (w_a * A_i) + (w_i * I_i) 
		"""

		return State(next_S, next_E, next_A, next_I, next_R, next_D, next_V, N)

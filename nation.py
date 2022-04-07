import numpy as np

from state import State
from agent import Agent
from utils import calc_loss_GDP

class Nation(Agent):

	def interact(self, conn_agents, value):

		if type(value) is not dict:

			migration = self.state.N * value

			self.emigrate(migration)

			for agent in conn_agents:

				new_state_agent = agent.immigrate(self, migration/len(conn_agents))

				agent.replace_state(new_state_agent)

			return self, conn_agents

		else:

			for agent in conn_agents:

				migration = int(value[agent.name].get('departures')/365)

				self.emigrate(migration)

				new_state_agent = agent.immigrate(self, migration)

				agent.replace_state(new_state_agent)

			return self, conn_agents

	
	def next_state(self, t):
		"""
		b= rate of transmission
		n= natural death rate
		alpha / c(t)= containment policy 
		s= measuring effect of isolation policy
		g=infected/aymptomatic recovery rate
		d=infected die rate
		e= 
		k= 
		w_a, w_m= environment contamination
		f = lost immunity ratio
		rho= removal environment contamination

		next_S = S - (b * S * c) * (s * I + E + A) - (n * S) + (n * (1 - D))  # Add fraction of recovered compartment.
		next_E = E + (b * c * S) * (s * I + E + A) - (k + n)*E
		next_A = A + (1 - e) * k * E - (g + n) * A
		next_I = I + (e * k * E) - (g + d + n) * I
		next_R = R + (g * (A + I)) - (n * R) 
		next_D = D + d * I  # Remove fraction of recovered compartment.
		next_V = w_a*A+w_i*I
		"""

		N, S, E, A, I, R, D, V, loss = self.state.to_array

		p = self.cont_param


		b, n, c, s, g, d, e, k, w_a, w_i, f, rho = [*self.parameters.values()]

		if self.C.shape!=(3,3):

			p = p[1] #select p value of adult since without age groups all populations will be considered adult of working age 

			next_S = S - sum(b) * S * (self.C * V + self.C * (A + I)) - n * S - n * (1 - D) + f * R

			next_E = E + sum(b) * S * (self.C * V + self.C * (A + I)) - (k + n) * E

		else:

			next_S = S - b * S * (self.C @ V + self.C @ ((A + I) / N.sum())) - n * S - n * (1 - D) + f * R 

			next_E = E + b * S * (self.C @ V + self.C @ ((A + I) / N.sum())) - (k + n) * E

		next_A = A + (1 - e) * k * E - (g + n) * A 

		next_I = I + (e * k * E) - (g + d + n) * I

		next_R = R + (g * (A + I)) - (n * R) - f * R

		next_D = D + d * I 

		next_V = (w_a * (1-p) * A) + (w_i * (1-p) * I) - rho * V


		next_loss = loss + calc_loss_GDP(self, t)

		
		return State(N, next_S, next_E, next_A, next_I, next_R, next_D, next_V, next_loss)

	def policy(self, alpha):
		# TODO alpha should be a parameter passed in constructor and saved in self.__alpha or something similar
		return alpha

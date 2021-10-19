import numpy as np

class State:

	def __init__(self, S, E, I, R, N):

		self._state = np.array([S, E, I, R, N])

	def __repr__(self):

		return "State :  %s " % (self._state)
	
	@property
	def S(self):
		return self._state[0]

	@property
	def E(self):
		return self._state[1]

	@property
	def I(self):
		return self._state[2]

	@property
	def R(self):
		return self._state[3]

	@property
	def N(self):
		return self._state[4]

	def set_N(self, sign, value):

		if sign=='+':

			self._state[4] = self.N + value

		elif sign=='-':

			self._state[4] = self.N - value
		
		return self

	@property
	def to_array(self):
		return self._state

	@property
	def SEIR(self):
		return self._state[:4]


	def next_state(self, params):

		S, E, I, R, N = self._state

		a, b, g, d, r = [*params.values()]
		
		next_S = S - (r * b * S * I) + (d * R)  # Add fraction of recovered compartment.
		next_E = E + (r * b * S * I - a * E)
		next_I = I + (a * E - g * I)
		next_R = R + (g * I) - (d * R)  # Remove fraction of recovered compartment.

		return State(next_S, next_E, next_I, next_R, N)

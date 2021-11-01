import numpy as np

class State:

	def __init__(self, S, E, A, I, R, D, N):

		self._state = np.array([S, E, A, I, R, D, N])

	def __repr__(self):

		return "State :  %s " % (self._state)
	
	@property
	def S(self):
		return self._state[0]

	@property
	def E(self):
		return self._state[1]

	@property
	def A(self):
		return self._state[2]

	@property
	def I(self):
		return self._state[3]

	@property
	def R(self):
		return self._state[4]

	@property
	def D(self):
		return self._state[5]

	@property
	def N(self):
		return self._state[6]

	def set_value(self, sign, value):

		if sign=='+':

			value = self.N + value

		elif sign=='-':

			value = self.N - value
		
		return value

	@property
	def to_array(self):
		return self._state

	@property
	def SEIR(self):
		return self._state[:6]

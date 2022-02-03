import numpy as np

class State:

	def __init__(self, N, S, E, A, I, R, D):

		self._state = np.array([ N, S, E, A, I, R, D])

	def __repr__(self):

		return "Population:  %s \n \t SEAIRD:	%s" % (self.N, self.SEAIRD )

	@property
	def N(self):
		return self._state[0]

	@property
	def S(self):
		return self._state[1]

	@property
	def E(self):
		return self._state[2]

	@property
	def A(self):
		return self._state[3]

	@property
	def I(self):
		return self._state[4]

	@property
	def R(self):
		return self._state[5]

	@property
	def D(self):
		return self._state[6]


	def set_N(self, N):

		self._state=N

		return self

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
	def SEAIRD(self):
		return self._state[1:]

import numpy as np


class State:
    def __init__(self, N, S, E, A, I, R, D, V, loss):

        self._state = np.array(
            list(map(
                lambda x: x if isinstance(x, np.ndarray) else np.array([x]), 
                [N, S, E, A, I, R, D, V, loss]
            ))
        ).astype(np.float32)

    def __repr__(self):

        return "Population:  %s \n \t SEAIRDV:	%s \n \t Loss: %s" % (
            self.N,
            self.SEAIRDV,
            self.loss,
        )

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

    @property
    def V(self):
        return self._state[7]

    @property
    def loss(self):
        return self._state[8]

    def set_N(self, N):

        self._state[0] = N

        return self

    def set_value(self, sign, value):

        if sign == "+":

            value = self.N + value

        elif sign == "-":

            value = self.N - value

        return value

    @property
    def to_array(self):
        return self._state

    @property
    def SEAIRDV(self):
        return np.row_stack(self._state[1:])

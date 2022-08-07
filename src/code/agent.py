from abc import ABC, abstractmethod

import numpy as np


class Agent(ABC):
    def __init__(
        self,
        config_par,
        name,
    ):

        self.config_par = config_par
        self.name = name

        self.state = None

        self._history = []

    def update_history(self, state):

        self._history.append(self.state_to_array(state))

    def state_to_array(self, state):
        return state

    def set_state(self, action, reward, next_state):

        self.state = next_state

        self.update_history(self.state)

        return self

    def replace_state(self, state):

        self.state = state

        self._history[-1] = self.state_to_array(state)

        return self

    @property
    def history(self):

        return np.asarray(self._history)

    @abstractmethod
    def policy(self):

        pass

    def update(self, n=1):
        pass

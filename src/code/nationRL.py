import numpy as np
import torch.nn as nn
from torch import Tensor
from torch.distributions.beta import Beta
from torch.optim import Adam

from agentRL import BetaAgent
from nation import Nation
from replayBuffer import replayBuffer


class NationRL(BetaAgent, Nation):
    # TODO ensure that neural policy gets called
    def __init__(
        self,
        config_par,
        contact_matrix,
        cont_param,
        population,
        C,
        name,
        state,
        parameters,
    ):

        BetaAgent.__init__(self, config_par=config_par, name=name)

        Nation.__init__(
            self,
            config_par,
            contact_matrix,
            cont_param,
            population,
            C,
            name,
            state,
            parameters,
        )

    # Give experience to agent

    def extract_state(self, state_info):
        return state_info.SEAIRDV.flatten().astype(float)

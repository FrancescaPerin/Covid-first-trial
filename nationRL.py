import torch.nn as nn
from torch import Tensor
from torch.distributions.beta import Beta

from nation import Nation
from replayBuffer import replayBuffer


class Net(nn.Module):
    def __init__(
        self,
        state_size,
        output_size,
        neurons=[128, 64, 32],
        activations="ReLU",
        out_activation=None,
        n_heads=1,
    ):

        super().__init__()

        # If activation is not a list (i.e. different activation per layer) then make it a list
        if not isinstance(activations, list):
            activations = [activations] * len(neurons)

        # Append input and output size to neurons
        neurons = [state_size] + neurons
        activations = [None] + activations

        # Initialize neural network
        self.__backbone = nn.Sequential()

        # Iterate over input size of layer, output size, and activation function
        for idx, (input_n, output_n, activation_function) in enumerate(
            zip(neurons[:-1], neurons[1:], activations[1:])
        ):
            # Create linear layer
            self.__backbone.add_module(f"layer_{idx}", nn.Linear(input_n, output_n))

            # Add activation function if provided
            if activation_function is not None:
                self.__backbone.add_module(
                    f"activation_{idx}", getattr(nn, activation_function)()
                )

        # Create output layer(s)
        self.__heads = []

        for _ in range(n_heads):

            head = nn.Sequential()
            head.add_module(f"layer_mean", nn.Linear(neurons[-1], output_size))

            if out_activation is not None:
                head.add_module(f"activation_mean", getattr(nn, out_activation)())

            self.__heads.append(head)

    def forward(self, state):

        # Get hidden layer up to before heads
        h = self.__backbone(state)

        # Get outputs from heads
        outputs = tuple(head(h) + 1e-7 for head in self.__heads)

        # Give outputs as is if more than one
        if len(self.__heads) > 1:
            return outputs

        # Unpack only output
        return outputs[0]


class NationRL(Nation):
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

        super().__init__(
            config_par,
            contact_matrix,
            cont_param,
            population,
            C,
            name,
            state,
            parameters,
        )

        self.__replaybuffer = replayBuffer(**config_par["bufferSettings"])
        self.__actor = Net(**config_par["networkParameters"]["actor"])
        self.__critic = Net(**config_par["networkParameters"]["critic"])

    def policy(self, alpha):

        # Get state from SEAIRDV
        state = self.state.SEAIRDV.flatten().astype(float)

        # Get alpha from actor
        alpha = self.get_dist(state).sample()

        return alpha.cpu().detach().numpy()

    def get_dist(self, state):

        # Get parameters of distribution of alpha
        alpha_dist_pars = self.__actor(Tensor(state))

        # Crete distribution over alpha
        return Beta(*alpha_dist_pars)

    def get_log_probs(self, state, action):

        dist = self.get_dist(state)
        return dist.log_prob(action)

    @property
    def net(self):
        return self.__net

    def set_state(self, action, reward, next_state):

        transition = (self.state, action, reward, next_state)
        self.__replaybuffer.append(transition)

        return super().set_state(action, reward, next_state)

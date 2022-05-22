import torch.nn as nn
from torch import Tensor
from torch.distributions.beta import Beta
from torch.optim import Adam
import numpy as np

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

    def to(self, device):
        self.__backbone.to(device)
        for head in self.__heads:
            head.to(device)


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

        # Parameters
        self.__gamma = config_par["networkParameters"]["gamma"]
        self.__device = config_par["networkParameters"]["device"]

        # Memory
        self.__replaybuffer = replayBuffer(**config_par["bufferSettings"])

        # Actor
        self.__actor = Net(**config_par["networkParameters"]["actor"]["net"])
        self.__actor.to(self.__device)
        self.__actor_optimizer = Adam(
            self.__actor.parameters(),
            **config_par["networkParameters"]["actor"]["optim"],
        )

        # Critic
        self.__critic = Net(**config_par["networkParameters"]["critic"]["net"])
        self.__critic.to(self.__device)
        self.__critic_optimizer = Adam(
            self.__critic.parameters(),
            **config_par["networkParameters"]["critic"]["optim"],
        )

    # Give experience to agent

    def set_state(self, action, reward, next_state):

        transition = (
            self.extract_state(self.state),
            action,
            [reward],
            self.extract_state(next_state),
        )
        self.__replaybuffer.append(transition)

        return super().set_state(action, reward, next_state)

    def extract_state(self, SEAIRDV):
        # TODO maybe give the option to concatenate the SEIARDV of all nations
        return SEAIRDV.SEAIRDV.flatten().astype(float)

    # Acting

    def policy(self):

        # Get state from SEAIRDV
        state = self.extract_state(self.state)

        # Get alpha from actor
        alpha = self.get_dist(Tensor(state).to(self.__device)).sample()

        return alpha.cpu().detach().numpy()

    def get_dist(self, state):

        # Get parameters of distribution of alpha
        alpha_dist_pars = self.__actor(state)

        # Crete distribution over alpha
        return Beta(*alpha_dist_pars)

    def get_log_probs(self, state, action):

        dist = self.get_dist(state)
        return dist.log_prob(action)

    # Learning

    def update(self, n=1):

        for step, t in zip(range(n), self.__replaybuffer):

            # Reset gradients
            self.__actor_optimizer.zero_grad()
            self.__critic_optimizer.zero_grad()

            # Compute loss
            actor_loss, critic_loss = self.update_batch(t)

            # Differentiate loss w.r.t. parameters
            if actor_loss is not None and critic_loss is not None:
                actor_loss.backward()
                critic_loss.backward()

                # Update parameters
                self.__actor_optimizer.step()
                self.__critic_optimizer.step()

    def update_batch(self, t):

        s1, a, r, s2 = map(lambda x: x.to(self.__device), t)

        TD_target = r + self.__gamma * self.__critic(s2)
        delta = (self.__critic(s1) - TD_target) ** 2

        actor_loss = -self.get_log_probs(s1, a) * delta.detach()

        return actor_loss.mean(), delta.mean()

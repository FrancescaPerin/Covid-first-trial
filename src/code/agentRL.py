import torch.nn as nn
from torch import Tensor
from torch.distributions.beta import Beta
from torch.distributions.multinomial import Multinomial
from torch.optim import Adam
from agent import Agent
from abc import abstractmethod
import torch

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


class AgentRL(Agent):
    def __init__(
        self,
        name,
        config_par,
    ):

        super().__init__(config_par=config_par, name=name)

        # Parameters
        self.__gamma = config_par["networkParameters"]["gamma"]
        self._device = config_par["networkParameters"]["device"]

        # Memory
        self.__replaybuffer = replayBuffer(**config_par["bufferSettings"])

        # Actor
        self._actor = Net(**config_par["networkParameters"]["actor"]["net"])
        self._actor.to(self._device)
        self._actor_optimizer = Adam(
            self._actor.parameters(),
            **config_par["networkParameters"]["actor"]["optim"],
        )

        # Critic
        self._critic = Net(**config_par["networkParameters"]["critic"]["net"])
        self._critic.to(self._device)
        self._critic_optimizer = Adam(
            self._critic.parameters(),
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

    def extract_state(self, state_info):
        return state_info

    # Acting

    def policy(self):

        # Get state vector
        state = Tensor(self.extract_state(self.state)).to(self._device)

        # Get alpha from actor
        return self.get_dist(state).sample().cpu().detach().numpy()

    @abstractmethod
    def get_dist(self, state):
        pass

    def get_log_probs(self, state, action):

        return self.get_dist(state).log_prob(action)

    # Learning

    def update(self, n=1):

        for step, t in zip(range(n), self.__replaybuffer):

            # Reset gradients
            self._actor_optimizer.zero_grad()
            self._critic_optimizer.zero_grad()

            # Compute loss
            actor_loss, critic_loss = self.update_batch(t)

            # Differentiate loss w.r.t. parameters
            if actor_loss is not None and critic_loss is not None:
                actor_loss.backward()
                critic_loss.backward()

                # Update parameters
                self._actor_optimizer.step()
                self._critic_optimizer.step()

    def extract_transition(self, t):

        return map(lambda x: x.to(self._device), t)

    def update_batch(self, t):

        s1, a, r, s2 = self.extract_transition(t)

        TD_target = r + self.__gamma * self._critic(s2)
        delta = (self._critic(s1) - TD_target) ** 2

        actor_loss = -self.get_log_probs(s1, a) * delta.detach()

        return actor_loss.mean(), delta.mean()


class BetaAgent(AgentRL):
    def get_dist(self, state):

        # Get parameters of distribution of alpha
        alpha_dist_pars = self._actor(state)

        # Crete distribution over alpha
        return Beta(*alpha_dist_pars)


class MultinomialAgent(AgentRL):
    def extract_transition(self, t):

        s1, a, r, s2 = super().extract_transition(t)

        # convert a to one-hot encoding
        I = torch.eye(
            self.config_par["networkParameters"]["actor"]["net"]["output_size"]
        ).to(self._device)
        a = I[a.to(torch.long)]

        return s1, a, r, s2

    def get_dist(self, state):

        # Get probabilities for each event
        log_probs = self._actor(state)

        # Create multinomial distribution
        return Multinomial(probs=log_probs)

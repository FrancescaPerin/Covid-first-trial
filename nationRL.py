import torch.nn as nn

from nation import Nation
from replayBuffer import replayBuffer


class Net(nn.Module):
    def __init__(
        self,
        state_size,
        action_size,
        neurons=[128, 64, 32],
        activations="ReLU",
    ):

        super().__init__()

        # If activation is not a list (i.e. different activation per layer) then make it a list
        if not isinstance(activations, list):
            activations = [activations] * len(neurons)

        # Append input and output size to neurons
        neurons = [state_size] + neurons + [action_size]
        activations = [None] + activations + [None]

        # Initialize neural network
        self.__net = nn.Sequential()

        # Iterate over input size of layer, output size, and activation function
        for idx, (input_size, output_size, activation_function) in enumerate(
            zip(neurons[:-1], neurons[1:], activations[1:])
        ):
            # Create linear layer
            self.__net.add_module(f"layer_{idx}", nn.Linear(input_size, output_size))

            # Add activation function if provided
            if activation_function is not None:
                self.__net.add_module(
                    f"activation_{idx}", getattr(nn, activation_function)()
                )

    def forward(self, state):
        return self.__net(state)


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
        self.__net = Net(**config_par["networkParameters"])

    def policy(self, alpha):
        # TODO alpha should be a parameter passed in constructor and saved in self.__alpha or something similar
        return alpha

    def set_state(self, action, reward, next_state):

        transition = (self.state, action, reward, next_state)
        self.__replaybuffer.append(transition)

        return super().set_state(action, reward, next_state)

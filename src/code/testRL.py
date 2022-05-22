from nationRL import NationRL
import gym
from matplotlib import pyplot as plt
from rich.progress import track
import numpy as np

# Create agent

config = {
    "iterations": 400,
    "fixed_migration": True,
    "pop_migration": 0.02,
    "nation_def": "Nation",
    "age_group": True,
    "age_group_summary": True,
    "economy": False,
    "bufferSettings": {"maxSize": 5000, "batchSize": 150, "shuffle_data": True},
    "networkParameters": {
        "gamma": 0.98,
        "device": "cpu",
        "actor": {
            "optim": {"lr": 0.001},
            "net": {
                "state_size": 4,
                "output_size": 2,
                "neurons": [256, 128, 64, 32],
                "activations": "ReLU",
                "out_activation": "ReLU",
                "n_heads": 1,
            },
        },
        "critic": {
            "optim": {"lr": 0.001},
            "net": {
                "state_size": 4,
                "output_size": 1,
                "neurons": [256, 128, 64, 32],
                "activations": "ReLU",
                "out_activation": "Sigmoid",
                "n_heads": 1,
            },
        },
    },
    "updatePeriod": 80,
    "updateN": 500,
    "alpha": 0.2,
}

agent = NationRL(
    config_par=config,
    contact_matrix=None,
    population=None,
    C=None,
    name=None,
    state=None,
    parameters=None,
    cont_param=None,
)

counter_update_period = 0

# Create environment
env = gym.make("CartPole-v1")

# Stats
returns = []

# Training loop
for episode in track(range(1000)):
# for episode in range(100):

    # Initialize state
    state = env.reset()
    agent.state = state

    # Initialize return of episode
    G = 0

    for i in range(config["iterations"]):

        # Get the action the agent would do
        action = np.argmax(agent.policy())

        # Pass action to environment and get new state
        next_state, reward, done, other = env.step(action)

        # Update return
        G += reward

        # Give reward to agent
        agent.set_state(action, reward, next_state)
        state = next_state

        # Update if necessary
        if counter_update_period >= config["updatePeriod"]:
            agent.update(config["updateN"])
            counter_update_period = 0
        else:
            counter_update_period += 1

        if done:
            break

    returns.append(G)

returns = np.array(returns)

plt.plot(returns, label="Raw")
plt.plot(np.cumsum(returns)/(np.arange(returns.shape[0])+1), label="Avg")
plt.legend()
plt.show()

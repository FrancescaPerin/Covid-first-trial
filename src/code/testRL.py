from agentRL import MultinomialAgent
import gym
from matplotlib import pyplot as plt
from rich.progress import track
import numpy as np
import time

# Create agent

TRAIN_EPISODES = 1000
TEST_EPISODES = 20

STATE_SIZE = 4
END_REWARD = None

ENV = "CartPole-v1"
# ENV = "Acrobot-v1"

config = {
    "iterations": 1000,
    "bufferSettings": {"maxSize": 300, "batchSize": 40, "shuffle_data": True},
    "networkParameters": {
        "gamma": 0.99,
        "device": "cpu",
        "actor": {
            "optim": {"lr": 0.001},
            "net": {
                "state_size": STATE_SIZE,
                "output_size": 2,
                "neurons": [128, 32],
                "activations": "LeakyReLU",
                "out_activation": None,
                "n_heads": 1,
            },
        },
        "critic": {
            "optim": {"lr": 0.001},
            "net": {
                "state_size": STATE_SIZE,
                "output_size": 1,
                "neurons": [128, 32],
                "activations": "LeakyReLU",
                "out_activation": None,
                "n_heads": 1,
            },
        },
    },
    "updatePeriod": 10,
    "updateN": 30,
}

agent = MultinomialAgent(
    config_par=config,
    name="agent",
)

counter_update_period = 0

# Create environment
env = gym.make("CartPole-v1")

# Stats
returns = []
actor_loss = []
critic_loss = []

# Training loop
# for episode in range(TRAIN_EPISODES):
for episode in track(range(TRAIN_EPISODES)):

    # Initialize state
    state = env.reset()
    agent.state = state

    # Initialize return of episode
    G = 0

    for i in range(config["iterations"]):

        # Get the action the agent would do
        action = np.argmax(agent.policy())
        # action = np.random.randint(2)

        # Pass action to environment and get new state
        next_state, reward, done, other = env.step(action)

        if done and END_REWARD is not None:
            reward = END_REWARD

        # Update return
        G += reward

        # Give reward to agent
        agent.set_state(action, reward, next_state)
        state = next_state

        # Update if necessary
        if counter_update_period >= config["updatePeriod"]:
            actor_t, critic_t = agent.update(config["updateN"])
            counter_update_period = 0
            actor_loss.append(actor_t)
            critic_loss.append(critic_t)
        else:
            counter_update_period += 1

        if done:
            break

    returns.append(G)

# Plot loss and returns
actor_loss = np.array(actor_loss)
critic_loss = np.array(critic_loss)

returns = np.array(returns)

fig, axs = plt.subplots(2)
axs[0].plot(returns, label="Raw")
axs[0].plot(np.cumsum(returns) / (np.arange(returns.shape[0]) + 1), label="Avg")
axs[0].legend()

axs[1].plot(actor_loss, label="Actor")
axs[1].plot(critic_loss, label="Critic")
axs[1].legend()

plt.show()

# Testing loop
for episode in track(range(TEST_EPISODES)):

    # Initialize state
    state = env.reset()

    for i in range(config["iterations"]):

        # Set agent current state
        agent.state = state

        # Get the action the agent would do
        action = np.argmax(agent.policy())

        # Pass action to environment and get new state
        state, reward, done, other = env.step(action)

        # Render environment
        env.render()

        if done:
            break

    print("END OF EPISODE: ", i)

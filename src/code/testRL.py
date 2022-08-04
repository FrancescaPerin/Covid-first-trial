from agentRL import MultinomialAgent
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
            "optim": {"lr": 0.01},
            "net": {
                "state_size": 4,
                "output_size": 2,
                "neurons": [128],
                "activations": "ReLU",
                "out_activation": "ReLU",
                "n_heads": 1,
            },
        },
        "critic": {
            "optim": {"lr": 0.01},
            "net": {
                "state_size": 4,
                "output_size": 1,
                "neurons": [128],
                "activations": "ReLU",
                "out_activation": None,
                "n_heads": 1,
            },
        },
    },
    "updatePeriod": 30,
    "updateN": 500,
    "alpha": 0.2,
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
actor_loss=[]
critic_loss=[]

# Training loop
for episode in track(range(62)):
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
            actor_t, critic_t = agent.update(config["updateN"])
            counter_update_period = 0
            actor_loss.append(actor_t)
            critic_loss.append(critic_t)
        else:
            counter_update_period += 1
            #actor_loss.append(actor_t)
            #critic_loss.append(critic_t)

        if done:
            break

    returns.append(G)


actor_loss = np.array(actor_loss)
critic_loss = np.array(critic_loss)

print(actor_loss)
print(critic_loss)

returns = np.array(returns)


fig, axs = plt.subplots(2)
axs[0].plot(returns, label="Raw")
axs[0].plot(np.cumsum(returns)/(np.arange(returns.shape[0])+1), label="Avg")
axs[0].legend()

axs[1].plot(actor_loss, label="Actor")
axs[1].plot(critic_loss, label="Critic")
axs[1].legend()

plt.show()




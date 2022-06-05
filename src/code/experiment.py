import argparse
import json
import os
from datetime import datetime
from os.path import join as joinpath

import numpy as np
import torch

from agent import Agent
from nation import Nation
from nationRL import NationRL
from utils import (
    calc_loss_GDP,
    check_file,
    load_contact,
    load_JSON,
    load_pop,
    summary_C,
)

parser = argparse.ArgumentParser(description="Passing arguments to code.")

# SEIARDV values for eache agent (SEAIRDV starting values and simulation parameters)
parser.add_argument(
    "--agent_params",
    type=check_file,
    default="agents_SEAIRD.json",
    help="JSON file with definition of agents parameters",
)

# Topology of simulation (connections between agents)
parser.add_argument(
    "--topology",
    type=check_file,
    default="topology.json",
    help="JSON file with topology definition of model",
)

# Environment and RL parameters
parser.add_argument(
    "--settings",
    type=check_file,
    default="settings.json",
    help="JSON file with settings of outer model",
)

# Contact parameters for contact matrices usage
parser.add_argument(
    "--cont_params",
    type=check_file,
    default="contact_settings.json",
    help="JSON file with settings of outer model",
)
# GDP/ economy parameters
parser.add_argument(
    "--economy_params",
    type=check_file,
    default="economy_settings.json",
    help="JSON file with settings of outer model",
)

args = parser.parse_args()

# Loading agents from JSON file
data_agents = load_JSON("../json/" + args.agent_params)

# Loading topology from JSON file
connections = load_JSON("../json/" + args.topology)

# Loading environment and RL settings from JSON file
settings = load_JSON("../json/" + args.settings)

# Loading contact matrices settings from JSON file
cont_params = np.asarray(list(load_JSON("../json/" + args.cont_params).values()))

# Loading economy settings from JSON file
economy_params = load_JSON("../json/" + args.cont_params)

# Saving dictionary containing Agent objects
agents = {}

# if age group is used state size of the network needs to be changed despite any other parameter
if settings["age_group"]:
    settings["networkParameters"]["actor"]["net"]["state_size"] = 24
    settings["networkParameters"]["critic"]["net"]["state_size"] = 24

for agent in data_agents:

    alpha = 1

    # Loading contact matrix of agent
    cont_matrix = load_contact(agent["name"])

    # Loading population of agent
    population = load_pop(agent["name"], settings["age_group"])

    # if population is divided in age groups
    if settings["age_group"] == True:

        # calculate population percentage in each age group
        pop_perc = population / population.sum()

        for key, value in agent["state"].items():

            # readjust SEIARDV values to account for splitting in age groups
            agent["state"][key] = pop_perc * value

        # Initialize final contact matrix
        C = summary_C(cont_matrix, cont_params, alpha)

    else:
        # Initialize final contact matrix
        C = np.array(alpha)

    # Define agent
    agent_obj = Nation(settings, cont_matrix, cont_params, population, C, **agent)

    agents[agent_obj.name] = agent_obj

# Initiate loss with 0 values
loss = np.zeros((len(agents), 2))

for i in range(settings["iterations"]):

    # Act in the environment
    for agent in agents:

        # Calculate new alpha trough policy
        alpha = agents[agent].policy()

        if settings["age_group"] == False:

            # Recompute C according to new alpha

            agents[agent] = agents[agent].update_C(
                np.array(alpha)
            )  # TODO: should also use summary_C to recompute

        else:
            # Recompute C according to new alpha and update it
            C = summary_C(cont_matrix, cont_params, alpha)

            agents[agent] = agents[agent].update_C(C)

        if settings["fixed_migration"]:

            # if migration value is fixed use settings value for all agents
            agents[agent].interact(
                [agents.get(key) for key in connections[agent]],
                settings["pop_migration"],
            )

        else:
            # otherwise load aviation data
            avia_data = load_JSON("../../data/Aviation/json_data.json")

            # interaction is based on agent aviation data (not fixed)
            agents[agent].interact(
                [agents.get(key) for key in connections[agent]], avia_data[agent]
            )

    for agent in agents:

        reward = agents[agent].state.D * agents[agent].state.loss

        agents[agent].set_state(alpha, reward, agents[agent].next_state(i))

        # Train agents
    if i != 0 and i % settings["updatePeriod"] == 0:

        for agent in agents:
            # Update agents
            agents[agent].update(n=settings["updateN"])


# Save data

results_path = datetime.now().strftime("%Y_%b_%d_%H_%M_%S")
final_results_path = joinpath("../../results", results_path)

if not os.path.isdir(final_results_path):
    os.makedirs(final_results_path)

# settings
with open(joinpath(final_results_path, "settings.json"), "wt") as f:
    json.dump(settings, f)

with open(joinpath(final_results_path, "cont_params.json"), "wt") as f:
    json.dump(args.cont_params, f)

with open(joinpath(final_results_path, "economy_params.json"), "wt") as f:
    json.dump(economy_params, f)

with open(joinpath(final_results_path, "agent_params.json"), "wt") as f:
    json.dump(args.agent_params, f)

# agents
torch.save(agents, joinpath(final_results_path, "agents.pth"))

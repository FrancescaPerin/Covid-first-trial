import argparse
import json
import os
from datetime import datetime
from os.path import join as joinpath

import numpy as np
import torch
from rich.progress import track

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
    summary_C_1D,
    reward_function,
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

parser.add_argument(
    "--agent_type",
    type=str,
    choices=["Nation", "NationRL"],
    default="Nation",
    help="Agent class to be used in experiment",
)

parser.add_argument(
    "--debug",
    default=False,
    action="store_true",
    help="Set to true to run debug mode",
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

# Load aviation data
avia_data = load_JSON("../../data/Aviation/json_data.json")

# Saving dictionary containing Agent objects
agents = {}

# if age group is used state size of the network needs to be changed despite any other parameter
if settings["age_group"]:
    settings["networkParameters"]["actor"]["net"][
        "state_size"
    ] = 21  # SEAIRDV x 3 age groups
    settings["networkParameters"]["critic"]["net"]["state_size"] = 21
else:
    settings["networkParameters"]["actor"]["net"]["state_size"] = 7
    settings["networkParameters"]["critic"]["net"]["state_size"] = 7

# Initialize agents
for agent in (
    track(data_agents, description="Initializing agents")
    if not args.debug
    else data_agents
):

    alpha = 0.0

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
        # Initialize final contact matrix (use adult compliance)
        C = summary_C_1D(cont_params, alpha)

    # Define agent
    NationClass = eval(args.agent_type)
    agent_obj = NationClass(settings, cont_matrix, cont_params, population, C, **agent)

    agents[agent_obj.name] = agent_obj

# Normalize aviation data
for agent_name, agent in agents.items():
    for travel_data in avia_data[agent_name].values():
        for travel_type, val in travel_data.items():
            travel_data[travel_type] = (val / 365) / agent.state.N.sum()

# Initiate loss with 0 values
loss = np.zeros((len(agents), 2))

for i in (
    track(range(settings["iterations"]), description="Running simulation")
    if not args.debug
    else range(settings["iterations"])
):

    if args.debug:
        print(f"Iteration: {i}")

    # Create dictionary sto store alphas
    alphas = {agent: agents[agent].policy() for agent in agents}

    # Act in the environment

    # Update C matrices for each agent
    if args.debug:
        print("Updating contact matrices")
    for agent in agents:

        if not settings["age_group"]:
            # Recompute C according to new alpha
            C = summary_C_1D(cont_params, alphas[agent])
        else:
            # Recompute C according to new alpha and update it
            C = summary_C(cont_matrix, cont_params, alphas[agent])

        agents[agent].update_C(C)

    # Immigrate/emigrate between each country
    if args.debug:
        print("Interaction between agents")
    for agent in agents:

        # interaction is based on agent aviation data (not fixed)
        agents[agent].interact(
            alphas[agent],
            [agents.get(key) for key in connections[agent]],
            settings["pop_migration"]
            if settings["fixed_migration"]
            else avia_data[agent],
        )

    # Set transition in environment (and compute reward) for each agent
    if args.debug:
        print("Updating buffer for agents")
    for agent in agents:
        agents[agent].set_state(
            alphas[agent], reward_function(agents[agent]), agents[agent].next_state(i)
        )

    # Train agents
    if i != 0 and i % settings["updatePeriod"] == 0:

        if args.debug:
            print("Updating agent policies")

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

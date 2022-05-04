import numpy as np
import json
import argparse
import os

from nationRL import NationRL
from nation import Nation
from agent import Agent

from utils import (
    check_file,
    load_JSON,
    load_contact,
    load_pop,
    summary_C,
    calc_loss_GDP,
)
from plots import (
    plot_age_compartment_comparison,
    plot_compartment_comparison,
    plot_loss_GDP,
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
data_agents = load_JSON(args.agent_params)

# Loading topology from JSON file
connections = load_JSON(args.topology)

# Loading environment and RL settings from JSON file
settings = load_JSON(args.settings)

# Loading contact matrices settings from JSON file
cont_params = np.asarray(list(load_JSON(args.cont_params).values()))

# Loading economy settings from JSON file
economy_params = load_JSON(args.cont_params)

# Saving dictionary containing Agent objects
agents = {}

for agent in data_agents:

    alpha = 0.2

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

        # Initialize contact matrix
        C = summary_C(cont_matrix, cont_params, alpha)
    
    else: 
        # Initialize contact matrix
        C = np.array(1 - alpha)

    # Define agent 
    agent_obj = Nation(settings, cont_matrix, cont_params, population, C, **agent)

    agents[agent_obj.name] = agent_obj

#Initiate loss with 0 values
loss = np.zeros((len(agents), 2))

for i in range(settings["iterations"]):

    # Act in the environment
    for agent in agents:

        # Calculate new alpha trough policy
        alpha = agents[agent].policy()

        if settings["age_group"] == False:

            #Recompute C according to new alpha

            agents[agent] = agents[agent].update_C(np.array(1 - alpha)) #TODO: should also use summary_C to recompute

        else:
            #Recompute C according to new alpha and update it 
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
            avia_data = load_JSON("Aviation/json_data.json")

            # interaction is based on agent aviation data (not fixed)
            agents[agent].interact(
                [agents.get(key) for key in connections[agent]], avia_data[agent]
            )

            # Set new state for agents
    for agent in agents:

        reward = 0

        agents[agent].set_state(alpha, reward, agents[agent].next_state(i))

        # Train agents
    if i != 0 and i % settings["updatePeriod"] == 0:

        for agent in agents:
            # Update agents
            agents[agent].update(n=settings["updateN"])


#Plotting based on verious settings

if settings["age_group"] == True:

    if settings["economy"] == True:

        plot_loss_GDP(agents)

    plot_age_compartment_comparison(
        agents, 0, "Susceptible", settings["age_group_summary"]
    )
    plot_age_compartment_comparison(agents, 1, "Exposed", settings["age_group_summary"])
    plot_age_compartment_comparison(
        agents, 3, "Infected", settings["age_group_summary"]
    )
    plot_age_compartment_comparison(
        agents, 4, "Recovered", settings["age_group_summary"]
    )

else:

    if settings["economy"] == True:

        plot_loss_GDP(agents)

    plot_compartment_comparison(agents, 0, "Susceptible")
    plot_compartment_comparison(agents, 1, "Exposed")
    plot_compartment_comparison(agents, 3, "Infected")

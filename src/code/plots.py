import numpy as np
import math
import os
from os.path import join as joinpath
from matplotlib import pyplot as plt
from collections import defaultdict
from itertools import groupby


def plot_age_compartment_comparison(
    experiments, idx, comp_name, summary=False, sub_dir=".", show=False, group_vals=None
):

    # Either don't give group values or give one value of each experiment (dictionary of agents)
    assert group_vals is None or len(group_vals) == len(experiments)

    # If no grouping is given, create a single "fake" group with parameter value `0`
    if group_vals is None:
        groups = {0: experiments}
    else:

        # Sort by value
        sorted_pairs = sorted(zip(experiments, group_vals), key=lambda x: x[1])

        # Group by value
        groups = {
            par_val : [x[0] for x in group_experiments]
            for par_val, group_experiments in groupby(sorted_pairs, key=lambda x: x[1])
        }

    plt.rcParams["figure.figsize"] = (15, 9)
    fig, axs = plt.subplots(
        len(experiments[0]), 1
    )  # get the number of agents from the first experiment
    fig.subplots_adjust(hspace=0.5, wspace=0.001)

    fig.suptitle(f"{comp_name} comparison for agents")

    axs = axs.ravel()

    agent_names = list(
        experiments[0].keys()
    )  # get the key order from the first experiment

    # Plot desired compartment
    for group_val, group in groups.items():

        # Compute average history per agent

        for i, agent_name in enumerate(agent_names):

            # Average histories accross experiments for agents with the same name
            history = np.mean(
                [agents[agent_name].history[:, 1:, :] for agents in group], axis=0
            )

            arr_filter = history[:, idx:, :] > 0.001

            axs[i].plot(
                history[:, idx, 0],
                label=f"Child {'' if group_vals is None else group_val}",
            )  # child

            axs[i].plot(
                history[:, idx, 1],
                label=f"Adult {'' if group_vals is None else group_val}",
            )  # adult

            axs[i].plot(
                history[:, idx, 2],
                label=f"Senior {'' if group_vals is None else group_val}",
            )  # senior

            if summary:
                axs[i].plot(
                    np.sum(history[:, idx, :], axis=1),
                    label=f"Total {'' if group_vals is None else group_val}",
                )

            axs[i].set_ylabel("Population fraction")
            axs[i].set_xlabel("Time (days)")
            axs[i].set_title(agent_name)
            axs[i].legend()

    # Add information
    final_path = joinpath("../../results", sub_dir, "age_group")
    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(joinpath(final_path, f"{comp_name}_comparison.png"))

    if show:
        plt.show()


def plot_compartment_comparison(experiments, idx, comp_name, sub_dir=".", show=False, group_vals=None):

    # Either don't give group values or give one value of each experiment (dictionary of agents)
    assert group_vals is None or len(group_vals) == len(experiments)

    # If no grouping is given, create a single "fake" group with parameter value `0`
    if group_vals is None:

        groups = {0: experiments}
    else:

        # Sort by value
        sorted_pairs = sorted(zip(experiments, group_vals), key=lambda x: x[1])

        # Group by value
        groups = {
            par_val : [x[0] for x in group_experiments]
            for par_val, group_experiments in groupby(sorted_pairs, key=lambda x: x[1])
        }


    plt.rcParams["figure.figsize"] = (15, 5)

    agent_names = list(
        experiments[0].keys()
    ) 

    # Plot desired compartment
    for group_val, group in groups.items():

        # Compute average history per agent
        for agent_name in agent_names:

            # Average histories accross experiments for agents with the same name

            history = np.array([agents[agent_name].history[:, 1:] for agents in group], dtype=np.float64)

            history_mean = np.mean(
                    history, axis=0
                )
            history_std = np.std(
                    history, axis=0
                )

            #print(std.shape)
            history_se = history_std/math.sqrt(history_std.shape[0])

            # arr_filter = history[:, idx:] > 0.001

            sel_mean = np.squeeze(np.asarray(history_mean[:, 1:])[:, idx])
            sel_se = np.squeeze(np.asarray(history_se[:, 1:])[:, idx])

            plt.plot(sel_mean,
                label=f"{agent_name} {'' if group_vals is None else group_val}"
                )

            #print((sel_history - (2 * se[idx])))
            plt.fill_between(range(len(sel_mean)), sel_mean - 2*sel_se, sel_mean + 2*sel_se)

    # Add information
    plt.legend()
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.title(f"{comp_name} comparison for agents")

    final_path = joinpath("../../results", sub_dir, "no_age_group")
    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(joinpath(final_path, f"{comp_name}_comparison.png"))

    if show:
        plt.show()

def plot_loss_GDP(agents, sub_dir=".", show=False):

    plt.rcParams["figure.figsize"] = (15, 5)

    # Plot desired compartment
    for curr_agent in agents.values():
        plt.plot(curr_agent.history[:, -1])

    # Add information
    plt.legend([agent for agent in agents])
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.title(f"Loss comparison for agents")

    final_path = joinpath("../../results", sub_dir)

    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(joinpath(final_path, "loss_comparison.png"))

    if show:
        plt.show()

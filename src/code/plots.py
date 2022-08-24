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

    age_groups = ["Child", "Adult", "Senior"]
    plt.rcParams["figure.figsize"] = (18, 9)

    n_plots= len(age_groups)+1 if summary is True else len(age_groups)

    fig, axs = plt.subplots(n_plots, 1)  # get the number of agents from the first experiment

    fig.subplots_adjust(hspace=0.5, wspace=0.001)

    fig.suptitle(f"{comp_name} comparison for agents")

    axs = axs.ravel()

    age_groups = ["Child", "Adult", "Senior"]

    agent_names = list(
        experiments[0].keys()
    )  # get the key order from the first experiment

    # Plot desired compartment
    for group_val, group in groups.items():

        # Compute average history per agent

        for i, agent_name in enumerate(agent_names):

            # Average histories accross experiments for agents with the same name
            history = np.asarray(
                [agents[agent_name].history[:, 1:, :] for agents in group], dtype=np.float64
            )

            history_mean = np.mean(
                    history, axis=0
                )

            history_std = np.std(
                    history, axis=0
                )

            history_se = history_std/math.sqrt(history_std.shape[0])


            sel_mean = np.asarray(history_mean[:, idx, :])
            sel_se = np.asarray(history_se[:, idx, :])

            #arr_filter = history[:, idx:, :] > 0.001

            for j, name in enumerate(["Child", "Adult", "Senior"]):

                axs[j].plot(
                    sel_mean[:,j],
                    label=f"{agent_name} {'' if group_vals is None else group_val}",
                )  # child

                axs[j].fill_between(range(len(sel_mean)), 
                    sel_mean[:, j] - 2*sel_se[:, j], 
                    sel_mean[:, j] + 2*sel_se[:, j],
                    alpha=0.5
                )
                axs[j].set_ylabel("Population fraction")
                axs[j].set_title(age_groups[j])
   
            
            if summary:
                axs[len(age_groups)].plot(
                    np.sum(history_mean[:, idx, :], axis=1),
                    label=f"Total {'' if group_vals is None else group_val}",
                )

                axs[len(age_groups)].fill_between(range(len(history_mean)), 
                    np.sum(history_mean[:, idx, :], axis=1) - 2*np.sum(history_se[:, idx, :], axis=1), 
                    np.sum(history_mean[:, idx, :], axis=1) + 2*np.sum(history_se[:, idx, :], axis=1),
                    alpha=0.5
                )
                axs[len(age_groups)].set_ylabel("Population fraction")
                axs[len(age_groups)].set_title("Total")
                
        axs[n_plots-1].set_xlabel("Time (days)")
        axs[0].legend(loc='upper right', bbox_to_anchor=(1.27, 0.5))

        plt.subplots_adjust(right=0.80)
        plt.setp(axs, xlim=(0,history.shape[1]))

        plt.show()

        quit()



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

            history_se = history_std/math.sqrt(history_std.shape[0])

            # arr_filter = history[:, idx:] > 0.001

            sel_mean = np.squeeze(np.asarray(history_mean[:, 1:])[:, idx])
            sel_se = np.squeeze(np.asarray(history_se[:, 1:])[:, idx])

            plt.plot(sel_mean,
                label=f"{agent_name} {'' if group_vals is None else group_val}"
                )

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

def plot_alphas(experiments, alphas, sub_dir=".", show=False, group_vals=None):

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

    agent_names = list(
        experiments[0].keys()
    )

    
    plt.rcParams["figure.figsize"] = (15, 10)

    fig, axs = plt.subplots(int(len(alphas[0].keys())+1/2), 2)  # get the number of agents from the first experiment

    fig.subplots_adjust(hspace=0.6, wspace=0.4)

    fig.suptitle(f"Alpha comparison for country over time")

    axs = axs.ravel()

    # Plot desired compartment
    for group_val, group in groups.items():

        # Compute average history per agent
        for i, agent_name in enumerate(agent_names):

            history_temp = np.array([i for i in list(map(lambda x: [x[agent_name]], alphas))], dtype=np.float64)

            history = history_temp.reshape(history_temp.shape[1], history_temp.shape[0])

            history.reshape(1, len(alphas))

            history_mean = np.mean(
                    history, axis=0
                )
            history_std = np.std(
                    history, axis=0
                )

            history_se = history_std/math.sqrt(history_std.shape[0])


            sel_mean = np.squeeze(np.asarray(history_mean[:]))
            sel_se = np.squeeze(np.asarray(history_se[:]))


            ncols = 2
            # calculate number of rows
            nrows = len(alphas[0].keys()) // ncols + (len(alphas[0].keys()) % ncols > 0)

            ax = plt.subplot(nrows, ncols, i + 1)

            ax.plot(sel_mean,
                label=f"{agent_name} {'' if group_vals is None else group_val}"
                )

            ax.fill_between(range(len(sel_mean)), sel_mean - 2*sel_se, sel_mean + 2*sel_se)

            ax.set_ylim([-0.1,1.1])
    # Add information
    plt.legend()
    plt.ylabel("Value of state imposed closure")
    plt.xlabel("Time (days)")
    plt.title(f"State imposed closure values across time")

    final_path = joinpath("../../results", sub_dir)

    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(joinpath(final_path, "aplhas_comparison.png"))

    if show:
        plt.show()



def plot_loss_GDP(experiments, sub_dir=".", show=False, group_vals=None):

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

    agent_names = list(
        experiments[0].keys()
    )

    plt.rcParams["figure.figsize"] = (15, 5)

    # Plot desired compartment
    for group_val, group in groups.items():

        # Compute average history per agent
        for agent_name in agent_names:

            history = np.array([agents[agent_name].history[:, -1] for agents in group], dtype=np.float64)

            history_mean = np.mean(
                    history, axis=0
                )
            history_std = np.std(
                    history, axis=0
                )

            history_se = history_std/math.sqrt(history_std.shape[0])

            # arr_filter = history[:, idx:] > 0.001

            #TODO: why do we take the GDP loss of last age group only?
            sel_mean = np.squeeze(np.asarray(history_mean[:, -1]))
            sel_se = np.squeeze(np.asarray(history_se[:, -1]))

            plt.plot(sel_mean,
                label=f"{agent_name} {'' if group_vals is None else group_val}"
                )

            plt.fill_between(range(len(sel_mean)), sel_mean - 2*sel_se, sel_mean + 2*sel_se)


    # Add information
    plt.legend()
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.title(f"Loss comparison for agents")

    final_path = joinpath("../../results", sub_dir)

    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(joinpath(final_path, "loss_comparison.png"))

    if show:
        plt.show()

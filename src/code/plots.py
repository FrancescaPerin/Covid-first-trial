import numpy as np
import os
from matplotlib import pyplot as plt


def plot_age_compartment_comparison(agents, idx, comp_name, summary=False):

    plt.rcParams["figure.figsize"] = (15, 9)
    fig, axs = plt.subplots(len(agents), 1)
    fig.subplots_adjust(hspace=0.5, wspace=0.001)

    fig.suptitle(f"{comp_name} comparison for agents")

    axs = axs.ravel()

    # Plot desired compartment
    for i, curr_agent in enumerate(agents):

        arr_filter = (
            np.asarray(agents[curr_agent].history[:, 1:, :])[:, idx:, :] > 0.001
        )

        axs[i].plot(agents[curr_agent].history[:, 1:, :][:, idx, 0])  # child

        axs[i].plot(agents[curr_agent].history[:, 1:, :][:, idx, 1])  # adult

        axs[i].plot(agents[curr_agent].history[:, 1:, :][:, idx, 2])  # senior

        if summary == True:

            # print (np.sum(agents[curr_agent].history[:,1:,:][:,idx, :], axis = 1))

            axs[i].plot(np.sum(agents[curr_agent].history[:, 1:, :][:, idx, :], axis=1))
            axs[i].legend(["Child", "Adult", "Senior", "Total"])
        else:

            axs[i].legend(["Child", "Adult", "Senior"])

        axs[i].set_ylabel("Population fraction")
        axs[i].set_xlabel("Time (days)")
        axs[i].set_title(agents[curr_agent].name)

    # Add information
    final_path = "../../results/age_group/"
    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(f"../../results/age_group/{comp_name}_comparison.png")
    plt.show()


def plot_compartment_comparison(agents, idx, comp_name):

    plt.rcParams["figure.figsize"] = (15, 5)

    # Plot desired compartment
    for curr_agent in agents:

        arr_filter = np.asarray(agents[curr_agent].history[:, 1:])[:, idx] > 0.001

        plt.plot(np.asarray(agents[curr_agent].history[:, 1:])[:, idx])

    # Add information
    plt.legend([agent for agent in agents])
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.title(f"{comp_name} comparison for agents")

    final_path = "../../results/no_age_group/"
    if not os.path.isdir(final_path):
        os.makedirs(final_path)

    plt.savefig(f"../../results/no_age_group/{comp_name}_comparison.png")
    plt.show()


def plot_loss_GDP(agents):

    plt.rcParams["figure.figsize"] = (15, 5)

    # Plot desired compartment
    for curr_agent in agents:

        plt.plot(agents[curr_agent].history[:, -1])

    # Add information
    plt.legend([agent for agent in agents])
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.title(f"Loss comparison for agents")
    plt.savefig(f"../../results//loss_comparison.png")
    plt.show()

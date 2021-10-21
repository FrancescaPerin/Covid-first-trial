import numpy as np
from matplotlib import pyplot as plt

def plot_compartment_comparison(agents, idx, comp_name):
    # Plot desired compartment
    for curr_agent in agents:

        arr_filter = np.asarray(agents[curr_agent].history)[:, idx] > 0.001

        plt.plot(agents[curr_agent].history[arr_filter, idx])

    # Add information
    plt.title(f"{comp_name} comparison for agents")
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.legend([agent for agent in agents])
    plt.savefig(f"results/{comp_name}_comparison.png")
    plt.show()

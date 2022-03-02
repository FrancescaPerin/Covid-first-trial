import numpy as np
from matplotlib import pyplot as plt

def plot_age_compartment_comparison(agents, idx, comp_name):
    
    fig, axs = plt.subplots(len(agents),1)
    fig.subplots_adjust(hspace = .5, wspace=.001)

    fig.suptitle(f"{comp_name} comparison for agents")

    axs = axs.ravel()

    # Plot desired compartment
    for i, curr_agent in enumerate(agents):

        print(f'{curr_agent}--{agents[curr_agent].population}')

        arr_filter = np.asarray(agents[curr_agent].history[:,1:,:])[:,idx:, :] > 0.001

        axs[i].plot(agents[curr_agent].history[:,1:,:][:,idx, 0])
        
        axs[i].plot(agents[curr_agent].history[:,1:,:][:,idx, 1])
        
        axs[i].plot(agents[curr_agent].history[:,1:,:][:,idx, 2])

        axs[i].legend(['c','a','s'])
        axs[i].set_ylabel("Population fraction")
        axs[i].set_xlabel("Time (days)")
        axs[i].set_title(agents[curr_agent].name)

    # Add information
    plt.savefig(f"results/{comp_name}_comparison.png")
    plt.show()


def plot_compartment_comparison(agents, idx, comp_name):
    

    # Plot desired compartment
    for curr_agent in agents:

        #print(np.asarray(agents[curr_agent].history[:,1:])[:, idx])

        arr_filter = np.asarray(agents[curr_agent].history[:,1:])[:, idx] > 0.001

        plt.plot(np.asarray(agents[curr_agent].history[:,1:])[:, idx])
        

    # Add information
    plt.legend([agent for agent in agents])
    plt.ylabel("Population fraction")
    plt.xlabel("Time (days)")
    plt.title(f"{comp_name} comparison for agents")
    plt.savefig(f"results/{comp_name}_comparison.png")
    plt.show()

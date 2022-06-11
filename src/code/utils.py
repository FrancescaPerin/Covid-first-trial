import json
import numpy as np
import os
import pandas as pd

from sys import exit

from contact_m import contactMatrix


def check_file(file_name):

    if not isinstance(file_name, str):
        raise TypeError("File name not a string")

    elif file_name.endswith(".json"):
        return file_name

    else:
        return file_name + ".json"


def load_JSON(file_name):

    with open(file_name, "rt") as agents_json:
        return json.load(agents_json)


def load_contact(country):

    path = "../../data/Contact_matrices/new_matrices_152_countries"

    name = "age_matrix.npy"

    home = norm_home(country, os.path.join(path, "home", country, name))
    work = np.load(os.path.join(path, "work", country, name))
    school = np.load(os.path.join(path, "school", country, name))
    other = np.load(os.path.join(path, "other_locations", country, name))
    env = np.load(os.path.join(path, "environment", country, name))
    all_l = np.load(os.path.join(path, "all_locations", country, name))

    return contactMatrix(country, home, work, school, other, env, all_l)


def load_pop(country, age_group=False):

    path = "../../data/Population_group/Population_tables"

    name = "population_table.npy"

    pop = np.load(os.path.join(path, country, name), allow_pickle=True)

    df = pd.DataFrame(
        pop, columns=["Country", "Group", "2016", "2017", "2018", "2019", "2020"]
    )
    df = df.replace("..", np.nan)  # remplace emty cells with NaN values

    empty_row = 0

    for index, row in df.iterrows():

        assert (
            empty_row <= 2
        ), f"No data for {country}. Select different country."  # not enough data present for population according to age

        if row.count() < 3:
            empty_row += 1

    return df["2020"].to_numpy()[:3] if age_group else df["2020"].to_numpy()[-1]


def norm_home(country, path):

    hh_path = "../../data/Population_group/Household_data/Tables"

    home = np.load(path)

    hh_table = pd.DataFrame(
        np.load(os.path.join(hh_path, country, "avg_table.npy"), allow_pickle=True)
    )

    if len(hh_table.columns) > 2:

        sum_home_hh = np.divide(home, hh_table.to_numpy()[0][2:].reshape(3, 1))

    else:

        avg = hh_table.to_numpy()[0][1]

        arr = np.repeat(
            avg / 3, 3
        )  # child, adult, senior, distributed equally across households (Assumption)

        sum_home_hh = np.divide(home, arr.reshape(3, 1))

    return sum_home_hh


def summary_C(contact_matrix, cont_params, alpha):

    # TODO check using single cont_params for all k

    p = cont_params * alpha

    X = np.diag(1 - p)

    C = contact_matrix.home

    for k in ["school", "work", "other"]:

        m_i = getattr(contact_matrix, k)
        C = C + X @ (m_i @ X)

    C_env = X @ contact_matrix.env

    return C, C_env, np.diag(X)


def summary_C_1D(cont_params, alpha):

    X = 1 - (np.array([alpha]) * cont_params[1])

    C = X
    # TODO modify this if using multiple cont_params for different environment
    C_env = C

    return C, C_env, X


def calc_loss_GDP(agent, t, r=0.0001, sigma=2, teta=0.33, a=18000, alpha=1):

    loss = np.exp(-r * t) * (V(P(agent)) + a * agent.state.D)

    return loss


def G(alpha=0.2, teta=0.5):

    return (alpha) ** teta


def P(agent, alpha=0.2, teta=0.33):

    P = G(alpha, teta) * (agent.state.S + agent.state.E + agent.state.A + agent.state.R)

    return P


def V(P, sigma=2):

    V = -((P ** (1 - sigma) - 1) / (1 - sigma))

    return V


# Add normally ditributed noise to aviation migration mean
def add_noise(mean, percentage_std):

    if isinstance(mean, float):

        return float(mean + np.random.normal(scale=percentage_std * mean, size=1))

    else:

        pop_perc = mean / mean.sum()

        noise = np.random.normal(scale=percentage_std * mean.sum(), size=1)

    return mean + pop_perc * noise

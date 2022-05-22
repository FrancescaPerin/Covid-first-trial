import numpy as np
import pandas as pd
import os
import json


def load_population(file_name):

    matrix = pd.read_excel(io=file_name)

    return matrix


def country_list(population, save_json=False):

    countries = population["Country Name"].unique()

    if save_json:
        with open("list_countries.json", "w") as f:
            json.dump(countries.tolist(), f)

    return countries


def load_json(file_name):
    with open(file_name) as json_file:
        file = json.load(json_file)

    return file


def summary_table(table):

    df = pd.DataFrame(table)

    col = [
        "Reference date (dd/mm/yyyy)",
        "Average household size (number of members)",
        "Under age 15 years among all households",
        "Ages 20-64 years among all households",
    ]

    df = df[col].replace("..", np.nan)  # remplace emty cells with NaN values

    df["Over 65 years among all households"] = df[col[1]] - df[col[2]] - df[col[3]]

    selected_rows = df[~df.isnull().any(axis=1)]

    last_census = selected_rows["Reference date (dd/mm/yyyy)"].max()

    result = selected_rows[selected_rows["Reference date (dd/mm/yyyy)"] == last_census]

    if result.empty:

        one_val = df[
            [
                "Reference date (dd/mm/yyyy)",
                "Average household size (number of members)",
            ]
        ]

        sel_one_val = one_val[~one_val.isnull().any(axis=1)]
        last_sel = sel_one_val["Reference date (dd/mm/yyyy)"].max()

        result_2 = sel_one_val[sel_one_val["Reference date (dd/mm/yyyy)"] == last_sel]

        if len(result_2.index) > 1:

            avg = result_2["Average household size (number of members)"].mean()

            result_2 = pd.DataFrame(
                {
                    "Reference date (dd/mm/yyyy)": [last_sel],
                    "Average household size (number of members)": [avg],
                }
            )

        return result_2

    else:

        return result

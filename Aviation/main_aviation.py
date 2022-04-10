import json
import numpy as np
import os
import pandas as pd

from sys import exit

avia_data = "Data/avia_paincc_2015-2021.xlsx"
df = pd.read_excel(avia_data, sheet_name="Sheet 1", header=None)

df.drop(df.head(10).index, inplace=True)  # drop unwanted info
df.drop(df.tail(3).index, inplace=True)  # drop unwanted info

years = list(
    np.concatenate(
        [([i] * 3) for i in ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]],
        axis=0,
    )
)

columns = ["Geo", "Partner"] + years
df.columns = columns  # making header with location and year

df.replace(":", np.nan, inplace=True)  # replacing invalid characters

df.replace(
    "Germany (until 1990 former territory of the FRG)", "Germany", inplace=True
)  # replacing invalid characters


df.dropna(
    thresh=df.shape[1] - 20, axis=0, inplace=True
)  # remove empty lines corresponding to same country pairing

df.reset_index(drop=True, inplace=True)

countries = df["Geo"].unique()


summary_dict = {}
for geo in countries:

    summary_dict[geo] = {}

    for partner in countries:

        if geo != partner:

            df_paired = df[(df["Geo"] == geo) & (df["Partner"] == partner)]

            avg_on_board = (
                df_paired.iloc[:, 2:15:3].mean(axis=1).item()
            )  # take data from 2015 to 2018 only
            avg_arrivals = df_paired.iloc[:, 3:15:3].mean(axis=1).item()
            avg_departures = df_paired.iloc[:, 4:15:3].mean(axis=1).item()

            summary_dict[geo][partner] = {
                "on_board": avg_on_board,
                "arrivals": avg_arrivals,
                "departures": avg_departures,
            }


with open("countries.json", "w") as outfile:  # save json with countries available
    json.dump(list(countries), outfile)

with open("json_data.json", "w") as outfile:  # save json with all data pre-averaged
    json.dump(summary_dict, outfile, indent=4)

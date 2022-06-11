import numpy as np
import pandas as pd
import json
import os

from pandas import ExcelWriter


def merge_xlsx(file_list):

    with ExcelWriter(file_list[0][:-7] + ".xlsx") as writer:

        data = pd.DataFrame()

        for file in file_list:

            countries = pd.ExcelFile(file).sheet_names

            for country in countries:

                if file == file_list[1]:
                    col_list = [
                        "X1",
                        "X2",
                        "X3",
                        "X4",
                        "X5",
                        "X6",
                        "X7",
                        "X8",
                        "X9",
                        "X10",
                        "X11",
                        "X12",
                        "X13",
                        "X14",
                        "X15",
                        "X16",
                    ]
                    converters = {col: str for col in col_list}
                    data = pd.read_excel(
                        file,
                        sheet_name=country,
                        names=col_list,
                        header=None,
                        index_col=0,
                    )
                    # data.reset_index(drop=True,inplace=True)
                else:
                    data = pd.read_excel(file, sheet_name=country, index_col=0)
                    # data.reset_index(drop=True,inplace=True)

                data.to_excel(writer, sheet_name=country)

        writer.save()


def load_matrix_xlsx(file_name, sheet):

    matrix = pd.read_excel(io=file_name, sheet_name=sheet)

    return matrix


def save_list_json(countries, file_name="countries.json", save_json=False):

    if save_json:
        with open(file_name, "w") as f:
            json.dump(countries, f)


def list_countries(file_name):

    countries = pd.ExcelFile(file_name)

    return countries.sheet_names


def remove_countries(list_c, countries):

    for country in countries:

        list_c.remove(country)

    return list_c


def age_to_group(age_matrix):

    temporary_matrix = pd.DataFrame(
        {
            "c": age_matrix.iloc[:, 0:4].sum(axis=1),  # 0 to 14
            "a": age_matrix.iloc[:, 4:13].sum(axis=1),  # 15 to 64
            "s": age_matrix.iloc[:, 13:16].sum(axis=1),  # 65 to 80
        }
    )

    group_matrix = pd.DataFrame(
        {
            "c": temporary_matrix.iloc[0:4, :].mean(axis=0),
            "a": temporary_matrix.iloc[4:13, :].mean(axis=0),
            "s": temporary_matrix.iloc[13:16, :].mean(axis=0),
        }
    ).T

    return group_matrix


def reformat_all_matrices(countries, location, path, parent_dir):

    for country in countries:

        if location == "environment":

            true_location = "all_locations"
        else:
            true_location = location

        new_path = os.path.join(parent_dir, location, country)

        os.makedirs(new_path, exist_ok=True)

        age_matrix = load_matrix_xlsx(path + true_location + ".xlsx", country)

        group_matrix = age_to_group(age_matrix).to_numpy()

        # temp_max=np.amax(group_matrix)
        # temp_min=np.amin(group_matrix)

        if location == "environment":

            env_matrix = group_matrix / 6

            np.save(new_path + "/age_matrix", env_matrix)

            # temp_max=np.amax(env_matrix)
            # temp_min=np.amin(env_matrix)
        else:
            np.save(new_path + "/age_matrix", group_matrix)

    print("Done")

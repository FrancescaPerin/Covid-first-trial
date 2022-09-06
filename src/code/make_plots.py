import json
import numpy as np
from argparse import ArgumentParser
from os.path import join as joinpath
from os.path import relpath

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import torch

import seaborn as sns

from plots import (
    plot_age_compartment_comparison,
    plot_compartment_comparison,
    plot_loss_GDP,
    plot_alphas,
)


def all_plots(settings, agents, alphas, total_group, output_dir, show, values=None):

    colors = sns.color_palette("hls", 13)
    line_style = ['-', ':']

    plot_alphas(agents, alphas, colors, line_style, output_dir, show, group_vals=None)

    #if settings["economy"] == True:

    plot_loss_GDP(agents, colors, line_style, sub_dir=output_dir, show=show, group_vals= values)

    if settings["age_group"] == True:

        plot_age_compartment_comparison(
            agents,
            0,
            "Susceptible",
            colors,
            line_style,
            summary=total_group,
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            1,
            "Exposed",
            colors,
            line_style,
            summary=total_group,
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            3,
            "Infected",
            colors,
            line_style,
            summary=total_group,
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            4,
            "Recovered",
            colors,
            line_style,
            summary=total_group,
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            4,
            "Dead",
            colors,
            line_style,
            summary=total_group,
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )

    else:

        plot_compartment_comparison(
            agents, 0, "Susceptible", colors, line_style, sub_dir=output_dir, show=show, group_vals=values
        )

        #quit()
        plot_compartment_comparison(
            agents, 1, "Exposed", colors, line_style, sub_dir=output_dir, show=show, group_vals=values
        )
        plot_compartment_comparison(
            agents, 3, "Infected", colors, line_style, sub_dir=output_dir, show=show, group_vals=values
        )
        plot_compartment_comparison(
            agents, 4, "Recovered", colors, line_style, sub_dir=output_dir, show=show, group_vals=values
        )
        plot_compartment_comparison(
            agents, 5, "Dead", colors, line_style, sub_dir=output_dir, show=show, group_vals=values
        )

parser = ArgumentParser()

parser.add_argument(
    "--result_dirs",
    required=True,
    nargs="+",
    type=str,
    help="Directories with output from experiment",
)

parser.add_argument(
    "--output_dirs",
    default=None,
    nargs="+",
    type=str,
    help="Directories in which to save plots, if not given plots are saved in the result directory",
)

parser.add_argument(
    "--show",
    default=False,
    action="store_true",
    help="Set this flag to show the plots while saving them",
)
parser.add_argument(
    "--total_group",
    default=False,
    action="store_true",
    help="Set this flag to show the plots while saving them",
)

parser.add_argument(
    "--aggregate",
    default=None,
    action="store_true",
    help="Set this flag to be able to aggregate plots through mean",
)

parser.add_argument(
    "--file-value",
    default=None,
    nargs="+",
    type=str,
    help="Json file and values according to which to aggregate",
)

args = parser.parse_args()

if not isinstance(args.result_dirs, (list, tuple)):
    args.result_dirs = [args.result_dirs]

if not isinstance(args.output_dirs, (list, tuple)):
    args.output_dirs = [args.output_dirs]

assert len(args.output_dirs) == 1 or len(args.output_dirs) == len(args.result_dirs)

if not args.aggregate:

    for idx, result_dir in enumerate(args.result_dirs):

        # Load settings
        with open(joinpath(result_dir, "settings.json"), "rt") as f:
            settings = json.load(f)

        # Load agents
        agents = torch.load(joinpath(result_dir, "agents.pth"))

        # Load agents alphas
        alphas = np.load(joinpath(result_dir, "alphas_history.npy"), allow_pickle=True)

        # Get output directory
        output_dir = (
            args.output_dirs[idx] if len(args.output_dirs) > 1 else args.output_dirs[0]
        )
        if output_dir is None:
            output_dir = result_dir
            output_dir = relpath(output_dir, "../../results/")

        # Plotting based on verious settings
        all_plots(settings, [agents], alphas, args.total_group, output_dir, args.show)
else:
    values=[]

    for result_dir in args.result_dirs:
        with open(joinpath(result_dir, args.file_value[0]), 'rt') as f:
            data = json.load(f)

        for i in args.file_value[1:]:

            data = data[i]

        values.append(data)

    # Load settings
    with open(joinpath(args.result_dirs[0], "settings.json"), "rt") as f:
        settings = json.load(f)

    # Get output directory
    output_dir = args.output_dirs[0]
    assert output_dir is not None

    agents = [torch.load(joinpath(result_dir, "agents.pth")) for result_dir in args.result_dirs]

    alphas = [np.load(joinpath(result_dir, "alphas_history.npy")) for result_dir in args.result_dirs]

    # Plotting based on verious settings
    all_plots(settings, agents, aplhas, args.total_group, output_dir, args.show, values)

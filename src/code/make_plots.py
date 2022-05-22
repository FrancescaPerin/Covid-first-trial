import json
from argparse import ArgumentParser
from os.path import join as joinpath
from os.path import relpath

import torch

from plots import (
    plot_age_compartment_comparison,
    plot_compartment_comparison,
    plot_loss_GDP,
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

args = parser.parse_args()

if not isinstance(args.result_dirs, (list, tuple)):
    args.result_dirs = [args.result_dirs]

if not isinstance(args.output_dirs, (list, tuple)):
    args.output_dirs = [args.output_dirs]

assert len(args.output_dirs) == 1 or len(args.output_dirs) == len(args.result_dirs)

for idx, result_dir in enumerate(args.result_dirs):

    # Load settings
    with open(joinpath(result_dir, "settings.json"), "rt") as f:
        settings = json.load(f)

    # Load agents
    agents = torch.load(joinpath(result_dir, "agents.pth"))

    # Get output directory
    output_dir = (
        args.output_dirs[idx] if len(args.output_dirs) > 1 else args.output_dirs[0]
    )
    if output_dir is None:
        output_dir = result_dir
        output_dir = relpath(output_dir, "../../results/")

    # Plotting based on verious settings

    if settings["age_group"] == True:

        if settings["economy"] == True:

            plot_loss_GDP(agents, sub_dir=output_dir)

        plot_age_compartment_comparison(
            agents, 0, "Susceptible", settings["age_group_summary"], sub_dir=output_dir
        )
        plot_age_compartment_comparison(
            agents, 1, "Exposed", settings["age_group_summary"], sub_dir=output_dir
        )
        plot_age_compartment_comparison(
            agents, 3, "Infected", settings["age_group_summary"], sub_dir=output_dir
        )
        plot_age_compartment_comparison(
            agents, 4, "Recovered", settings["age_group_summary"], sub_dir=output_dir
        )

    else:

        if settings["economy"] == True:

            plot_loss_GDP(agents, sub_dir=output_dir)

        plot_compartment_comparison(agents, 0, "Susceptible", sub_dir=output_dir)
        plot_compartment_comparison(agents, 1, "Exposed", sub_dir=output_dir)
        plot_compartment_comparison(agents, 3, "Infected", sub_dir=output_dir)

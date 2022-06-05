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


def all_plots(settings, agents, output_dir, show, values=None):

    if settings["economy"] == True:

        plot_loss_GDP(agents[0], sub_dir=output_dir, show=show)

    if settings["age_group"] == True:

        plot_age_compartment_comparison(
            agents,
            0,
            "Susceptible",
            settings["age_group_summary"],
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            1,
            "Exposed",
            settings["age_group_summary"],
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            3,
            "Infected",
            settings["age_group_summary"],
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )
        plot_age_compartment_comparison(
            agents,
            4,
            "Recovered",
            settings["age_group_summary"],
            sub_dir=output_dir,
            show=show,
            group_vals=values,
        )

    else:

        plot_compartment_comparison(
            agents, 0, "Susceptible", sub_dir=output_dir, show=show, group_vals=values
        )
        plot_compartment_comparison(
            agents, 1, "Exposed", sub_dir=output_dir, show=show, group_vals=values
        )
        plot_compartment_comparison(
            agents, 3, "Infected", sub_dir=output_dir, show=show, group_vals=values
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

# TODO make this configurable
aggregate = True
values = [1,2,1,2]

args = parser.parse_args()

if not isinstance(args.result_dirs, (list, tuple)):
    args.result_dirs = [args.result_dirs]

if not isinstance(args.output_dirs, (list, tuple)):
    args.output_dirs = [args.output_dirs]

assert len(args.output_dirs) == 1 or len(args.output_dirs) == len(args.result_dirs)

if not aggregate:

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
        all_plots(settings, [agents], output_dir, args.show)
else:

    # Load settings
    with open(joinpath(args.result_dirs[0], "settings.json"), "rt") as f:
        settings = json.load(f)

    # Get output directory
    output_dir = args.output_dirs[0]
    assert output_dir is not None

    agents = [torch.load(joinpath(result_dir, "agents.pth")) for result_dir in args.result_dirs]

    # Plotting based on verious settings
    all_plots(settings, agents, output_dir, args.show, values)

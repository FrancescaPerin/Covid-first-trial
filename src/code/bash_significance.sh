#!/bin/bash

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_1 ../../results/plots/NationRL/set_1 --aggregated_output Nation_1_RL_1

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_1 ../../results/plots/NationRL/set_2 --aggregated_output Nation_1_RL_2

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_2 ../../results/plots/NationRL/set_3 --aggregated_output Nation_2_RL_3

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_2 ../../results/plots/NationRL/set_4 --aggregated_output Nation_2_RL_4

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_3 ../../results/plots/NationRL/set_5 --aggregated_output Nation_3_RL_5

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_3 ../../results/plots/NationRL/set_6 --aggregated_output Nation_3_RL_6  

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_4 ../../results/plots/NationRL/set_7 --aggregated_output Nation_4_RL_7

python extract_significance.py --aggregated_input ../../results/plots/Nation/set_4 ../../results/plots/NationRL/set_8 --aggregated_output Nation_4_RL_8
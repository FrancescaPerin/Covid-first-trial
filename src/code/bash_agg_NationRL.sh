#!/bin/bash

# Plots for settings_NationRL_set1.json
results_nationRL_1=( 2022_Sep_08_22_01_09 2022_Sep_08_22_04_31 2022_Sep_08_22_07_49 2022_Sep_08_22_11_08 2022_Sep_08_22_14_24 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_1[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_1

echo "Calculated aggregated analysis for NationRL set 1"

results_nationRL_2=( 2022_Sep_08_22_17_48 2022_Sep_08_22_21_10 2022_Sep_08_22_24_38 2022_Sep_08_22_28_02 2022_Sep_08_22_31_26 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_2[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_2

echo "Calculated aggregated analysis for NationRL set 2"

results_nationRL_3=( 2022_Sep_08_22_34_50 2022_Sep_08_22_38_16 2022_Sep_08_22_41_39 2022_Sep_08_22_45_03 2022_Sep_08_22_48_28 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_3[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_3

echo "Calculated aggregated analysis for NationRL set 3"

results_nationRL_4=( 2022_Sep_08_22_51_56 2022_Sep_08_22_55_28 2022_Sep_08_22_59_01 2022_Sep_08_23_02_26 2022_Sep_08_23_05_54 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_4[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_4

echo "Calculated aggregated analysis for NationRL set 4"

results_nationRL_5=( 2022_Sep_08_23_09_34 2022_Sep_08_23_13_11 2022_Sep_08_23_16_48 2022_Sep_08_23_20_25 2022_Sep_08_23_24_04 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_5[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_5

echo "Calculated aggregated analysis for NationRL set 5"

results_nationRL_6=( 2022_Sep_08_23_27_53 2022_Sep_08_23_31_37 2022_Sep_08_23_35_22 2022_Sep_08_23_39_07 2022_Sep_08_23_42_50 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_6[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_6

echo "Calculated aggregated analysis for NationRL set 6"

results_nationRL_7=(2022_Sep_08_23_46_34 2022_Sep_08_23_50_17 2022_Sep_08_23_53_58 2022_Sep_08_23_57_40 2022_Sep_09_00_01_23 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_7[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_7

echo "Calculated aggregated analysis for NationRL set 7"

results_nationRL_8=(2022_Sep_09_00_05_12 2022_Sep_09_00_08_59 2022_Sep_09_00_12_50 2022_Sep_09_00_16_39 2022_Sep_09_00_20_25 )

python analysis.py \
       --folders_input $(for dir in "${results_nationRL_8[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --analysis_type Aggregate-Experiment \
       --folders_output plots/NationRL/set_8

echo "Calculated aggregated analysis for NationRL set 8"


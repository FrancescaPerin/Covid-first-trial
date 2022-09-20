#! /bin/bash

#Nation

# Plots for settings_Nation_set1.json
results_nation_1=( 2022_Sep_08_20_48_08 2022_Sep_08_20_48_50 2022_Sep_08_20_49_31 2022_Sep_08_20_50_12 2022_Sep_08_20_50_54 )

python make_plots.py \
       --result_dirs $(for dir in "${results_nation_1[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
       --output_dirs plots/Nation/set_1 \
       --aggregate --file-value settings.json lockdown_period

echo "Made plots for Nation set 1"

# Plots for settings_Nation_set2.json
results_nation_2=( 2022_Sep_08_20_51_38 2022_Sep_08_20_52_21 2022_Sep_08_20_53_03 2022_Sep_08_20_53_46 2022_Sep_08_20_54_30 )

python make_plots.py \
     --result_dirs $(for dir in "${results_nation_2[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
     --output_dirs plots/Nation/set_2 \
     --aggregate --file-value settings.json lockdown_period --total_group

echo "Made plots for Nation set 2"

# Plots for settings_Nation_set3.json
results_nation_3=( 2022_Sep_08_20_55_30  2022_Sep_08_20_56_30 2022_Sep_08_20_57_30 2022_Sep_08_20_58_33 2022_Sep_08_20_59_34 )

python make_plots.py \
     --result_dirs $(for dir in "${results_nation_3[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
     --output_dirs plots/Nation/set_3 \
     --aggregate --file-value settings.json lockdown_period

echo "Made plots for Nation set 3"

# Plots for settings_Nation_set4.json
results_nation_4=( 2022_Sep_08_21_00_35 2022_Sep_08_21_01_37 2022_Sep_08_21_02_39 2022_Sep_08_21_03_43 2022_Sep_08_21_04_45 )

python make_plots.py \
     --result_dirs $(for dir in "${results_nation_4[@]}"; do echo ../../../../Old_results/results_latest/"${dir}"; done) \
     --output_dirs plots/Nation/set_4 \
     --aggregate --file-value settings.json lockdown_period --total_group

echo "Made plots for Nation set 4"

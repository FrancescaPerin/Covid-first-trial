#! /bin/bash

# Get nation type from command line
nation_type="${1}"

# Check command line arguments
if [ "${nation_type}" != "Nation" ] && [ "${nation_type}" != "NationRL" ];
then
    echo "Cannot accept ${nation_type} as Nation type"
    exit 1
fi

# For each config file
for config_file in ../json/settings_"${nation_type}"_set*.json
do
    # For each repetition (5 times)
    for rep in {1..5}
    do

        # Run experiment
        python experiment.py --settings "${config_file}" --agent_params ../json/all_agents_SEIARDV.json --topology ../json/complete_topology.json --agent_type "${nation_type}"

        # Print were results are (assumed to be last directory)
        last_results_dir="$( ls -tr ../../results | tail -n 1 )"
        echo "Results for $(basename ${config_file}) rep ${rep} in ${last_results_dir}"
        
    done
done

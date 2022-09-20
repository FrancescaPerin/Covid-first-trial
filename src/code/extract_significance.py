import argparse
import os
import numpy as np
import pandas as pd 
import json

from scipy.stats import t
from utils import load_JSON


def timestep_sign(metric, var, means, ses):

	v=[]

	for age_group in range(len(means[0])):

		means_age = [mean[age_group] for mean in means]
		se_age = [se[age_group] for se in ses]


		max_index = np.argmax(means_age)

		min_index = [0,1]
		min_index.remove(max_index)

		top = means_age[max_index] - var * se_age[max_index] 

		bottom = means_age[min_index[0]] + var * se_age[min_index[0]]

		v.append(bool(top > bottom))

	return  v


def find_sign(agg1, agg2):

	sig={}

	for agent in agg1.keys(): 

		sig[agent]={}

		for group in agg1[agent].keys():

			sig[agent][group]={}

			for metric in agg1[agent][group].keys():

				sig[agent][group][metric]={}

				var= np.abs(t.ppf((1-0.95)/2,len(agg1[agent][group][metric]['mean'])))

				means = [agg1[agent][group][metric]['mean'], agg2[agent][group][metric]['mean']]
				se = [agg1[agent][group][metric]['se'], agg2[agent][group][metric]['se']]

				
				if metric !='history':

					sig[agent][group][metric]= timestep_sign(metric, var, means, se)

				else:

					temp=[]
					for time in range(len(agg1[agent][group][metric]['mean'])):

						means = [agg1[agent][group][metric]['mean'][time], agg2[agent][group][metric]['mean'][time]]
						se = [agg1[agent][group][metric]['se'][time], agg2[agent][group][metric]['se'][time]]

						temp.append(timestep_sign(metric, var, means, se)) 

					sig[agent][group][metric]=temp			

	return sig

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Passing arguments to code.")

	parser.add_argument(
	"--aggregated_input",
	nargs='+',
	default="[]",
	help="Path to input folders",
	)

	parser.add_argument(
	"--aggregated_output",
	type=str,
	help="Path to output folder",
	)

	args = parser.parse_args()

	agg1 = load_JSON(os.path.join(args.aggregated_input[0],'timestep_analisis.json'))

	agg2 = load_JSON(os.path.join(args.aggregated_input[1],'timestep_analisis.json'))

	agg = find_sign(agg1, agg2)

	path = os.path.join('../../results/plots/significance_data/', args.aggregated_output)

	os.makedirs( path, exist_ok=True)

	with open(os.path.join(path,"significance_t.json"), "w") as write_file:
		json.dump(agg, write_file, indent = 8)




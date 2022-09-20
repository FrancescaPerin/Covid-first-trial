import numpy as np
import torch
import os
import glob
import json
import argparse

from utils import load_JSON

def extract_results(groups, folder, agents):

	dict_res={}

	for i, group in enumerate(groups):

		dict_res[group]={}

		for agent in agents:

			dict_res[group][agent]={}

			history=agents[agent].history[:,i+1]

			if history.shape[1]>1:
				history= np.column_stack([history, history.sum(1)])


			dict_res[group][agent]['max_v'] = list([float(i) for i in history.max(0)])

			dict_res[group][agent]['min_v'] = list([float(i) for i in history.min(0)])

			dict_res[group][agent]['mean_v'] = list([float(i) for i in history.mean(0)])

			dict_res[group][agent]['last_v'] = list([float(i) for i in history[-1]])

			dict_res[group][agent]['history'] = list([list(i.astype(float)) for i in history])

	return dict_res

def extract_avg(folders):

	exp={}

	avg={}

	for folder in folders:

		load_JSON(os.path.join(folder, 'result_analisis.json'))

		exp[folder]=load_JSON(os.path.join(folder, 'result_analisis.json'))
		agents = torch.load(os.path.join(folder, 'agents.pth'))


	for agent in agents:

		avg[agent] = {}

		for group in exp[folders[0]].keys():

			avg[agent][group] = {}

			for metric in exp[folder][group][agent].keys():

				avg[agent][group][metric] = {}

				temp = []

				for folder in folders:

					temp.append(exp[folder][group][agent][metric])

				mean = np.mean(temp, axis=0)
				avg[agent][group][metric]['mean'] = list([i for i in mean.tolist()])

				std = np.std(temp, axis=0)
				avg[agent][group][metric]['std'] = list([i for i in std.tolist()])

				se = avg[agent][group][metric]['std']/np.sqrt(len(avg[agent][group][metric]['std']))
				avg[agent][group][metric]['se'] = list([i for i in se.tolist() ])
	
	return avg

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Passing arguments to code.")

	parser.add_argument(
    "--folders_input",
    nargs='+',
    default="[]",
    help="Path to input folders",
	)

	parser.add_argument(
    "--analysis_type",
    type=str,
    choices=["Single-Experiment", "Aggregate-Experiment"],
    default="Single-Experiment",
    help="Type of analysis to be used",
	)

	parser.add_argument(
    "--folders_output",
    type=str,
    help="Path to output folder",
	)

	args = parser.parse_args()

	groups = ['S', 'E', 'A', 'I', 'R', 'D']

	if args.analysis_type=='Single-Experiment':
	
		for folder in args.folders_input:

			agents = torch.load(os.path.join(folder, 'agents.pth'))

			results = extract_results(groups, folder, agents)

			with open(os.path.join(folder,"result_analisis.json"), "w") as write_file:
				json.dump(results, write_file, indent = 8)
	
	if args.analysis_type=='Aggregate-Experiment':

		sett_json=[]

		for folder in args.folders_input:

			sett_json.append(load_JSON(glob.glob(os.path.join(folder, 'setting*.json'))[0]))

		if sett_json.count(sett_json[0]) == len(sett_json):

			avg = extract_avg(args.folders_input)

			with open(os.path.join('../../results', args.folders_output,"timestep_analisis.json"), "w") as write_file:
				json.dump(avg, write_file, indent = 8)

		else:
			sys.stderr.write('Setting are not the same across experiments folders. Exiting program.')

import numpy as np
import pandas as pd
import os 
import json

def load_population(file_name):

	matrix = pd.read_excel(io=file_name)

	return matrix 

def country_list (population, save_json=False):
	
	countries = population['Country Name'].unique()

	if save_json:
		with open('list_countries.json', 'w') as f:
			json.dump(countries.tolist(), f)

	return countries

def load_json(file_name):
	with open(file_name) as json_file:
		file = json.load(json_file)

	return file



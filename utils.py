import json
import numpy as np
import os 
import pandas as pd

from contact_m import contactMatrix, Population

def check_file(file_name):


	if not isinstance(file_name, str):
		raise TypeError("File name not a string")

	elif file_name.endswith('.json'):
		return file_name

	else:
		return file_name + '.json'


def load_JSON(file_name):

	with open(file_name, 'rt') as agents_json:
		return json.load(agents_json)

def load_contact(country):

	path = 'Preprocessing/new_matrices_152_countries'

	name='age_matrix.npy'

	home=np.load(os.path.join(path,'home',country, name))
	work=np.load(os.path.join(path,'work',country, name))
	school=np.load(os.path.join(path,'school',country, name))
	other=np.load(os.path.join(path,'other_locations',country, name))
	env=np.load(os.path.join(path,'environment',country, name))
	all_l=np.load(os.path.join(path,'all_locations',country, name))

	return contactMatrix(country, home, work, school, other,env, all_l)

def load_pop(country):

	path='Preprocessing population_group/Tables'

	name='population_table.npy'

	pop= np.load(os.path.join(path, country, name), allow_pickle=True)

	df = pd.DataFrame(pop, columns = ['Country','Group','2016','2017','2018','2019','2020'])
	df=df.replace('..', np.nan) #remplace emty cells with NaN values

	empty_row=0

	for index,row in df.iterrows():

		assert empty_row <= 2, f'No data for {country}. Select different country.' # not enough data present for population according to age

		if row.count() < 3:
			empty_row+=1

	return Population(*df['2020'].to_numpy())







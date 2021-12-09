import numpy as np
import pandas as pd  
import json
import os 


def load_matrix_xlsx(file_name,sheet):

	matrix = pd.read_excel(io=file_name, sheet_name=sheet)

	return matrix 


def list_countries(file_name, second_file=None, save_json=False):

	countries = pd.ExcelFile(file_name)

	if second_file!=None:
		countries_2 = pd.ExcelFile(second_file)
		
		tot_countries=countries.sheet_names+countries_2.sheet_names
	else:

		tot_countries=countries.sheet_names

	if save_json:
		with open('countries.json', 'w') as f:
			json.dump(tot_countries, f)
	
	return tot_countries


def age_to_group(age_matrix):

	temporary_matrix = pd.DataFrame({'c' : age_matrix.iloc[:,0:4].sum(axis=1),# 0 to 19
 							'a': age_matrix.iloc[:,4:13].sum(axis=1), #20 to 64
 							's': age_matrix.iloc[:,13:16].sum(axis=1) #65 to 80
 							})

	group_matrix= pd.DataFrame({'c': temporary_matrix.iloc[0:4,:].mean(axis=0),
							'a': temporary_matrix.iloc[4:13,:].mean(axis=0),
							's': temporary_matrix.iloc[13:16,:].mean(axis=0),
							
							

							}).T 

	return group_matrix

def reformat_all_matrices(locations, path, endings, parent_dir):

	max_val=0
	min_val=1000

	for location in locations:

		for ending in endings:

			if location=='environment':

					true_location='all_locations'
			else:
				true_location =location

			countries = list_countries(path+true_location+ending, save_json=False)

			for country in countries:

				new_path = os.path.join(parent_dir,location,country)

				os.makedirs(new_path, exist_ok = True)


				age_matrix=load_matrix_xlsx(path+true_location+ending, country)

				group_matrix=age_to_group(age_matrix).to_numpy()

				temp_max=np.amax(group_matrix)
				temp_min=np.amin(group_matrix)

				if location=='environment':

					env_matrix=group_matrix/6

					np.save(new_path+'/age_matrix',env_matrix)

					temp_max=np.amax(env_matrix)
					temp_min=np.amin(env_matrix)


				if temp_max> max_val:
					max_val=temp_max
				if temp_min< min_val:
					min_val=temp_min

	return temp_max, temp_min





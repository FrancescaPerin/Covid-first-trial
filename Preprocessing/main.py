import numpy as np
import json
import pandas as pd
import os 

from utils import load_matrix_xlsx, list_countries, age_to_group


locations=['home','other_locations','school','work']


path='contact_matrices_152_countries/MUestimates_'

endings=['_1.xlsx','_2.xlsx']


parent_dir='age_matrices_152_countries'
for location in locations:

	for ending in endings:

		countries= list_countries(path+location+ending, save_json=False)

		for country in countries:

			new_path = os.path.join(parent_dir,location,country)
			print(new_path)

			os.makedirs(new_path, exist_ok = True)

			age_matrix=load_matrix_xlsx(path+location+ending, country)

			group_matrix=age_to_group(age_matrix).to_numpy()

			np.save(new_path+'/age_matrix',group_matrix)









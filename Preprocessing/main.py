import numpy as np
import json
import pandas as pd
import os 

from utils import load_matrix_xlsx, list_countries, age_to_group, reformat_all_matrices, save_list_json, remove_countries, merge_xlsx

locations=['environment','all_locations','home','other_locations','school','work']

path='contact_matrices_152_countries/MUestimates_'

endings=['_1.xlsx','_2.xlsx']


#merging the files with same location in one single file
for location in locations[1:]:


	files_names=[path+location+endings[0],path+location+endings[1]]

	merge_xlsx(files_names)

#print(load_matrix_xlsx(path+locations[0]+'.xlsx', "Albania"))






#parent_dir='age_matrices_152_countries'

parent_dir='new_matrices_152_countries'

countries = list_countries(path+locations[-1]+'.xlsx')

for location in locations:

	reformat_all_matrices(countries,location,path,parent_dir)


save_list_json(countries,save_json=False)


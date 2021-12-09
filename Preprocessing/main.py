import numpy as np
import json
import pandas as pd
import os 

from utils import load_matrix_xlsx, list_countries, age_to_group, reformat_all_matrices

locations=['environment','all_locations','home','other_locations','school','work']

path='contact_matrices_152_countries/MUestimates_'

endings=['_1.xlsx','_2.xlsx']


parent_dir='age_matrices_152_countries'

max_val,min_val=reformat_all_matrices(locations,path,endings,parent_dir)

print(max_val)
print(min_val)


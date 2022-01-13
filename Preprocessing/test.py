import json
import os
import numpy as np

#locations=['environment','all_locations','home','other_locations','school','work']
locations=['home']
path_1='age_matrices_152_countries'

path_2='new_matrices_152_countries'

file = open('countries.json')
 
# returns JSON object as
# a dictionary
countries = json.load(file)

count=0

for location in locations:
	for country in countries:
		print(country)
		matrix_1=np.load(os.path.join(path_1,location,country)+'/age_matrix.npy')
		matrix_2=np.load(os.path.join(path_2,location,country)+'/age_matrix.npy')

		if not np.allclose(matrix_1,matrix_2):
			print('one')
			print(matrix_1)
			print('two')
			print(matrix_2)
			count+=1

print(count)




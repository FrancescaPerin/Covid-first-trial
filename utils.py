import json
import numpy as np
import os 

from contact_m import contactMatrix

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

def load_contact(path, country):

	name='age_matrix.npy'

	home=np.load(os.path.join(path,'home',country, name))
	work=np.load(os.path.join(path,'work',country, name))
	school=np.load(os.path.join(path,'school',country, name))
	other=np.load(os.path.join(path,'other_locations',country, name))
	env=np.load(os.path.join(path,'environment',country, name))
	all_l=np.load(os.path.join(path,'all_locations',country, name))

	return contactMatrix(country, home, work, school, other,env, all_l)



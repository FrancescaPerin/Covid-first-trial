import json

def check_file(file_name):


	if not isinstance(file_name, str):
		raise TypeError("File name not a string")

	elif file_name.endswith('.json'):
		return file_name

	else:
		return file_name + '.json'


def load_JSON(file_name):

	with open(file_name, 'rt') as agents_json:
		data_agents = json.load(agents_json)

	return data_agents
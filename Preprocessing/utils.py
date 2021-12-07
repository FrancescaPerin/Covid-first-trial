import pandas as pd  
import json


def load_matrix_xlsx(file_name,sheet):

	matrix = pd.read_excel(io=file_name, sheet_name=sheet)
	#print(matrix.head(5))  # print first 5 rows of the dataframe

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

	temporary_matrix = pd.DataFrame({'c' : age_matrix.iloc[:,0:4].sum(axis=1),
 							'a': age_matrix.iloc[:,4:13].sum(axis=1),
 							's': age_matrix.iloc[:,13:16].sum(axis=1)
 							})

	group_matrix= pd.DataFrame({'c': temporary_matrix.iloc[0:4,:].mean(axis=0),
							'a': temporary_matrix.iloc[4:13,:].mean(axis=0),
							's': temporary_matrix.iloc[13:16,:].mean(axis=0),
							
							

							}).T 

	return group_matrix
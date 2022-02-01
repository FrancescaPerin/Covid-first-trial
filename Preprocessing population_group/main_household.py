import numpy as np
import pandas as pd
import os
import json

from utils import load_json

save_json=True

old_countries=load_json('/Users/francescaperin/Desktop/MSc Thesis/My code start/Covid-first-trial/Preprocessing/countries.json')
current_countries=load_json('list_countries.json')

path='/Users/francescaperin/Desktop/MSc Thesis/My code start/Covid-first-trial/Preprocessing population_group/'
file_name=os.path.join (path, 'Household data/household_size.xlsx')

xls = pd.ExcelFile(file_name)
data=pd.read_excel(xls, 'UN HH Size and Composition 2019', header=None)

data.drop([0, 1, 2,3],inplace=True)
data.reset_index(drop=True, inplace=True)

data.columns = data.iloc[0]
data.drop([0], inplace=True)

new_countries = data['Country or area'].unique()

data['Reference date (dd/mm/yyyy)'] = pd.to_datetime(data['Reference date (dd/mm/yyyy)'])

common=list(set(old_countries).intersection(new_countries))

#common_2=list(set(old_countries).intersection(new_countries))


rest_old=list((set(old_countries)^set(new_countries))& set(old_countries))

rest_new=list((set(old_countries)^set(new_countries))& set(new_countries))

file_names_fix='Household data/name_fix_household.json'
countries_fix=load_json(path+file_names_fix)

countries_list=list()

for country in common:

	hh_table=data[data['Country or area']== country] ##add here to .drop(to drop columns)

	new_path=os.path.join(path, 'Household data','Tables', country)
	os.makedirs(new_path, exist_ok = True)

	np.save(new_path+'/hh_table',hh_table)

	countries_list.append(country)

for country in rest_old:

	if country in countries_fix: 

		hh_table=data[data['Country or area']== country]

		new_path=os.path.join(path, 'Household data','Tables', countries_fix[country])
		os.makedirs(new_path, exist_ok = True)

		np.save(new_path+'/hh_table',hh_table)

		countries_list.append(countries_fix[country])


if save_json==True:
	with open('Household data/hh_countries.json', 'w') as f:
		json.dump(countries_list, f)
















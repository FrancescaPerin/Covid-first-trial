import numpy as np
import pandas as pd
import json
import os

from utils import load_population, country_list, load_json


path='/Users/francescaperin/Desktop/MSc Thesis/My code start/Covid-first-trial/'
file='Data_Extract_From_World_Development_Indicators.xlsx'
population=load_population(file)

countries=country_list(population,True)[:-3]


file_m = '/Preprocessing/countries.json'

countries_m = load_json(path+file_m)

common=list(set(countries_m).intersection(countries))

rem_countries=list((set(countries_m)^set(countries))& set(countries_m))

rem_countries.remove('Taiwan')

file_names_fix='Preprocessing population_group/name_fix.json'

countries_fix=load_json(path+file_names_fix)

for country in common:

	pop_table=population[population['Country Name']== country].drop(columns=['Country Code', 'Series Code'])

	pop_table.sort_values(by=['Series Name'], inplace=True)

	new_path=os.path.join(path,'Preprocessing population_group', 'Tables', country)
	os.makedirs(new_path, exist_ok = True)

	np.save(new_path+'/population_table',pop_table)

for country in rem_countries:

	pop_table=population[population['Country Name']== country].drop(columns=['Country Code', 'Series Code'])

	pop_table.sort_values(by=['Series Name'], inplace=True)

	new_path=os.path.join(path,'Preprocessing population_group', 'Tables', countries_fix[country])
	os.makedirs(new_path, exist_ok = True)

	np.save(new_path+'/population_table',pop_table)

#print(rem_countries)

import numpy as np
import pandas as pd
import json
import os

from utils import load_population, country_list, load_json

file='Data_Extract_From_World_Development_Indicators.xlsx'
population=load_population(file)

countries=country_list(population,True)[:-3]

file_m = '/Users/francescaperin/Desktop/MSc Thesis/My code start/Covid-first-trial/Preprocessing/countries.json'

countries_m = load_json(file_m)

common=list(set(countries_m).intersection(countries))

rem_countries=list((set(countries_m)^set(countries))& set(countries))

rem_countries_m=list((set(countries_m)^set(countries))& set(countries_m))


print(common)
print(rem_countries)
print(rem_countries_m)

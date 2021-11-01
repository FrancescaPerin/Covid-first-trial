import numpy as np



class City:

	def __init__(self, name, country, population):
		self._name = name
		self._country = country
		self.population = population 

	def __repr__ (self):

		return "\nCity %s: Population %s,(Country %s) " % (self._name, self.population, self._country)

from dataclasses import dataclass
import numpy as np

@dataclass
class contactMatrix:

	def __init__(self, country: str, home, work, school, other, env, all_l):
		self.country = country
		self.home = home
		self.work = work
		self.school = school 
		self.other = other
		self.env = env
		self.all_l = all_l

	def __repr__(self):
		return """ 
			home:\n %s \n\n\t 
			work:\n %s \n\n\t 
			school:\n %s \n\n\t 
			other: \n %s \n\n\t
			env: \n %s \n\n\t 
			all_l: \n %s \n\n\t""" % (self.home, self.work, self.school, self.other, self.env, self.all_l)

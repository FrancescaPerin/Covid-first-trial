import numpy

class Agent:

	def __init__(self, name, x, y, z):

		self.name= name
		self.x = x
		self.y = y
		self.z = z 

	
	def __repr__ (self):

		return "Agent %s :  %s, %s, %s " % (self.name, self.x, self.y, self.z)
	

	def interact(self, conn_agents, type_inter, value):


		for agent in conn_agents:

			if type_inter==1:
				self.x -= value
				agent.x += value
			elif type_inter==2:
				self.y -= value
				agent.y +=value
			else:
				self.z -=value
				agent.z += value

		return self, conn_agents

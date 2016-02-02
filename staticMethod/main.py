import util
reload(util)

import second
reload(second)

class Pet(object):

	def __init__(self, name):
		self.name = name

pet = Pet('Mike')

util.UI(pet)

print(pet)
print(second.testCall())

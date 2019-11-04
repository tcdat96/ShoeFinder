class Shoe():
	score = ''

	def __init__(self, name, gender, price, numberOfColors, brand):
		self.name = name
		self.gender = gender
		self.price = price
		self.numberOfColors = numberOfColors
		self.brand = brand

	def __str__(self):
		return "%s\t%s's %s (%s) - %s colors" % (self.brand, self.gender, self.name, self.price, self.numberOfColors)
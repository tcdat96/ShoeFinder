class ShoeRating():
	def __init__(self, brand, name, score):
		self.brand = brand
		self.name = name
		self.score = score

	def __str__(self):
		return '%s\'%s: %s' % (self.brand, self.name, self.score)
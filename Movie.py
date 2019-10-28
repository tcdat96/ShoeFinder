class Movie():
    def __init__(self, title, year, genre, rating, director):
    	self.title = title
    	self.year = year
    	self.genre = genre
    	self.rating = rating
    	self.director = director

    def __str__(self):
    	return "Title: %s %s\nGenre: %s\nRating: %s\nDirector: %s\n" % (self.title, self.year, self.genre, self.rating, self.director)
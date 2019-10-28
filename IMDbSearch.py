from ISearchMovie import ISearchMovie
from Movie import Movie

import urllib
import requests
import json

from bs4 import BeautifulSoup
from bs4 import NavigableString

class IMDbSearch(ISearchMovie):
	def __init__(self):
		self.url = 'https://www.imdb.com/search/title/?'

	def getMovies(self, title):
		vars = {'title': title}
		url = self.url + urllib.parse.urlencode(vars)
		page = urllib.request.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')

		movies = []

		items = soup.find('div', {'class': 'lister-list'})
		for item in items.children:
			if isinstance(item, NavigableString):
				continue
			content = item.find('div', {'class': 'lister-item-content'})
			title = content.find('a').text
			year = content.find('span', {'class': 'lister-item-year'}).text
			genre = content.find('span', {'class': 'genre'}).text.strip('\n')
			
			ratingBar = content.find('div', {'class': 'ratings-imdb-rating'})
			rating = ratingBar.find('strong').text if ratingBar is not None else 'Not yet rated'

			crew = content.find(lambda crew:'Director' in crew.text)
			director = crew.find('a').text if crew is not None else ''

			movie = Movie(title, year, genre, rating, director)
			movies.append(movie)

		return movies

from IScraper import IScraper
from Shoe import Shoe

import urllib
import requests
import json

from bs4 import BeautifulSoup
from bs4 import NavigableString

class UnderAmourScraper(IScraper):
	def __init__(self):
		self.url = 'https://www.underarmour.com/en-us/search/'

	def getUrl(self, name, gender, sport):
		ext = (gender + 's/' if gender != '' else '') + 'footwear' + ('/' + sport if sport != '' else '') + '?'
		vars = {'q': name}
		return self.url + ext + urllib.parse.urlencode(vars)

	def getShoes(self, name, gender='', sport=''):
		soup = IScraper.getData(self, name, gender, sport)
		shoes = []
		grid = soup.find('ul', {'class': 'tileset'})
		items = soup.find_all('li', {'class': 'tile'})
		for item in items:
			if isinstance(item, NavigableString):
				continue

			name = item.find('div', {'class': 'title'}).text.strip('\n\r\t')

			price = item.find('span', {'class': 'price'})
			if price is not None:
				price = price.text.strip('\n\r\t')

			colors = 0
			chips = item.find('ul', {'class': 'chips'})
			if chips is not None:
				colors = len(chips.find_all('li'))
			
			shoe = Shoe(name, gender, price, colors, 'UnderAmour')
			shoes.append(shoe)
			print(shoe)

		return shoes

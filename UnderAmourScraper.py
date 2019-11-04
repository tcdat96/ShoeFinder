from IScraper import IScraper
from Shoe import Shoe

import urllib
import requests
import json

from bs4 import BeautifulSoup
from bs4 import NavigableString

class UnderAmourScraper(IScraper):
	def __init__(self):
		self.domain = 'https://www.underarmour.com/en-us'

	def getUrl(self, name, gender, sport):
		ext = (gender + 's/' if gender != '' else '') + 'footwear' + ('/' + sport if sport != '' else '')
		if name != '':
			vars = {'q': name}
			return '%s/search/%s?%s' % (self.domain, ext, urllib.parse.urlencode(vars))
		else:
			return '%s/%s' % (self.domain, ext)

	def getShoes(self, name, gender='', sport=''):
		soup = IScraper.getData(self, name, gender, sport)
		if soup is None:
			return []

		grid = soup.find('ul', {'class': 'tileset'})
		if grid is None:
			return []

		shoes = []
		items = grid.find_all('li', {'class': 'tile'})
		for item in items:
			if isinstance(item, NavigableString):
				continue

			name = item.find('div', {'class': 'title'}).text.strip('\n\r\t')

			price = item.find('span', {'class': 'price'})
			if price is None:
				price = item.find('span', {'class': 'price-sale'})
			if price is not None:
				price = price.text.strip('\n\r\t')

			chips = item.find('ul', {'class': 'chips'})
			colors = len(chips.find_all('li')) if chips is not None else 0

			shoe = Shoe(name, gender, price, colors, 'UnderAmour')
			shoes.append(shoe)

		return shoes

from IScraper import IScraper
from ShoeRating import ShoeRating

import urllib
import requests
import json
import re

from bs4 import BeautifulSoup
from bs4 import NavigableString

class RunRepeatScraper(IScraper):
	def __init__(self):
		self.domain = 'https://runrepeat.com'

	def getUrl(self, name, gender, sport):
		return '%s/search?q=%s&brand=new-balance,puma,under-armour&category=all' % (self.domain, name)

	def getShoes(self, name, gender='', sport=''):
		soup = IScraper.getData(self, name, gender, sport)
		if soup is None:
			return []

		rankingList = soup.find('ol', {'id': 'rankings-list'})
		if rankingList is None:
			return []

		ratings = []		
		items = rankingList.find_all('li')
		for item in items:
			if isinstance(item, NavigableString):
				continue

			name = item.find('div', {'class': 'product-name'})
			if name is None:
				continue
			name = name.text.strip().strip('\n\r\t')
			brand, name = self.breakDownName(name)

			score = item.find('div', {'class': 'overall_score'})
			if score is None:
				continue
			score = score.text.strip().strip('\n\r\t')

			rating = ShoeRating(brand, name, score)
			ratings.append(rating)

		return ratings

	def breakDownName(self, name):
		if name.startswith('New Balance'):
			brand = 'New Balance'
			name = name[12:]
		elif name.startswith('Puma'):
			brand = 'Puma'
			name = name[5:]
		elif name.startswith('Under Armour'):
			brand = 'Under Armour'
			name = name[13:]
		return (brand.strip().strip('\n\r\t'), name.strip().strip('\n\r\t'))
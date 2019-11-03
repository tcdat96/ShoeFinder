from IScraper import IScraper
from Shoe import Shoe

import urllib
import requests
import json
import re

from bs4 import BeautifulSoup
from bs4 import NavigableString

class PumaScraper(IScraper):
	def __init__(self):
		self.url = 'https://us.puma.com/en/us/search?'

	def getUrl(self, name, gender, sport):
		vars = {'q': name, 'prefn1': 'productDivision', 'prefv1': 'Footwear', 'pagesize': 128}
		if gender != '':
			vars['prefn2'] = 'gender'
			vars['prefv2'] = gender
		if sport != '':
			vars['prefn3'] = 'sportName'
			vars['prefv3'] = sport
		return self.url + urllib.parse.urlencode(vars)

	def getShoes(self, name, gender='', sport=''):
		soup = IScraper.getData(self, name, gender, sport)
		grid = soup.find('div', {'class': 'product-grid'})
		if grid is None:
			return []

		shoes = []
		items = grid.find_all('div', {'class': 'product-tile'})		
		for item in items:
			if isinstance(item, NavigableString):
				continue

			body = item.find('div', {'class': 'tile-body'})
			name = body.find('div', {'class': 'pdp-link'}).text.strip('\n\r\t')

			price = 'N/A'
			priceDiv = body.find('div', {'class': 'price'})
			if priceDiv is not None:
				price = priceDiv.find('span', {'class': 'value'}).text.strip()

			colors = 0
			swatches = body.find('div', {'class': 'swatches'})
			if swatches is not None:
				colors = len(swatches.find_all('a', {'class': 'swatch__container'}))
			
			shoe = Shoe(name, gender, price, colors, 'Puma')
			print(shoe)
			shoes.append(shoe)

		return shoes

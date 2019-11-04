from IScraper import IScraper
from Shoe import Shoe

import urllib
import requests
import json
import re

from bs4 import BeautifulSoup
from bs4 import NavigableString

class NewBalanceScraper(IScraper):
	def __init__(self):
		self.domain = 'https://www.newbalance.com'

	def getUrl(self, name, gender, sport):
		if name != '':
			vars = {'q': name, 'prefn1': 'productClass', 'prefv1': 'Shoes', 'sz': 48}
			if gender != '':
				vars['prefn2'] = 'genderAndAgeGroupCombo'
				vars['prefv2'] = gender
			if sport != '':
				vars['prefn3'] = 'activity'
				vars['prefv3'] = sport
			return '%s/search?%s' % (self.domain, urllib.parse.urlencode(vars))
		else:
			return '%s/%s/shoes/%s/' % (self.domain, gender, sport)

	def getShoes(self, name, gender='', sport=''):
		soup = IScraper.getData(self, name, gender, sport)
		if soup is None:
			return []

		productList = soup.find('ul', {'id': 'product-list-main'})
		if productList is None:
			# for only sport and gender case
			productList = soup.find('div', {'class': 'product-groups'})
			if not productList:
				return []

		shoes = []		
		items = productList.find_all('li')
		for item in items:
			if isinstance(item, NavigableString):
				continue

			product = item.find('div', {'class': 'product'})
			name = product.find('p', {'class': 'product-name'}).text.strip('\r\n\t')

			price = 0
			productPricing = product.find('div', {'class': 'product-pricing'})
			if productPricing is not None:
				price = productPricing.text.strip().replace('\n', '').replace('\r', '').replace('\t', '')

			colors = 0
			swatches = product.find('div', {'class': 'swatches'})
			if swatches is not None:
				colors = len(swatches.find_all('a', {'class': 'color'}))
			
			shoe = Shoe(name, gender, price, colors, 'NewBalance')
			shoes.append(shoe)

		return shoes

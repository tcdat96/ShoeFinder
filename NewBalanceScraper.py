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
		self.url = 'https://www.newbalance.com/search?'

	def getUrl(self, name, gender):
		vars = {'q': name, 'prefn1': 'genderAndAgeGroupCombo', 'prefn2': 'productClass', 'sz': 48, 'prefv1': gender, 'prefv2': 'Shoes'}
		return self.url + urllib.parse.urlencode(vars)

	def getShoes(self, name, gender):
		soup = IScraper.getData(self, name, gender)
		shoes = []
		items = soup.find('ul', {'id': 'product-list-main'}).find_all('li')
		for item in items:
			if isinstance(item, NavigableString):
				continue

			product = item.find('div', {'class': 'product'})
			name = product.find('p', {'class': 'product-name'}).text.strip('\r\n\t')

			price = 0
			productPricing = product.find('div', {'class': 'product-pricing'})
			if productPricing is not None:
				price = productPricing.text.strip().replace('\n', "").replace('\r', "").replace('\t', "")

			colors = 0
			swatches = product.find('div', {'class': 'swatches'})
			if swatches is not None:
				colors = len(swatches.find_all('a', {'class': 'color'}))
			
			shoe = Shoe(name, gender, price, colors, 'NewBalance')
			print(shoe)
			shoes.append(shoe)

		return shoes

from IScraper import IScraper
from ShoeRating import ShoeRating

import abc
import urllib
import requests
import json

from bs4 import BeautifulSoup
from bs4 import NavigableString

class RatingScraper(IScraper):
	def __init__(self):
		self.domain = 'https://runrepeat.com'

	@abc.abstractmethod
	def getUrl(self, name, gender, sport):
		raise NotImplementedError

	@abc.abstractmethod
	def getShoes(self, name, gender='', sport=''):
		raise NotImplementedError

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
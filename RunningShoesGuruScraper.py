from IScraper import IScraper
from RatingScraper import RatingScraper
from ShoeRating import ShoeRating

import urllib
import requests
import json

from bs4 import BeautifulSoup
from bs4 import NavigableString

class RunningShoesGuruScraper(RatingScraper):
	def __init__(self):
		self.domain = 'https://www.runningshoesguru.com'

	def getUrl(self, name, gender, sport):
		return '%s/?s=%s' % (self.domain, name)

	def getShoes(self, name, gender='', sport=''):
		soup = IScraper.getData(self, name, gender, sport)
		if soup is None:
			return []

		rankingList = soup.find('ul', {'class': 'row list-unstyled'})
		if rankingList is None:
			return []

		ratings = []
		items = rankingList.find_all('div', {'class': 'panel-body'})
		for item in items:
			if isinstance(item, NavigableString):
				continue

			name = item.find('h2', {'class': 'entry-title'})
			if name is None:
				continue
			name = name.text.strip().strip('\n\r\t')
			brand, name = RatingScraper.breakDownName(self, name)

			score = item.find(lambda score:'User\'s rating' in score.text)
			if score is None:
				continue
			score = score.find('div', {'class': 'review_box_stars_small'})
			score = score.text.strip().strip('\n\r\t')
			score = int(score[:-3]) * 10
			if score == 0:
				continue

			rating = ShoeRating(brand, name, score)
			ratings.append(rating)

		return ratings
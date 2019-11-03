import abc
import urllib3
import requests
from bs4 import BeautifulSoup

class IScraper(abc.ABC):
	@abc.abstractmethod
	def getUrl(self, name, gender):
		raise NotImplementedError

	def getData(self, name, gender):
		url = self.getUrl(name, gender)
		print(url)
		http = urllib3.PoolManager()
		userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		headers = {'user-agent': userAgent}
		page = requests.get(url, headers=headers)
		return BeautifulSoup(page.content, features='html.parser')

	@abc.abstractmethod
	def getShoes(self, name, gender):
		raise NotImplementedError
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from Shoe import Shoe
import IScraper
from NewBalanceScraper import NewBalanceScraper
from PumaScraper import PumaScraper
from UnderAmourScraper import UnderAmourScraper

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'DbMS Term Project'
		self.left = 500
		self.top = 500
		self.width = 640
		self.height = 480
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		# Create textbox
		self.textbox = QLineEdit(self)
		self.textbox.move(20, 20)
		self.textbox.resize(280,40)

		# Create a button in the window
		self.button = QPushButton('Show text', self)
		self.button.move(20,80)
		self.button.clicked.connect(self.on_click)

		NewBalanceScraper().getShoes("fresh", "Men")
		PumaScraper().getShoes("roma", "Men")
		UnderAmourScraper().getShoes("HOVR", "Men")

		self.show()

	@pyqtSlot()
	def on_click(self):
		title = self.textbox.text()
		self.textbox.setText("")
		shoes = []
		sources = [NewBalanceScraper()]
		for source in sources:
			shoes.extend(source.getShoes(title))
		for shoe in shoes:
			print(shoe)
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
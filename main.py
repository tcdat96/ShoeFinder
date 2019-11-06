import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QTabWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt5.QtCore import *
from PyQt5 import QtCore

from Shoe import Shoe
import IScraper
from NewBalanceScraper import NewBalanceScraper
from PumaScraper import PumaScraper
from UnderArmourScraper import UnderArmourScraper

from RunRepeatScraper import RunRepeatScraper
from RunningShoesGuruScraper import RunningShoesGuruScraper

class App(QWidget):

    sources = [NewBalanceScraper(), PumaScraper(), UnderArmourScraper()]
    ratingSources = [RunRepeatScraper(), RunningShoesGuruScraper()]

    def __init__(self):
        super().__init__()
        self.title = 'SneakerFinder'

        size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        width = size.width()
        height = size.height()

        self.left = int(width / 4)
        self.top = int(height / 6)
        self.width = self.left * 2
        self.height = self.top * 4

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.createMainTab()

        self.layout.addWidget(self.tabs)

        self.show()

    def createMainTab(self):
        self.tab1 = QWidget()
        self.tab1.layout = QHBoxLayout(self)

        container = QVBoxLayout(self)

        # icon
        label = QLabel(self)
        pixmap = QPixmap('icon.jpg')
        pixmap = pixmap.scaled(int(self.width / 3), int(self.width / 3), QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        container.addWidget(label, 1)

        # application name
        nameLabel = QLabel('SneakerFinder', self)
        nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        nameLabel.setStyleSheet("font: 30pt Comic Sans MS")
        container.addWidget(nameLabel)

        container.addStretch(1)

        # name
        nameContainer = QHBoxLayout(self)
        nameLabel = QLabel('Name', self)
        self.tab1.name = QLineEdit(self)
        nameContainer.addWidget(nameLabel)
        nameContainer.addWidget(self.tab1.name)
        container.addLayout(nameContainer)
        # gender
        self.tab1.gender = QComboBox(self)
        self.tab1.gender.addItems(['', 'Men', 'Women'])
        container.addWidget(self.tab1.gender)
        # sport
        self.tab1.sport = QComboBox(self)
        self.tab1.sport.addItems(['', 'Lifestyle', 'Running', 'Training', 'Baseball', 'Basketball', 'Soccer'])
        container.addWidget(self.tab1.sport)
        # price range
        rangeContainer = QHBoxLayout(self)
        rangeLabel = QLabel('Price range', self)
        onlyInt = QIntValidator(0, 100000)
        self.tab1.minPrice = QLineEdit(self)
        self.tab1.minPrice.setValidator(onlyInt)
        self.tab1.maxPrice = QLineEdit(self)
        self.tab1.maxPrice.setValidator(onlyInt)
        rangeContainer.addWidget(rangeLabel)
        rangeContainer.addWidget(self.tab1.minPrice, 1)
        rangeContainer.addWidget(self.tab1.maxPrice, 1)
        container.addLayout(rangeContainer)
        # search button
        button = QPushButton('Search', self)
        button.clicked.connect(self.on_click)
        container.addWidget(button, 1)

        # processing text
        self.tab1.loading = QLabel(self)
        self.tab1.loading.setAlignment(QtCore.Qt.AlignCenter)
        container.addWidget(self.tab1.loading)

        container.addStretch(1)
        self.tab1.layout.addLayout(QVBoxLayout(self), 1)
        self.tab1.layout.addLayout(container, 1)
        self.tab1.layout.addLayout(QVBoxLayout(self), 1)

        self.tab1.setLayout(self.tab1.layout)
        self.tabs.addTab(self.tab1, "SneakerFinder")

    @QtCore.pyqtSlot()
    def on_click(self):
        name = self.tab1.name.text()
        sport = self.tab1.sport.currentText()
        gender = self.tab1.gender.currentText()

        if name == '' and (sport == '' or gender == ''):
            self.tab1.loading.setText('Either name is not empty or\nboth sport and gender cannot be empty')
            return

        self.tab1.loading.setText('Searching...')
        self.tab1.loading.repaint()

        tabName = (gender + '/' if gender != '' else '') + (sport + '/' if sport != '' else '') + name
        tab = self.createTab(tabName)

        shoes = []
        for source in self.sources:
            shoes.extend(source.getShoes(name, gender, sport))
        # for shoe in shoes:
        #     print(shoe)
        # shoes = [Shoe('name 1','Men','$1','1','NewBalance'),Shoe('name 2','Women','$2','2','Puma'),Shoe('name 3','Kids','$3','3','UnderArmour')]

        shoes = self.filterPrice(shoes)

        # ratings
        if name != '':
            shoes = self.populateRatings(shoes, name)

        table = self.populateTable(shoes)
        tab.layout.addWidget(table)

        # hide score column if name is empty
        if name == '':
            table.setColumnHidden(4, True)

        self.tab1.loading.setText('')

    def filterPrice(self, shoes):
        try:
            minPrice = float(self.tab1.minPrice.text())
        except ValueError:
            minPrice = 0
        try:
            maxPrice = float(self.tab1.maxPrice.text())
        except ValueError:
            maxPrice = 100000
        return list(filter(lambda shoe: shoe.price >= minPrice and shoe.price <= maxPrice, shoes))

    def populateRatings(self, shoes, name):
        ratings = []
        for source in self.ratingSources:
            ratings.extend(source.getShoes(name))

        for shoe in shoes: print(shoe)
        for rating in ratings: print(rating)

        result = []
        for shoe in shoes:
            added = False
            for rating in ratings:
                if shoe.name == rating.name and shoe.brand == rating.brand:
                    result.append((shoe, rating.score))
                    added = True
            if added is False:
                result.append((shoe, ''))

        return result

    def createTab(self, title):
        tab = QWidget()
        tab.layout = QVBoxLayout(self)
        tab.layout.setAlignment(QtCore.Qt.AlignCenter)
        tab.setLayout(tab.layout)

        self.tabs.addTab(tab, title)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

        return tab

    def populateTable(self, shoes):
        table = self.createTable(len(shoes))
        self.fillTable(table, shoes)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        return table

    def createTable(self, rows):
        table = QTableWidget()
        table.setRowCount(rows)
        table.setColumnCount(5)
        table.setHorizontalHeaderItem(0, QTableWidgetItem('Name'));
        table.setHorizontalHeaderItem(1, QTableWidgetItem('Price'));
        table.setHorizontalHeaderItem(2, QTableWidgetItem('Colors'));
        table.setHorizontalHeaderItem(3, QTableWidgetItem('Brand'));
        table.setHorizontalHeaderItem(4, QTableWidgetItem('Score'));
        return table

    def fillTable(self, table, shoes):
        for i in range(len(shoes)):
            shoe = shoes[i][0]
            score = shoes[i][1]
            table.setItem(i, 0, QTableWidgetItem(shoe.name))

            price = '$%.2f' % shoe.price
            table.setItem(i, 1, QTableWidgetItem(price))

            if shoe.numberOfColors != 0:
                colorItem = QTableWidgetItem(str(shoe.numberOfColors))
                colorItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(i, 2, colorItem)

            table.setItem(i, 3, QTableWidgetItem(shoe.brand))

            if score != '':
                scoreItem = QTableWidgetItem(str(score))
                scoreItem.setTextAlignment(QtCore.Qt.AlignCenter);
                table.setItem(i, 4, scoreItem)
    
    def closeTab(self, currentIndex):
        self.tabs.removeTab(currentIndex)
        if self.tabs.count() == 0:
            QCoreApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
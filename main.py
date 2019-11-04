import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QTabWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtCore

from Shoe import Shoe
import IScraper
from NewBalanceScraper import NewBalanceScraper
from PumaScraper import PumaScraper
from UnderAmourScraper import UnderAmourScraper

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'DbMS Term Project'

        size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        width = size.width()
        height = size.height()

        self.left = int(width / 3)
        self.top = int(height / 6)
        self.width = self.left
        self.height = self.top * 4

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout(self)
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

        # name
        self.tab1.textbox = QLineEdit(self)
        container.addWidget(self.tab1.textbox, 1)
        # gender
        self.tab1.gender = QComboBox(self)
        self.tab1.gender.addItems(['', 'Men', 'Women'])
        container.addWidget(self.tab1.gender, 1)
        # sport
        self.tab1.sport = QComboBox(self)
        self.tab1.sport.addItems(['', 'Lifestyle', 'Running', 'Training', 'Baseball', 'Basketball', 'Soccer'])
        container.addWidget(self.tab1.sport, 1)
        # search button
        button = QPushButton('Show text', self)
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
        self.tabs.addTab(self.tab1, "ShoeFinder")

    @QtCore.pyqtSlot()
    def on_click(self):
        name = self.tab1.textbox.text()
        sport = self.tab1.sport.currentText()
        gender = self.tab1.gender.currentText()

        self.tab1.loading.setText('Searching...')
        self.tab1.loading.repaint()

        tabName = (gender + '/' if gender != '' else '') + (sport + '/' if sport != '' else '') + name
        tab = self.createTab(tabName)

        shoes = []
        sources = [NewBalanceScraper(), PumaScraper(), UnderAmourScraper()]
        for source in sources:
            shoes.extend(source.getShoes(name, gender, sport))
        for shoe in shoes:
            print(shoe)
        # shoes = [Shoe('name 1','Men','$1','1','NewBalance'),Shoe('name 2','Women','$2','2','Puma'),Shoe('name 3','Kids','$3','3','UnderAmour')]
        
        table = self.populateTable(shoes)
        tab.layout.addWidget(table)
        self.tab1.loading.setText('')

    def createTab(self, title):
        tab = QWidget()
        tab.layout = QVBoxLayout(self)
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
        table.setColumnCount(4)
        table.setHorizontalHeaderItem(0, QTableWidgetItem('Name'));
        table.setHorizontalHeaderItem(1, QTableWidgetItem('Price'));
        table.setHorizontalHeaderItem(2, QTableWidgetItem('Colors'));
        table.setHorizontalHeaderItem(3, QTableWidgetItem('Brand'));
        return table

    def fillTable(self, table, shoes):
        for i in range(len(shoes)):
            shoe = shoes[i]
            table.setItem(i,0, QTableWidgetItem(shoe.name))
            table.setItem(i,1, QTableWidgetItem(shoe.price))

            colorItem = QTableWidgetItem(str(shoe.numberOfColors))
            colorItem.setTextAlignment(QtCore.Qt.AlignCenter);
            table.setItem(i,2, colorItem)

            table.setItem(i,3, QTableWidgetItem(shoe.brand))
    
    def closeTab(self, currentIndex):
        self.tabs.removeTab(currentIndex)
        if self.tabs.count() == 0:
            QCoreApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
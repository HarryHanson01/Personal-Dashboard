import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget, QGridLayout
import psutil
import pyqtgraph as pg

from systemStatsModule import SystemStatsPanel
from todoModule import TodoPanel
from weatherModule import WeatherPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Dashboard")
        self.setFixedSize(QSize(800, 600))

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout()
        centralWidget.setLayout(mainLayout)
        
        dashboardLayout = QGridLayout()
        mainLayout.addLayout(dashboardLayout)

        systemStatsPanel = SystemStatsPanel()
        todoPanel = TodoPanel()
        weatherPanel = WeatherPanel()

        #(widget, row, column, rowspan, colspan)
        dashboardLayout.addWidget(systemStatsPanel, 0, 0, 1, 2)  # big top panel
        dashboardLayout.addWidget(todoPanel, 1, 0, 1, 1)           # bottom left
        dashboardLayout.addWidget(weatherPanel, 1, 1, 1, 1)        # bottom right

        # temporary - remove these upon styling
        #systemStatsPanel.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        todoPanel.setStyleSheet("background-color: lightgreen; border: 1px solid black;")
        weatherPanel.setStyleSheet("background-color: red; border: 1px solid black;")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
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
        self.resize(1100, 750)
        self.setMinimumSize(900, 650)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout()
        centralWidget.setLayout(mainLayout)
        
        dashboardLayout = QGridLayout()
        mainLayout.addLayout(dashboardLayout)

        systemStatsPanel = SystemStatsPanel()
        todoPanel = TodoPanel()
        weatherPanel = WeatherPanel()

        # this will be deleted later - I want to make the each panel movable by the user.
        #(widget, row, column, rowspan, colspan)
        dashboardLayout.addWidget(systemStatsPanel, 0, 0, 1, 3)
        dashboardLayout.addWidget(todoPanel, 1, 0, 1, 2)
        dashboardLayout.addWidget(weatherPanel, 1, 2, 1, 1)

        # styling
        weatherPanel.setObjectName("WeatherPanel")
        todoPanel.setObjectName("TodoPanel")
        systemStatsPanel.setObjectName("SystemStatsPanel")



app = QApplication(sys.argv)

with open("app/styles/main.css", "r") as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()

app.exec()
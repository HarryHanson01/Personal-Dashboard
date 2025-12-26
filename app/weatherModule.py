from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QPushButton, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
from weatherService import fetch_weather
from datetime import datetime

class WeatherPanel(QFrame):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)

        headerLayout = QHBoxLayout()


        titleLabel = QLabel("<b>Weather</b>")

        self.todayButton = QPushButton("Today")
        self.forecastButton = QPushButton("5-Day")

        self.todayButton.setCheckable(True)
        self.forecastButton.setCheckable(True)
        self.todayButton.setChecked(True)

        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch()
        headerLayout.addWidget(self.todayButton)
        headerLayout.addWidget(self.forecastButton)

        mainLayout.addLayout(headerLayout)


        self.stack = QStackedWidget()
        mainLayout.addWidget(self.stack)

        self.todayView = QWidget()
        self.forecastView = QWidget()

        self.stack.addWidget(self.todayView) # index 0
        self.stack.addWidget(self.forecastView) # index 1
        self.todayButton.clicked.connect(lambda: self.switchView(0))
        self.forecastButton.clicked.connect(lambda: self.switchView(1))

        self.stack.setCurrentIndex(0)


        self.buildTodayView()

        self.buildForecastView()

        self.loadWeather()



    def switchView(self, index):
        self.stack.setCurrentIndex(index)
        self.todayButton.setChecked(index == 0)
        self.forecastButton.setChecked(index == 1)

    
    def buildTodayView(self):
        layout = QVBoxLayout(self.todayView)

        self.iconLabel = QLabel()
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tempLabel = QLabel("— °C")
        self.tempLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.descLabel = QLabel("—")
        self.descLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.detailsLabel = QLabel("—")
        self.detailsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.iconLabel)
        layout.addWidget(self.tempLabel)
        layout.addWidget(self.descLabel)
        layout.addWidget(self.detailsLabel)

    
    def buildForecastView(self):
        layout = QVBoxLayout(self.forecastView)

        self.forecastContainer = QWidget()
        self.forecastLayout = QVBoxLayout(self.forecastContainer)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.forecastContainer)

        layout.addWidget(scroll)


    def loadWeather(self):
        try:
            data = fetch_weather()
            self.updateToday(data["current"])
            self.updateForecast(data["forecast"])
        except Exception as e:
            print("Weather error:", e)
            self.tempLabel.setText("Weather unavailable")


    def updateToday(self, data):
        temp = round(data["main"]["temp"])
        feels = round(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]

        weather = data["weather"][0]
        desc = weather["description"].title()
        iconCode = weather["icon"]
        windMps = data["wind"]["speed"]
        windMph = round(windMps * 2.23694)

        self.tempLabel.setText(f"{temp} °C")
        self.descLabel.setText(desc)
        self.detailsLabel.setText(
            f"Feels like {feels} °C · Humidity {humidity}% · Wind {windMph} mph"
        )

        self.setWeatherIcon(iconCode)



    def updateForecast(self, data):
        # Clear old widgets
        for i in reversed(range(self.forecastLayout.count())):
            widget = self.forecastLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        daily = {}

        # one entry per day
        for entry in data["list"]:
            dateStr = datetime.fromtimestamp(entry["dt"]).strftime("%a")
            temp = round(entry["main"]["temp"])
            desc = entry["weather"][0]["main"]
            icon = entry["weather"][0]["icon"]

            if dateStr not in daily:
                daily[dateStr] = {"temp": temp, "desc": desc, "icon": icon}

        # for next 5 days
        for day, info in list(daily.items())[1:6]:
            dayLayout = QHBoxLayout()

            iconLabel = QLabel()
            iconLabel.setFixedSize(50, 50)  # will probably need adjusting
            self.setForecastIcon(iconLabel, info["icon"])

            dayLabel = QLabel(day)
            dayLabel.setFixedWidth(50)

            tempLabel = QLabel(f"{info['temp']}°C {info['desc']}")

            dayLayout.addWidget(iconLabel)
            dayLayout.addWidget(dayLabel)
            dayLayout.addWidget(tempLabel)
            dayLayout.addStretch()

            container = QWidget()
            container.setLayout(dayLayout)

            self.forecastLayout.addWidget(container)


    def setWeatherIcon(self, iconCode):
        url = f"https://openweathermap.org/img/wn/{iconCode}@2x.png"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            self.iconLabel.setPixmap(pixmap)

        except Exception as e:
            print("Icon error:", e)
            self.iconLabel.clear()


    def setForecastIcon(self, label, iconCode):
        url = f"https://openweathermap.org/img/wn/{iconCode}@2x.png"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            label.setPixmap(pixmap)
        except Exception as e:
            print("Forecast icon error:", e)
            label.clear()

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame

class WeatherPanel(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Weather Panel")
        layout.addWidget(label)
        self.setLayout(layout)
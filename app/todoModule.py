from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class TodoPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Todo Panel")
        layout.addWidget(label)
        self.setLayout(layout)
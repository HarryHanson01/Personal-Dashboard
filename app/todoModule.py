from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QCheckBox, QScrollArea, QDateEdit, QMessageBox, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QDate
from datetime import datetime

class TodoItem(QFrame):
    def __init__(self, title, description, createdDate, dueDate=None):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Top of the task
        topLayout = QHBoxLayout()
        titleLabel = QLabel(f"<b>{title}</b>")
        titleLabel.setObjectName("TodoTitle")
        self.completeCheckbox = QCheckBox()
        self.completeCheckbox.setObjectName("TodoCheckbox")

        topLayout.addWidget(titleLabel)
        topLayout.addStretch()             
        topLayout.addWidget(self.completeCheckbox)
        layout.addLayout(topLayout)

        # Description 
        if description:
            descLabel = QLabel(description)
            descLabel.setWordWrap(True)
            descLabel.setObjectName("TodoDescription")
            layout.addWidget(descLabel)

        # Dates
        datesLayout = QHBoxLayout()

        createdLabel = QLabel(f"Created: {createdDate}")
        createdLabel.setObjectName("TodoCreatedDate")

        dueLabel = QLabel(f"Due: {dueDate}") if dueDate else QLabel("")
        dueLabel.setObjectName("TodoDueDate")
        dueLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

        datesLayout.addWidget(createdLabel)
        datesLayout.addStretch()  # push due date to the right
        datesLayout.addWidget(dueLabel)
        layout.addLayout(datesLayout)

        # Task styling
        self.setObjectName("TodoItem")

    def isCompleted(self):
        return self.completeCheckbox.isChecked()


class TodoPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)

        mainLayout = QVBoxLayout(self)

        # Header
        headerLayout = QHBoxLayout()
        title = QLabel("<b>Todo List</b>")

        self.toggleAddButton = QPushButton("+")
        self.toggleAddButton.setFixedSize(24, 24)
        self.toggleAddButton.clicked.connect(self.toggleAddPanel)

        headerLayout.addWidget(title)
        headerLayout.addStretch()
        headerLayout.addWidget(self.toggleAddButton)
        mainLayout.addLayout(headerLayout)

        # Add tasks panel
        self.addTaskPanel = QFrame()
        self.addTaskPanel.setObjectName("AddTaskPanel")
        addLayout = QVBoxLayout(self.addTaskPanel)

        # Task title input
        self.titleInput = QLineEdit()
        self.titleInput.setPlaceholderText("Task title")

        # Task description input
        self.descInput = QTextEdit()
        self.descInput.setPlaceholderText("Description")
        self.descInput.setFixedHeight(40)

        # Horizontal layout for toggle, label and date
        dueLayout = QHBoxLayout()

        # due date toggle button
        self.toggleDueButton = QPushButton("OFF")
        self.toggleDueButton.setCheckable(True)
        self.toggleDueButton.setFixedHeight(28)
        self.toggleDueButton.setObjectName("toggleDueButton")
        self.toggleDueButton.clicked.connect(self.toggleDueDate)

        # Due date label next to toggle button
        dueLabel = QLabel("Due Date:")
        dueLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        dueLabel.setStyleSheet("color: #fff;")

        # Due date input fills remaining space
        self.dueDateInput = QDateEdit()
        self.dueDateInput.setCalendarPopup(False)
        self.dueDateInput.setButtonSymbols(QDateEdit.ButtonSymbols.NoButtons)
        self.dueDateInput.setDate(QDate.currentDate())
        self.dueDateInput.setEnabled(False)
        self.dueDateInput.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dueDateInput.setMinimumWidth(150)  

        # Add widgets to horizontal layout
        dueLayout.addWidget(self.toggleDueButton)
        dueLayout.addWidget(dueLabel)
        dueLayout.addWidget(self.dueDateInput)

        # Add task button
        addTaskButton = QPushButton("Add Task")
        addTaskButton.setObjectName("addTaskButton")
        addTaskButton.clicked.connect(self.addTask)

        # Add widgets to vertical layout
        addLayout.addWidget(self.titleInput)
        addLayout.addWidget(self.descInput)
        addLayout.addLayout(dueLayout)
        addLayout.addWidget(addTaskButton)

        self.addTaskPanel.setVisible(False)
        mainLayout.addWidget(self.addTaskPanel)

        # Scrollable tasks
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.taskContainer = QWidget()
        self.taskLayout = QVBoxLayout(self.taskContainer)
        self.taskLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrollArea.setWidget(self.taskContainer)
        mainLayout.addWidget(self.scrollArea)

        # Footer - delete completed tasks
        clearButton = QPushButton("Delete Completed Tasks")
        clearButton.clicked.connect(self.deleteCompletedTasks)
        mainLayout.addWidget(clearButton)

    def toggleAddPanel(self):
        visible = self.addTaskPanel.isVisible()
        self.addTaskPanel.setVisible(not visible)
        self.toggleAddButton.setText("×" if not visible else "+")

    def toggleDueDate(self):
        enabled = self.dueDateInput.isEnabled()
        self.dueDateInput.setEnabled(not enabled)
        self.toggleDueButton.setText("ON " if not enabled else "OFF")

    def addTask(self):
        title = self.titleInput.text().strip()
        description = self.descInput.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Error", "Task title is required.")
            return

        created_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        due_date = None
        if self.dueDateInput.isEnabled() and self.dueDateInput.date().isValid():
            due_date = self.dueDateInput.date().toString("yyyy-MM-dd")

        task = TodoItem(title, description, created_date, due_date)
        self.taskLayout.addWidget(task)

        # Reset 
        self.titleInput.clear()
        self.descInput.clear()
        self.dueDateInput.setDate(QDate.currentDate())
        self.dueDateInput.setEnabled(False)
        self.toggleDueButton.setChecked(False)
        self.toggleDueButton.setText("OFF")
        self.addTaskPanel.setVisible(False)
        self.toggleAddButton.setText("+")

    def deleteCompletedTasks(self):
        for i in reversed(range(self.taskLayout.count())):
            widget = self.taskLayout.itemAt(i).widget()
            if widget and widget.isCompleted():
                widget.setParent(None)
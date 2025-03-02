# Federal-Retirement-Automationv2/gui/login_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        # Set a fixed size for the dialog
        self.setFixedSize(300, 200)  # Width: 300px, Height: 200px
        self.center()  # Center the dialog on the screen

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        # Hardcoded users for demonstration
        self.users = {
            "employee": {"password": "emp123", "role": "employee"},
            "processor": {"password": "proc123", "role": "processor"},
            "supervisor": {"password": "super123", "role": "supervisor"}
        }

    def center(self):
        """Center the dialog on the screen using QGuiApplication and QScreen."""
        # Get the geometry of the dialog
        frame_geometry = self.frameGeometry()
        # Get the primary screen's center
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_point = screen_geometry.center()
        # Move the dialog's center to the screen's center
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.users and self.users[username]["password"] == password:
            self.role = self.users[username]["role"]
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
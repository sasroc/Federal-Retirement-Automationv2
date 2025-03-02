# Federal-Retirement-Automationv2/gui/login_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QPropertyAnimation, QSize
from PyQt6.QtGui import QGuiApplication, QColor, QFont
import sys

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        # Set a fixed size for the dialog
        self.setFixedSize(300, 200)  # Width: 300px, Height: 200px
        self.center()  # Center the dialog on the screen

        # Apply modern dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2f;  /* Dark background matching the app */
                border-radius: 10px;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #333333;
                border: 2px solid #777777;
                border-radius: 8px;
                padding: 6px;
                color: #ffffff;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;  /* Green border on focus for modern look */
                background-color: #404040;
            }
            QLineEdit::placeholder {
                color: #AAAAAA;
                font-style: italic;
            }
            QPushButton {
                background-color: #4CAF50;  /* Green button for modern design */
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Slightly darker green on hover */
            }
            QPushButton:pressed {
                background-color: #3d8b40;  /* Even darker green when pressed */
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        # Title label
        title_label = QLabel("Federal Retirement Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMaximumHeight(170)  # Consistent height for modern look
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMaximumHeight(40)  # Consistent height for modern look
        layout.addWidget(self.password_input)

        # Login button with animation
        self.login_btn = QPushButton("Login")
        self.login_btn.setMaximumHeight(100)  # Consistent height
        self.login_btn.clicked.connect(self.login)
        # Add subtle scale animation on hover
        self.add_hover_animation(self.login_btn)
        layout.addWidget(self.login_btn)

        # Hardcoded users for demonstration
        self.users = {
            "employee": {"password": "emp123", "role": "employee"},
            "processor": {"password": "proc123", "role": "processor"},
            "supervisor": {"password": "super123", "role": "supervisor"}
        }

    def center(self):
        """Center the dialog on the screen using QGuiApplication and QScreen."""
        frame_geometry = self.frameGeometry()
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def add_hover_animation(self, button):
        """Add a subtle scale animation on hover for modern interactivity."""
        animation = QPropertyAnimation(button, b"size")
        animation.setDuration(200)  # Animation duration in milliseconds
        button.enterEvent = lambda event: animation.setStartValue(button.size()) or animation.setEndValue(QSize(310, 45)) or animation.start()
        button.leaveEvent = lambda event: animation.setStartValue(button.size()) or animation.setEndValue(QSize(300, 40)) or animation.start()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.users and self.users[username]["password"] == password:
            self.role = self.users[username]["role"]
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.", 
                                QMessageBox.Icon.Critical, 
                                QMessageBox.StandardButton.Ok)
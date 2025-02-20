from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
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

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.users and self.users[username]["password"] == password:
            self.role = self.users[username]["role"]
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
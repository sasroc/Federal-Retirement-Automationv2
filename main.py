# Federal-Retirement-Automationv2/main.py

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog
from gui.employee_portal import EmployeePortal
from gui.processor_dashboard import ProcessorDashboard
from gui.supervisor_dashboard import SupervisorDashboard
from gui.login_dialog import LoginDialog
from utils.database import create_database
import sys  # Import sys to handle application exit

class RetirementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Federal Retirement Automation")
        self.setGeometry(100, 100, 800, 600)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Widgets will be initialized with username after login
        self.employee_portal = None
        self.processor_dashboard = None
        self.supervisor_dashboard = None

        # Show login dialog
        login_dialog = LoginDialog(self)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            role = login_dialog.role
            username = login_dialog.username_input.text()  # Get username from login dialog
            if role == "employee":
                self.employee_portal = EmployeePortal(username)
                self.stack.addWidget(self.employee_portal)
                self.stack.setCurrentWidget(self.employee_portal)
                self.showMaximized()
            elif role == "processor":
                self.processor_dashboard = ProcessorDashboard(username)
                self.stack.addWidget(self.processor_dashboard)
                self.stack.setCurrentWidget(self.processor_dashboard)
                self.showMaximized()
            elif role == "supervisor":
                self.supervisor_dashboard = SupervisorDashboard(username)
                self.stack.addWidget(self.supervisor_dashboard)
                self.stack.setCurrentWidget(self.supervisor_dashboard)
                self.showMaximized()
        else:
            # If login fails or is canceled, exit the application entirely
            self.close()
            sys.exit(0)  # Explicitly terminate the application

if __name__ == "__main__":
    create_database()  # Ensure database is created before app starts
    app = QApplication(sys.argv)  # Pass sys.argv to QApplication
    window = RetirementApp()
    sys.exit(app.exec())  # Use sys.exit to properly terminate with app.exec()
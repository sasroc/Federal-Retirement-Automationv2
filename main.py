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

        # Create widgets for each role
        self.employee_portal = EmployeePortal()
        self.processor_dashboard = ProcessorDashboard()
        self.supervisor_dashboard = SupervisorDashboard()

        # Add widgets to stack
        self.stack.addWidget(self.employee_portal)
        self.stack.addWidget(self.processor_dashboard)
        self.stack.addWidget(self.supervisor_dashboard)

        # Show login dialog
        login_dialog = LoginDialog(self)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            role = login_dialog.role
            if role == "employee":
                self.stack.setCurrentWidget(self.employee_portal)
            elif role == "processor":
                self.stack.setCurrentWidget(self.processor_dashboard)
            elif role == "supervisor":
                self.stack.setCurrentWidget(self.supervisor_dashboard)
        else:
            # If login fails or is canceled, exit the application entirely
            self.close()
            sys.exit(0)  # Explicitly terminate the application

if __name__ == "__main__":
    create_database()  # Ensure database is created before app starts
    app = QApplication(sys.argv)  # Pass sys.argv to QApplication
    window = RetirementApp()
    window.show()
    sys.exit(app.exec())  # Use sys.exit to properly terminate with app.exec()
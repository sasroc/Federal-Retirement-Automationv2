# Federal-Retirement-Automationv2/main.py

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog
from gui.employee_portal import EmployeePortal
from gui.processor_dashboard import ProcessorDashboard
from gui.supervisor_dashboard import SupervisorDashboard
from gui.login_dialog import LoginDialog
from utils.database import create_database
import sys

class RetirementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Federal Retirement Automation")
        self.setGeometry(100, 100, 800, 600)  # Initial geometry, but hidden until login
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.employee_portal = None
        self.processor_dashboard = None
        self.supervisor_dashboard = None

        # Show only the login dialog initially, hide the main window
        self.hide()  # Hide the main window until login is successful
        self.show_login_dialog()

    def show_login_dialog(self):
        """Show the login dialog and initialize the appropriate dashboard after login."""
        login_dialog = LoginDialog(self)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            role = login_dialog.role
            username = login_dialog.username_input.text()
            if role == "employee":
                self.employee_portal = EmployeePortal(username)
                self.stack.addWidget(self.employee_portal)
                self.stack.setCurrentWidget(self.employee_portal)
            elif role == "processor":
                self.processor_dashboard = ProcessorDashboard(username)
                self.stack.addWidget(self.processor_dashboard)
                self.stack.setCurrentWidget(self.processor_dashboard)
            elif role == "supervisor":
                self.supervisor_dashboard = SupervisorDashboard(username)
                self.stack.addWidget(self.supervisor_dashboard)
                self.stack.setCurrentWidget(self.supervisor_dashboard)
            # Show and maximize the main window after successful login
            self.show()
            self.showMaximized()
            QApplication.processEvents()  # Ensure layout updates after maximizing
        else:
            self.close()
            sys.exit(0)

    def logout(self):
        """Handle logout by clearing the current dashboard and showing the login dialog."""
        # Clear the current stack
        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        # Reset window state and show login dialog
        self.hide()  # Hide the main window before showing login
        self.show_login_dialog()

if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = RetirementApp()
    sys.exit(app.exec())
# Federal-Retirement-Automationv2/main.py

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog
from PyQt6.QtCore import Qt, Qt as QtCore  # Explicitly import Qt for WindowState
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
        # Set an initial size that should fit most screens; avoid conflicts with minimum size
        self.setGeometry(100, 100, 1280, 720)  # Reduced initial height to avoid issues
        self.setMinimumSize(800, 600)  # Set a reasonable minimum size
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
            # Show the window and adjust size smoothly
            self.show()
            # Instead of showMaximized(), restore to normal state first, then maximize
            self.setWindowState(Qt.WindowState.WindowNoState)  # Reset to normal state
            self.showMaximized()  # Now maximize safely
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

        # Reset window state and size to avoid geometry conflicts
        self.setWindowState(Qt.WindowState.WindowNoState)  # Reset to normal state
        self.resize(1280, 720)  # Reset to a safe size
        self.move(100, 100)  # Reset position
        self.hide()  # Hide the main window before showing login
        self.show_login_dialog()

if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = RetirementApp()
    sys.exit(app.exec())
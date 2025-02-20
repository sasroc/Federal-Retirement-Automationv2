from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog
from gui.employee_portal import EmployeePortal
from gui.processor_dashboard import ProcessorDashboard
from gui.supervisor_dashboard import SupervisorDashboard
from gui.login_dialog import LoginDialog  # Assuming you saved the login dialog in gui/login_dialog.py

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
            # If login fails or is canceled, close the application
            self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = RetirementApp()
    window.show()
    app.exec()
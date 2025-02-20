from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.employee_portal import EmployeePortal
from gui.processor_dashboard import ProcessorDashboard
from gui.supervisor_dashboard import SupervisorDashboard
from utils.database import create_database

class RetirementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Federal Retirement Automation")
        self.setGeometry(100, 100, 800, 600)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.employee_portal = EmployeePortal()
        self.processor_dashboard = ProcessorDashboard()
        self.supervisor_dashboard = SupervisorDashboard()

        self.stack.addWidget(self.employee_portal)
        self.stack.addWidget(self.processor_dashboard)
        self.stack.addWidget(self.supervisor_dashboard)

        # Simulate role-based access (expand with authentication later)
        self.stack.setCurrentWidget(self.employee_portal)

if __name__ == "__main__":
    create_database()
    app = QApplication([])
    window = RetirementApp()
    window.show()
    app.exec()
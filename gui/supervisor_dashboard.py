from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import sqlite3
from utils.calculations import calculate_age

class DetailsDialog(QDialog):
    def __init__(self, application_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Application {application_id} Details")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Applications WHERE application_id = ?", (application_id,))
        app = cursor.fetchone()
        cursor.execute("SELECT * FROM Employees WHERE employee_id = ?", (app[1],))
        emp = cursor.fetchone()
        conn.close()

        age = calculate_age(emp[3])
        details = f"""
        Application ID: {app[0]}
        Employee: {emp[1]} {emp[2]}
        Date of Birth: {emp[3]} (Age: {age})
        Years of Service: {app[2]}
        Retirement Date: {app[3]}
        High-3 Salary: ${app[4]:,.2f}
        Submission Date: {app[5]}
        Status: {app[6]}
        Benefits: ${app[7]:,.2f} (if calculated)
        Note: Benefits are typically 1% of high-3 salary per year of service, or 1.1% if age >= 62 and years >= 20.
        """
        layout.addWidget(QLabel(details, styleSheet="color: #ffffff; font-size: 14px;"))

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

class SupervisorDashboard(QWidget):
    def __init__(self):
        super().__init__()
        # Set dark background to match EmployeePortal
        self.setStyleSheet("""
            background-color: #1e1e2f;  /* Dark background for modern look */
            font-family: Arial;
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        # Table setup with dark background and white text
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["App ID", "Name", "Age", "Years", "Salary", "Benefits", "Actions"])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2f;
                color: #ffffff;  /* White text for table content */
                font-size: 14px;
                border: 2px solid #777777;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #333333;  /* Dark grey for headers */
                color: #ffffff;  /* White text for headers */
                padding: 8px;
                border: 1px solid #777777;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::alternate {
                background-color: #444444;  /* Dark grey for alternate rows */
                color: #ffffff;  /* White text for alternate rows */
            }
        """)
        layout.addWidget(self.table, stretch=1)

        # Refresh button with styling matching EmployeePortal
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 14px;
        """)
        refresh_btn.clicked.connect(self.load_applications)
        layout.addWidget(refresh_btn, stretch=0)

        self.load_applications()

    def load_applications(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT a.application_id, e.first_name || ' ' || e.last_name, e.dob, a.years_service, a.salary, a.benefits "
                       "FROM Applications a JOIN Employees e ON a.employee_id = e.employee_id WHERE a.status = 'calculated'")
        apps = cursor.fetchall()
        self.table.setRowCount(len(apps))
        
        for row, app in enumerate(apps):
            age = calculate_age(app[2])
            for col, data in enumerate([app[0], app[1], age, app[3], f"${app[4]:,.2f}", f"${app[5]:,.2f}" if app[5] else "N/A"]):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

            # Action buttons
            view_btn = QPushButton("View Details")
            view_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 5px; border-radius: 3px;")
            view_btn.clicked.connect(lambda _, a=app: self.view_details(a[0]))

            approve_btn = QPushButton("Approve")
            approve_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px;")
            approve_btn.clicked.connect(lambda _, a=app: self.approve_application(a))

            deny_btn = QPushButton("Deny")
            deny_btn.setStyleSheet("background-color: #F44336; color: white; padding: 5px; border-radius: 3px;")
            deny_btn.clicked.connect(lambda _, a=app: self.deny_application(a))

            btn_layout = QHBoxLayout()
            btn_layout.addWidget(view_btn)
            btn_layout.addWidget(approve_btn)
            btn_layout.addWidget(deny_btn)
            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            self.table.setCellWidget(row, 6, btn_widget)
        conn.close()

    def view_details(self, application_id):
        dialog = DetailsDialog(application_id, self)
        dialog.exec()

    def approve_application(self, app):
        confirm = QMessageBox.question(self, "Confirm Approval", "Are you sure you want to approve this application?")
        if confirm == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Applications SET status = 'approved' WHERE application_id = ?", (app[0],))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Approval", "Application approved.")
            self.load_applications()

    def deny_application(self, app):
        confirm = QMessageBox.question(self, "Confirm Denial", "Are you sure you want to deny this application?")
        if confirm == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Applications SET status = 'denied' WHERE application_id = ?", (app[0],))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Denial", "Application denied.")
            self.load_applications()
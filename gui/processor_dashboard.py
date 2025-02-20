from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, QLabel
from PyQt6.QtCore import Qt
import sqlite3
from utils.calculations import calculate_age, is_eligible, calculate_annuity

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
        years_service = app[2]
        eligible = is_eligible(age, years_service)
        annuity = calculate_annuity(years_service, app[4], age) if eligible else 0

        details = f"""
        Application ID: {app[0]}
        Employee: {emp[1]} {emp[2]}
        Date of Birth: {emp[3]} (Age: {age})
        Years of Service: {years_service}
        Retirement Date: {app[3]}
        High-3 Salary: ${app[4]:,.2f}
        Submission Date: {app[5]}
        Status: {app[6]}
        Eligible: {'Yes' if eligible else 'No'}
        Benefits: ${annuity:,.2f} (if eligible)
        """
        layout.addWidget(QLabel(details, styleSheet="color: #ffffff; font-size: 14px;"))

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

class ProcessorDashboard(QWidget):
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
                       "FROM Applications a JOIN Employees e ON a.employee_id = e.employee_id WHERE a.status = 'submitted'")
        apps = cursor.fetchall()
        self.table.setRowCount(len(apps))
        
        for row, app in enumerate(apps):
            age = calculate_age(app[2])
            years_service = app[3]
            eligible = is_eligible(age, years_service)
            annuity = calculate_annuity(years_service, app[4], age) if eligible else 0

            # Update application status and benefits in database
            cursor.execute("UPDATE Applications SET status = ?, benefits = ? WHERE application_id = ?",
                           ('calculated' if eligible else 'ineligible', annuity, app[0]))
            conn.commit()

            for col, data in enumerate([app[0], app[1], age, years_service, f"${app[4]:,.2f}", f"${annuity:,.2f}" if eligible else "N/A"]):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

            view_btn = QPushButton("View Details")
            view_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 5px; border-radius: 3px;")
            view_btn.clicked.connect(lambda _, a=app: self.view_details(a[0]))

            self.table.setCellWidget(row, 6, view_btn)
        conn.close()

    def view_details(self, application_id):
        dialog = DetailsDialog(application_id, self)
        dialog.exec()
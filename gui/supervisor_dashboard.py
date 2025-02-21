from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import sqlite3
from utils.calculations import calculate_age

class DetailsDialog(QDialog):
    def __init__(self, application_id, parent=None):
        super().__init__(parent)
        self.application_id = application_id
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
        # Handle benefits safely
        benefits = app[7] if app[7] is not None else 0.0
        try:
            benefits = float(benefits)
            benefits_str = f"${benefits:,.2f}"
        except (ValueError, TypeError):
            benefits_str = "N/A"

        details = f"""
        Application ID: {app[0]}
        Employee: {emp[1]} {emp[2]}
        Date of Birth: {emp[3]} (Age: {age})
        Years of Service: {app[2]}
        Retirement Date: {app[3]}
        High-3 Salary: ${app[4]:,.2f}
        Submission Date: {app[5]}
        Status: {app[6]}
        Benefits: {benefits_str} (if calculated)
        Agency: {app[8]}
        Position: {app[9]}
        Survivor Benefit: {app[10]}
        FEHB: {'Yes' if app[11] else 'No'}
        FEGLI: {'Yes' if app[12] else 'No'}
        Bank Name: {app[13]}
        Account Number: {app[14]}
        Routing Number: {app[15]}
        Military Service: {'Yes' if app[16] else 'No'}
        Military Retired Pay: {'Yes' if app[17] else 'No'}
        Waived Military Pay: {'Yes' if app[18] else 'No'}
        Sick Leave Hours: {app[19]}
        Court Orders: {'Yes' if app[20] else 'No'}
        """
        layout.addWidget(QLabel(details, styleSheet="color: #ffffff; font-size: 14px;"))

        # Action buttons
        btn_layout = QHBoxLayout()
        
        approve_btn = QPushButton("Approve")
        approve_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px;")
        approve_btn.clicked.connect(self.approve_application)
        btn_layout.addWidget(approve_btn)

        deny_btn = QPushButton("Deny")
        deny_btn.setStyleSheet("background-color: #F44336; color: white; padding: 5px; border-radius: 3px;")
        deny_btn.clicked.connect(self.deny_application)
        btn_layout.addWidget(deny_btn)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def approve_application(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Applications SET status = 'Approved' WHERE application_id = ?", (self.application_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Approval", "Application approved.")
        self.accept()
        self.parent().load_applications()

    def deny_application(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Applications SET status = 'Denied' WHERE application_id = ?", (self.application_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Denial", "Application denied.")
        self.accept()
        self.parent().load_applications()

class SupervisorDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1e1e2f; font-family: Arial;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)  # Added Status column
        self.table.setHorizontalHeaderLabels(["App ID", "Name", "Age", "Years", "Salary", "Benefits", "Status", "Actions"])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-size: 14px;
                border: 2px solid #777777;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #777777;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::alternate {
                background-color: #444444;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.table, stretch=1)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 12px; border-radius: 8px; font-size: 14px;")
        refresh_btn.clicked.connect(self.load_applications)
        layout.addWidget(refresh_btn, stretch=0)

        self.load_applications()

    def load_applications(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT a.application_id, e.first_name || ' ' || e.last_name, e.dob, a.years_service, a.salary, a.benefits, a.status "
                       "FROM Applications a JOIN Employees e ON a.employee_id = e.employee_id WHERE a.status IN ('pending approval', 'Approved', 'Denied')")
        apps = cursor.fetchall()
        self.table.setRowCount(len(apps))
        
        for row, app in enumerate(apps):
            age = calculate_age(app[2])
            benefits = app[5] if app[5] is not None else 0.0
            try:
                benefits_str = f"${float(benefits):,.2f}"
            except (ValueError, TypeError):
                benefits_str = "N/A"
            for col, data in enumerate([app[0], app[1], age, app[3], f"${app[4]:,.2f}", benefits_str, app[6]]):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

            view_btn = QPushButton("View Details")
            view_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 5px; border-radius: 3px;")
            view_btn.clicked.connect(lambda _, a=app: self.view_details(a[0]))
            self.table.setCellWidget(row, 7, view_btn)
        conn.close()

    def view_details(self, application_id):
        dialog = DetailsDialog(application_id, self)
        dialog.exec()
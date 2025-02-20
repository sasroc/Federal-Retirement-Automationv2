from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
import sqlite3
from utils.calculations import calculate_age, is_eligible, calculate_annuity

class ProcessorDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f0f4f8;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["App ID", "Name", "Age", "Years", "Retirement Date", "Salary", "Action"])
        layout.addWidget(self.table)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        refresh_btn.clicked.connect(self.load_applications)
        layout.addWidget(refresh_btn)

        self.load_applications()

    def load_applications(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT a.application_id, e.first_name || ' ' || e.last_name, e.dob, a.years_service, a.retirement_date, a.salary, a.status "
                       "FROM Applications a JOIN Employees e ON a.employee_id = e.employee_id WHERE a.status = 'submitted'")
        apps = cursor.fetchall()
        self.table.setRowCount(len(apps))
        for row, app in enumerate(apps):
            age = calculate_age(app[2])
            for col, data in enumerate([app[0], app[1], age, app[3], app[4], app[5]]):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
            verify_btn = QPushButton("Verify")
            verify_btn.setStyleSheet("background-color: #FF9800; color: white;")
            verify_btn.clicked.connect(lambda _, r=row, a=app: self.verify_eligibility(r, a))
            self.table.setCellWidget(row, 6, verify_btn)
            calc_btn = QPushButton("Calculate")
            calc_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            calc_btn.clicked.connect(lambda _, r=row, a=app: self.calculate_benefits(r, a))
            self.table.setCellWidget(row, 6, calc_btn if app[6] == 'eligible' else verify_btn)
        conn.close()

    def verify_eligibility(self, row, app):
        age = calculate_age(app[2])
        eligible = is_eligible(age, app[3])
        status = 'eligible' if eligible else 'ineligible'
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Applications SET status = ? WHERE application_id = ?", (status, app[0]))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Verification", f"Employee is {status}.")
        self.load_applications()


    def calculate_benefits(self, row, app):
        age = calculate_age(app[2])
        annuity = calculate_annuity(app[3], app[5], age)
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Applications SET status = 'calculated', benefits = ? WHERE application_id = ?", (annuity, app[0]))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Benefits", f"Annual Annuity: ${annuity:,.2f}")
        self.load_applications()
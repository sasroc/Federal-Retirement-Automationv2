from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import sqlite3
from utils.calculations import calculate_age, is_eligible, calculate_annuity
from utils.dialogs import NoteDialog, ViewNotesDialog, NoteHistoryDialog

class DetailsDialog(QDialog):
    def __init__(self, application_id, parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.setWindowTitle(f"Application {application_id} Details")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        try:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT application_id, employee_id, years_service, retirement_date, salary, submission_date, status, 
                       agency, position_title, survivor_benefit, fehb_continue, fegli_continue, bank_name, 
                       account_number, routing_number, served_military, military_retired_pay, waived_military_pay, 
                       sick_leave_hours, has_court_orders, benefits, hire_date
                FROM Applications WHERE application_id = ?""", (application_id,))
            app = cursor.fetchone()

            cursor.execute("""
                SELECT employee_id, first_name, last_name, dob, ssn, address, city, state, zip_code, phone, email, 
                       is_us_citizen
                FROM Employees WHERE employee_id = ?""", (app[1],))
            emp = cursor.fetchone()
            conn.close()

            if not app or not emp:
                layout.addWidget(QLabel("No application or employee data found.", styleSheet="color: #ffffff; font-size: 18px;"))
            else:
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
                Agency: {app[7]}
                Position: {app[8]}
                Survivor Benefit: {app[9]}
                FEHB: {'Yes' if app[10] else 'No'}
                FEGLI: {'Yes' if app[11] else 'No'}
                Bank Name: {app[12]}
                Account Number: {app[13]}
                Routing Number: {app[14]}
                Military Service: {'Yes' if app[15] else 'No'}
                Military Retired Pay: {'Yes' if app[16] else 'No'}
                Waived Military Pay: {'Yes' if app[17] else 'No'}
                Sick Leave Hours: {app[18]}
                Court Orders: {'Yes' if app[19] else 'No'}
                """
                layout.addWidget(QLabel(details, styleSheet="color: #ffffff; font-size: 16px;"))

            btn_layout = QHBoxLayout()
            submit_btn = QPushButton("Submit to Supervisor")
            submit_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px;")
            submit_btn.clicked.connect(self.submit_to_supervisor)
            btn_layout.addWidget(submit_btn)

            more_info_btn = QPushButton("Needs Additional Information")
            more_info_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 5px; border-radius: 3px;")
            more_info_btn.clicked.connect(self.needs_more_info)
            btn_layout.addWidget(more_info_btn)

            close_btn = QPushButton("Close")
            close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
            close_btn.clicked.connect(self.close)
            btn_layout.addWidget(close_btn)

            layout.addLayout(btn_layout)

        except sqlite3.Error as e:
            layout.addWidget(QLabel(f"Database error: {str(e)}", styleSheet="color: #ffffff; font-size: 14px;"))
        except Exception as e:
            layout.addWidget(QLabel(f"Error: {str(e)}", styleSheet="color: #ffffff; font-size: 14px;"))

    def submit_to_supervisor(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM Applications WHERE application_id = ?", (self.application_id,))
        current_status = cursor.fetchone()[0]
        
        if current_status == "Denied by Supervisor":
            # Clear denial_note but preserve note_history
            cursor.execute("""
                UPDATE Applications 
                SET status = 'Pending', denial_note = NULL 
                WHERE application_id = ?
            """, (self.application_id,))
            QMessageBox.information(self, "Success", "Application resubmitted to Supervisor with denial note cleared.")
        else:
            cursor.execute("UPDATE Applications SET status = 'Pending' WHERE application_id = ?", (self.application_id,))
            QMessageBox.information(self, "Success", "Application submitted to Supervisor.")
        
        conn.commit()
        conn.close()
        self.accept()
        self.parent().load_applications()

    def needs_more_info(self):
        note_dialog = NoteDialog(self.application_id, note_type="additional_info", parent=self)
        if note_dialog.exec() == QDialog.DialogCode.Accepted:
            self.accept()
            self.parent().load_applications()

class ProcessorDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1e1e2f; font-family: Arial;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(10)  # Increased to 10 for Note History
        self.table.setHorizontalHeaderLabels(["App ID", "Name", "Age", "Years", "Salary", "Benefits", "Status", "Actions", "Notes", "Note History"])
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
        try:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.application_id, e.first_name || ' ' || e.last_name, e.dob, a.years_service, a.salary, a.benefits, a.status 
                FROM Applications a 
                JOIN Employees e ON a.employee_id = e.employee_id 
                WHERE a.status IN ('Processing', 'Needs Additional Info', 'Denied by Supervisor')
            """)
            apps = cursor.fetchall()
            
            self.table.setRowCount(len(apps))
            
            for row, app in enumerate(apps):
                if not app:
                    continue
                age = calculate_age(app[2])
                years_service = app[3]
                eligible = is_eligible(age, years_service)
                annuity = calculate_annuity(years_service, app[4], age) if eligible else 0

                if eligible and (app[5] is None or app[5] == 0):
                    cursor.execute("UPDATE Applications SET benefits = ? WHERE application_id = ?", (annuity, app[0]))
                    conn.commit()

                for col, data in enumerate([app[0], app[1], age, years_service, f"${app[4]:,.2f}", f"${annuity:,.2f}" if eligible else "N/A", app[6]]):
                    item = QTableWidgetItem(str(data) if data is not None else "N/A")
                    self.table.setItem(row, col, item)

                view_btn = QPushButton("View Details")
                view_btn.setStyleSheet("""
                    background-color: #2196F3;
                    color: #FFFFFF;
                    padding: 2px 20px;
                    border-radius: 3px;
                    font-size: 12px;
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                    border: 2px solid #FFFFFF;
                    min-height: 40px;
                """)
                view_btn.clicked.connect(lambda _, a=app: self.view_details(a[0]))
                self.table.setCellWidget(row, 7, view_btn)

                notes_btn = QPushButton("View Notes")
                notes_btn.setStyleSheet("""
                    background-color: #FFEB3B;
                    color: #000000;
                    padding: 2px 20px;
                    border-radius: 3px;
                    font-size: 12px;
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                    border: 2px solid #000000;
                    min-height: 40px;
                """)
                notes_btn.clicked.connect(lambda _, aid=app[0]: self.view_application_notes(aid))
                self.table.setCellWidget(row, 8, notes_btn)

                history_btn = QPushButton("View History")
                history_btn.setStyleSheet("""
                    background-color: #808080;  /* Grey */
                    color: #FFFFFF;  /* White text */
                    padding: 2px 20px;
                    border-radius: 3px;
                    font-size: 12px;
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                    border: 2px solid #FFFFFF;  /* White border */
                    min-height: 40px;
                """)
                history_btn.clicked.connect(lambda _, aid=app[0]: self.view_note_history(aid))
                self.table.setCellWidget(row, 9, history_btn)

                self.table.setRowHeight(row, 60)
                self.table.setColumnWidth(7, 150)
                self.table.setColumnWidth(8, 150)
                self.table.setColumnWidth(9, 150)

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading applications: {str(e)}")
            conn.close()

    def view_details(self, application_id):
        dialog = DetailsDialog(application_id, self)
        dialog.exec()

    def view_application_notes(self, application_id):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM Applications WHERE application_id = ?", (application_id,))
        status = cursor.fetchone()[0]
        conn.close()
        
        note_type = "denial" if status == "Denied by Supervisor" else "additional_info"
        dialog = ViewNotesDialog(application_id, note_type=note_type, parent=self)
        dialog.exec()

    def view_note_history(self, application_id):
        dialog = NoteHistoryDialog(application_id, parent=self)
        dialog.exec()
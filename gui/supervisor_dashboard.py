from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, QLabel, QHBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
import sqlite3
from utils.calculations import calculate_age

class NoteDialog(QDialog):
    def __init__(self, application_id, parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.setWindowTitle("Add Denial Note")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Text area for note input
        self.note_text = QTextEdit()
        layout.addWidget(QLabel("Enter a note for denying this application:", styleSheet="color: #ffffff; font-size: 14px;"))
        layout.addWidget(self.note_text)

        # Save button
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px;")
        save_btn.clicked.connect(self.save_note)
        layout.addWidget(save_btn)

    def save_note(self):
        note = self.note_text.toPlainText().strip()
        if note:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            # Update or insert the note into the Applications table for this specific application
            cursor.execute("""
                UPDATE Applications SET denial_note = ?, status = 'Denied' WHERE application_id = ?
            """, (note, self.application_id))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Note saved successfully. Application denied.")
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a note before saving.")

class ViewNotesDialog(QDialog):
    def __init__(self, application_id, parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.setWindowTitle(f"View Notes for Application {application_id}")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT denial_note FROM Applications WHERE application_id = ?
        """, (application_id,))
        note = cursor.fetchone()
        conn.close()

        if note and note[0]:
            layout.addWidget(QLabel(f"Note:\n\n{note[0]}", styleSheet="color: #ffffff; font-size: 14px;"))
        else:
            layout.addWidget(QLabel("No notes available for this application.", styleSheet="color: #ffffff; font-size: 14px;"))

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

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
            
            # Explicitly select the columns we need from Applications, including denial_note
            cursor.execute("""
                SELECT application_id, employee_id, years_service, retirement_date, salary, submission_date, status, 
                       agency, position_title, survivor_benefit, fehb_continue, fegli_continue, bank_name, 
                       account_number, routing_number, served_military, military_retired_pay, waived_military_pay, 
                       sick_leave_hours, has_court_orders, benefits, hire_date, denial_note
                FROM Applications WHERE application_id = ?""", (application_id,))
            app = cursor.fetchone()

            # Explicitly select the columns we need from Employees
            cursor.execute("""
                SELECT employee_id, first_name, last_name, dob, ssn, address, city, state, zip_code, phone, email, 
                       is_us_citizen
                FROM Employees WHERE employee_id = ?""", (app[1],))
            emp = cursor.fetchone()
            conn.close()

            if not app or not emp:
                layout.addWidget(QLabel("No application or employee data found.", styleSheet="color: #ffffff; font-size: 14px;"))
            else:
                age = calculate_age(emp[3])  # dob is the 4th column (index 3) in Employees
                years_service = app[2]  # years_service is the 3rd column (index 2) in Applications
                benefits = app[20] if app[20] is not None else 0.0  # benefits is the 21st column (index 20)
                try:
                    benefits_str = f"${float(benefits):,.2f}"
                except (ValueError, TypeError):
                    benefits_str = "N/A"

                # Use the correct column indices or names for each field, matching the original format but with all fields
                details = f"""
                Application ID: {app[0]}
                Employee: {emp[1]} {emp[2]}
                Date of Birth: {emp[3]} (Age: {age})
                Years of Service: {years_service}
                Retirement Date: {app[3]}
                High-3 Salary: ${app[4]:,.2f}
                Submission Date: {app[5]}
                Status: {app[6]}
                Benefits: {benefits_str} (if calculated)
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
                layout.addWidget(QLabel(details, styleSheet="color: #ffffff; font-size: 14px;"))

            # Action buttons, now only in DetailsDialog, matching the original functionality
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

        except sqlite3.Error as e:
            layout.addWidget(QLabel(f"Database error: {str(e)}", styleSheet="color: #ffffff; font-size: 14px;"))
        except Exception as e:
            layout.addWidget(QLabel(f"Error: {str(e)}", styleSheet="color: #ffffff; font-size: 14px;"))

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
        # Prompt for a note before denying, then update status to 'Denied'
        note_dialog = NoteDialog(self.application_id, self)
        if note_dialog.exec() == QDialog.DialogCode.Accepted:
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

        # Table setup with dark background and white text, including Status and Notes columns
        self.table = QTableWidget()
        self.table.setColumnCount(9)  # Added a column for "Notes" actions
        self.table.setHorizontalHeaderLabels(["App ID", "Name", "Age", "Years", "Salary", "Benefits", "Status", "Actions", "Notes"])
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
        try:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            # Use explicit column names to match the Applications table schema, preserving the original behavior
            cursor.execute("""
                SELECT a.application_id, e.first_name || ' ' || e.last_name, e.dob, a.years_service, a.salary, a.benefits, a.status 
                FROM Applications a 
                JOIN Employees e ON a.employee_id = e.employee_id 
                WHERE a.status IN ('Pending', 'Approved', 'Denied')
            """)
            apps = cursor.fetchall()
            
            self.table.setRowCount(len(apps))
            
            for row, app in enumerate(apps):
                if not app:
                    continue
                age = calculate_age(app[2])  # dob is the 3rd column (index 2)
                benefits = app[5] if app[5] is not None else 0.0
                try:
                    benefits_str = f"${float(benefits):,.2f}"
                except (ValueError, TypeError):
                    benefits_str = "N/A"
                for col, data in enumerate([app[0], app[1], age, app[3], f"${app[4]:,.2f}", benefits_str, app[6]]):
                    item = QTableWidgetItem(str(data) if data is not None else "N/A")
                    self.table.setItem(row, col, item)

                # Actions column (column 7) - Show "View Details" button with clearly visible text
                view_btn = QPushButton("View Details")
                view_btn.setStyleSheet("""
                    background-color: #2196F3;
                    color: #FFFFFF;  /* Ensure white text for high contrast against blue background */
                    padding: 2px 20px;  /* Sufficient padding for height and width */
                    border-radius: 3px;
                    font-size: 12px;  /* Larger font size for better readability */
                    font-family: Arial, sans-serif;
                    font-weight: bold;  /* Make text bold for emphasis */
                    border: 2px solid #FFFFFF;  /* Bright border for visibility */
                    min-height: 40px;  /* Minimum height to ensure text fits */
                """)
                view_btn.clicked.connect(lambda _, a=app: self.view_details(a[0]))
                self.table.setCellWidget(row, 7, view_btn)

                # Notes column (column 8) - Add "View Notes" button with shaded yellow background
                notes_btn = QPushButton("View Notes")
                notes_btn.setStyleSheet("""
                    background-color: #FFEB3B;  /* Shaded yellow (e.g., light yellow) */
                    color: #000000;  /* Black text for high contrast against yellow background */
                    padding: 2px 20px;  /* Sufficient padding for height and width */
                    border-radius: 3px;
                    font-size: 12px;  /* Larger font size for better readability */
                    font-family: Arial, sans-serif;
                    font-weight: bold;  /* Make text bold for emphasis */
                    border: 2px solid #000000;  /* Black border for visibility */
                    min-height: 40px;  /* Minimum height to ensure text fits */
                """)
                notes_btn.clicked.connect(lambda _, aid=app[0]: self.view_application_notes(aid))
                self.table.setCellWidget(row, 8, notes_btn)

                # Set a larger row height to accommodate the buttons and ensure text visibility
                self.table.setRowHeight(row, 60)  # Adjust this value as needed for readability

            # Set wider widths for the 'Actions' (column 7) and 'Notes' (column 8) columns
            self.table.setColumnWidth(7, 150)  # Increase width to 150 pixels for 'Actions' (adjust as needed)
            self.table.setColumnWidth(8, 150)  # Increase width to 150 pixels for 'Notes' (adjust as needed)

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading applications: {str(e)}")
            conn.close()

    def view_details(self, application_id):
        dialog = DetailsDialog(application_id, self)
        dialog.exec()

    def view_application_notes(self, application_id):
        # Open a dialog to show the note for this specific application
        dialog = ViewNotesDialog(application_id, self)
        dialog.exec()

    def approve_application(self, app):
        confirm = QMessageBox.question(self, "Confirm Approval", "Are you sure you want to approve this application?")
        if confirm == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Applications SET status = 'Approved' WHERE application_id = ?", (app[0],))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Approval", "Application approved.")
            self.load_applications()

    def deny_application(self, app):
        # Prompt for a note before denying, then update status to 'Denied'
        note_dialog = NoteDialog(app[0], self)
        if note_dialog.exec() == QDialog.DialogCode.Accepted:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Applications SET status = 'Denied' WHERE application_id = ?", (app[0],))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Denial", "Application denied.")
            self.load_applications()
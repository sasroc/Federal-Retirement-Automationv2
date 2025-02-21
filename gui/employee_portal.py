from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFormLayout, QCheckBox, QDateEdit
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from models.employee import Employee
from models.application import Application
from utils.ocr_processor import extract_text_from_image, parse_ocr_text

class EmployeePortal(QWidget):
    def __init__(self):
        super().__init__()
        # Base stylesheet for the widget, ensuring a dark background for contrast
        self.setStyleSheet("""
            background-color: #1e1e2f;  /* Dark background for modern look */
            font-family: Arial;
        """)
        
        # Main layout with margins and spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        # Header
        header = QLabel("Retirement Application")
        header.setObjectName("header")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #ffffff;  /* White text for header */
        """)
        layout.addWidget(header)

        # Form layout for input fields
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setVerticalSpacing(10)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        # Personal Information
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Enter your first name")
        form_layout.addRow(QLabel("First Name:", styleSheet="color: #ffffff;"), self.first_name)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Enter your last name")
        form_layout.addRow(QLabel("Last Name:", styleSheet="color: #ffffff;"), self.last_name)

        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDisplayFormat("yyyy-MM-dd")
        self.dob.setDate(QDate.currentDate().addYears(-40))  # Default to ~40 years ago
        form_layout.addRow(QLabel("Date of Birth:", styleSheet="color: #ffffff;"), self.dob)

        self.ssn = QLineEdit()
        self.ssn.setPlaceholderText("XXX-XX-XXXX")
        form_layout.addRow(QLabel("Social Security Number:", styleSheet="color: #ffffff;"), self.ssn)

        self.address = QLineEdit()
        self.address.setPlaceholderText("Street Address")
        form_layout.addRow(QLabel("Address:", styleSheet="color: #ffffff;"), self.address)

        self.city = QLineEdit()
        self.city.setPlaceholderText("City")
        form_layout.addRow(QLabel("City:", styleSheet="color: #ffffff;"), self.city)

        self.state = QLineEdit()
        self.state.setPlaceholderText("State")
        form_layout.addRow(QLabel("State:", styleSheet="color: #ffffff;"), self.state)

        self.zip_code = QLineEdit()
        self.zip_code.setPlaceholderText("Zip Code")
        form_layout.addRow(QLabel("Zip Code:", styleSheet="color: #ffffff;"), self.zip_code)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone Number")
        form_layout.addRow(QLabel("Phone Number:", styleSheet="color: #ffffff;"), self.phone)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email Address")
        form_layout.addRow(QLabel("Email Address:", styleSheet="color: #ffffff;"), self.email)

        self.is_us_citizen = QCheckBox()
        form_layout.addRow(QLabel("U.S. Citizen:", styleSheet="color: #ffffff;"), self.is_us_citizen)

        # Employment Details
        self.agency = QLineEdit()
        self.agency.setPlaceholderText("e.g., Department of Defense")
        form_layout.addRow(QLabel("Agency:", styleSheet="color: #ffffff;"), self.agency)

        self.position_title = QLineEdit()
        self.position_title.setPlaceholderText("Position Title")
        form_layout.addRow(QLabel("Position Title:", styleSheet="color: #ffffff;"), self.position_title)

        self.hire_date = QDateEdit()
        self.hire_date.setCalendarPopup(True)
        self.hire_date.setDisplayFormat("yyyy-MM-dd")
        self.hire_date.setDate(QDate.currentDate().addYears(-20))  # Default to ~20 years ago
        form_layout.addRow(QLabel("Hire/Start Date:", styleSheet="color: #ffffff;"), self.hire_date)

        self.retirement_date = QDateEdit()
        self.retirement_date.setCalendarPopup(True)
        self.retirement_date.setDisplayFormat("yyyy-MM-dd")
        self.retirement_date.setDate(QDate.currentDate())  # Default to today
        form_layout.addRow(QLabel("Retirement Date:", styleSheet="color: #ffffff;"), self.retirement_date)

        self.years_service = QLineEdit()
        self.years_service.setReadOnly(True)  # Calculated field, not editable
        self.years_service.setPlaceholderText("Calculated automatically")
        self.years_service.setStyleSheet("""
            QLineEdit {
                background-color: #444444;
                color: #ffffff;
                padding: 8px;
                border: 2px solid #777777;
                border-radius: 6px;
                font-size: 14px;
            }
        """)
        form_layout.addRow(QLabel("Years of Service:", styleSheet="color: #ffffff;"), self.years_service)

        self.salary = QLineEdit()
        self.salary.setPlaceholderText("Enter high-3 average salary")
        form_layout.addRow(QLabel("High-3 Salary:", styleSheet="color: #ffffff;"), self.salary)

        # Benefits Elections
        self.survivor_benefit = QLineEdit()
        self.survivor_benefit.setPlaceholderText("e.g., Full, Partial, None")
        form_layout.addRow(QLabel("Survivor Benefit:", styleSheet="color: #ffffff;"), self.survivor_benefit)

        self.fehb_continue = QCheckBox()
        form_layout.addRow(QLabel("Continue FEHB (5+ years coverage):", styleSheet="color: #ffffff;"), self.fehb_continue)

        self.fegli_continue = QCheckBox()
        form_layout.addRow(QLabel("Continue FEGLI (5+ years coverage):", styleSheet="color: #ffffff;"), self.fegli_continue)

        self.bank_name = QLineEdit()
        self.bank_name.setPlaceholderText("Bank Name")
        form_layout.addRow(QLabel("Bank Name (Direct Deposit):", styleSheet="color: #ffffff;"), self.bank_name)

        self.account_number = QLineEdit()
        self.account_number.setPlaceholderText("Account Number")
        form_layout.addRow(QLabel("Account Number:", styleSheet="color: #ffffff;"), self.account_number)

        self.routing_number = QLineEdit()
        self.routing_number.setPlaceholderText("Routing Number")
        form_layout.addRow(QLabel("Routing Number:", styleSheet="color: #ffffff;"), self.routing_number)

        # Military Service
        self.served_military = QCheckBox()
        form_layout.addRow(QLabel("Served in Armed Forces:", styleSheet="color: #ffffff;"), self.served_military)

        self.military_retired_pay = QCheckBox()
        form_layout.addRow(QLabel("Receiving Military Retired Pay:", styleSheet="color: #ffffff;"), self.military_retired_pay)

        self.waived_military_pay = QCheckBox()
        form_layout.addRow(QLabel("Waived Military Pay for CSRS/FERS:", styleSheet="color: #ffffff;"), self.waived_military_pay)

        # Additional Information
        self.sick_leave_hours = QLineEdit()
        self.sick_leave_hours.setPlaceholderText("Unused Sick Leave Hours")
        form_layout.addRow(QLabel("Unused Sick Leave Hours:", styleSheet="color: #ffffff;"), self.sick_leave_hours)

        self.has_court_orders = QCheckBox()
        form_layout.addRow(QLabel("Court Orders for Former Spouses:", styleSheet="color: #ffffff;"), self.has_court_orders)

        layout.addLayout(form_layout)

        # Buttons with improved styling
        submit_btn = QPushButton("Submit Application")
        submit_btn.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 14px;
        """)
        submit_btn.clicked.connect(self.submit_application)
        layout.addWidget(submit_btn)

        upload_btn = QPushButton("Upload Document or Image")
        upload_btn.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 14px;
        """)
        upload_btn.clicked.connect(self.upload_form)
        layout.addWidget(upload_btn)

        layout.addStretch()

        # Updated stylesheet for text boxes and widgets to ensure visibility
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit { 
                padding: 8px; 
                border: 2px solid #777777; 
                border-radius: 6px; 
                color: white; 
                background-color: #444444;  /* Dark grey background */
                font-size: 14px;
                qproperty-alignment: AlignLeft;  /* Ensure text alignment */
            }
            QLineEdit::placeholder { 
                color: #AAAAAA;  /* Light grey for placeholder text */
                font-style: italic;
            }
            QDateEdit {
                padding: 8px;
                border: 2px solid #777777;
                border-radius: 6px;
                color: white;
                background-color: #444444;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                background-color: #2196F3;
                color: white;
                border: none;
            }
            QCheckBox { 
                color: #ffffff; 
                font-size: 14px;
            }
            QLabel { 
                color: #ffffff; 
                font-size: 14px;
            }
        """)

        # Connect date changes to update years of service
        self.hire_date.dateChanged.connect(self.calculate_years_service)
        self.retirement_date.dateChanged.connect(self.calculate_years_service)

    def calculate_years_service(self):
        hire_date = self.hire_date.date().toPyDate()
        retirement_date = self.retirement_date.date().toPyDate()
        if hire_date and retirement_date and retirement_date > hire_date:
            time_diff = retirement_date - hire_date
            years = time_diff.days / 365.25  # Approximate years, accounting for leap years
            self.years_service.setText(f"{years:.2f}")
        else:
            self.years_service.setText("")

    def submit_application(self):
        try:
            # Personal Information
            employee = Employee(
                self.first_name.text(), 
                self.last_name.text(), 
                self.dob.date().toString("yyyy-MM-dd"),
                self.ssn.text(),
                self.address.text(),
                self.city.text(),
                self.state.text(),
                self.zip_code.text(),
                self.phone.text(),
                self.email.text(),
                self.is_us_citizen.isChecked()
            )
            employee_id = employee.save()

            # Application Details
            years_service = float(self.years_service.text()) if self.years_service.text() else 0
            app = Application(
                employee_id,
                years_service,
                self.retirement_date.date().toString("yyyy-MM-dd"),
                float(self.salary.text()),
                self.agency.text(),
                self.position_title.text(),
                self.survivor_benefit.text(),
                self.fehb_continue.isChecked(),
                self.fegli_continue.isChecked(),
                self.bank_name.text(),
                self.account_number.text(),
                self.routing_number.text(),
                self.served_military.isChecked(),
                self.military_retired_pay.isChecked(),
                self.waived_military_pay.isChecked(),
                float(self.sick_leave_hours.text()) if self.sick_leave_hours.text() else 0,
                self.has_court_orders.isChecked()
            )
            app.save()
            QMessageBox.information(self, "Success", "Application submitted successfully!")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def upload_form(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Form", "", 
                                               "Files (*.png *.jpg *.jpeg *.pdf)")
        if file_name:
            text = extract_text_from_image(file_name)
            data = parse_ocr_text(text)
            self.first_name.setText(data.get('first_name', ''))
            self.last_name.setText(data.get('last_name', ''))
            self.dob.setDate(QDate.fromString(data.get('dob', ''), "yyyy-MM-dd") or QDate.currentDate().addYears(-40))
            self.ssn.setText(data.get('ssn', ''))
            self.address.setText(data.get('address', ''))  # Ensure address is correctly assigned
            self.city.setText(data.get('city', ''))
            self.state.setText(data.get('state', ''))
            self.zip_code.setText(data.get('zip_code', ''))
            self.phone.setText(data.get('phone', ''))
            self.email.setText(data.get('email', ''))  # Ensure email is correctly assigned
            self.is_us_citizen.setChecked(data.get('is_us_citizen', False))
            self.agency.setText(data.get('agency', ''))
            self.position_title.setText(data.get('position_title', ''))
            self.hire_date.setDate(QDate.fromString(data.get('hire_date', ''), "yyyy-MM-dd") or QDate.currentDate().addYears(-20))
            self.retirement_date.setDate(QDate.fromString(data.get('retirement_date', ''), "yyyy-MM-dd") or QDate.currentDate())
            salary = data.get('salary', '')
            self.salary.setText(str(salary) if salary != '' else '')
            self.survivor_benefit.setText(data.get('survivor_benefit', ''))
            self.fehb_continue.setChecked(data.get('fehb_continue', False))
            self.fegli_continue.setChecked(data.get('fegli_continue', False))
            self.bank_name.setText(data.get('bank_name', ''))
            self.account_number.setText(data.get('account_number', ''))
            self.routing_number.setText(data.get('routing_number', ''))
            self.served_military.setChecked(data.get('served_military', False))
            self.military_retired_pay.setChecked(data.get('military_retired_pay', False))
            self.waived_military_pay.setChecked(data.get('waived_military_pay', False))
            sick_leave_hours = data.get('sick_leave_hours', '')
            self.sick_leave_hours.setText(str(sick_leave_hours) if sick_leave_hours != '' else '')
            self.has_court_orders.setChecked(data.get('has_court_orders', False))
            self.calculate_years_service()
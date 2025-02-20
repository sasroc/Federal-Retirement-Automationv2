from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFormLayout
from PyQt6.QtCore import Qt
from models.employee import Employee
from models.application import Application
from utils.ocr_processor import extract_text_from_image, parse_ocr_text

class EmployeePortal(QWidget):
    def __init__(self):
        super().__init__()
        # Base stylesheet for the widget, ensuring a dark background for contrast
        self.setStyleSheet("background-color: #1e1e2f; font-family: Arial;")  # Darker background for modern look
        
        # Main layout with margins and spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        # Header
        header = QLabel("Retirement Application")
        header.setObjectName("header")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")  # White text for header
        layout.addWidget(header)

        # Form layout for input fields
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setVerticalSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Input fields with clear placeholders and ensured visibility
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Enter your first name")
        form_layout.addRow(QLabel("First Name:", styleSheet="color: #ffffff;"), self.first_name)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Enter your last name")
        form_layout.addRow(QLabel("Last Name:", styleSheet="color: #ffffff;"), self.last_name)

        self.dob = QLineEdit()
        self.dob.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow(QLabel("Date of Birth:", styleSheet="color: #ffffff;"), self.dob)

        self.years_service = QLineEdit()
        self.years_service.setPlaceholderText("Enter years of service")
        form_layout.addRow(QLabel("Years of Service:", styleSheet="color: #ffffff;"), self.years_service)

        self.retirement_date = QLineEdit()
        self.retirement_date.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow(QLabel("Retirement Date:", styleSheet="color: #ffffff;"), self.retirement_date)

        self.salary = QLineEdit()
        self.salary.setPlaceholderText("Enter high-3 average salary")
        form_layout.addRow(QLabel("High-3 Salary:", styleSheet="color: #ffffff;"), self.salary)

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

        upload_btn = QPushButton("Upload Paper Form")
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

        # Updated stylesheet for text boxes to ensure visibility
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit { 
                padding: 8px; 
                border: 2px solid #777777; 
                border-radius: 6px; 
                color: white; 
                background-color: #444444;  /* Dark grey background */
                font-size: 14px;
            }
            QLineEdit::placeholder { 
                color: #AAAAAA;  /* Light grey for placeholder text */
                font-style: italic;
            }
            QLabel { 
                color: #ffffff; 
                font-size: 14px;
            }
        """)

    def submit_application(self):
        try:
            employee = Employee(self.first_name.text(), self.last_name.text(), self.dob.text())
            employee_id = employee.save()  # Assuming save() returns the employee_id
            app = Application(employee_id, int(self.years_service.text()), 
                              self.retirement_date.text(), float(self.salary.text()))
            app.save()  # Assuming save() commits to DB
            QMessageBox.information(self, "Success", "Application submitted successfully!")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def upload_form(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Form", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            text = extract_text_from_image(file_name)
            data = parse_ocr_text(text)
            self.first_name.setText(data.get('first_name', ''))
            self.last_name.setText(data.get('last_name', ''))
            self.dob.setText(data.get('dob', ''))
            self.years_service.setText(data.get('years_service', ''))
            self.retirement_date.setText(data.get('retirement_date', ''))
            self.salary.setText(data.get('salary', ''))
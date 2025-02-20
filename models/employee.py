# models/employee.py
import sqlite3

class Employee:
    def __init__(self, first_name, last_name, dob, ssn=None, address=None, city=None, state=None, 
                 zip_code=None, phone=None, email=None, is_us_citizen=False):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.ssn = ssn
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.email = email
        self.is_us_citizen = is_us_citizen
        self.employee_id = None

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Employees (first_name, last_name, dob, ssn, address, city, state, zip_code, phone, email, is_us_citizen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.first_name, self.last_name, self.dob, self.ssn, self.address, self.city, 
              self.state, self.zip_code, self.phone, self.email, self.is_us_citizen))
        self.employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.employee_id
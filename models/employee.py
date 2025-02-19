import sqlite3

class Employee:
    def __init__(self, first_name, last_name, date_of_birth, address, city, state, zip_code, email, phone_number, ssn):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.email = email
        self.phone_number = phone_number
        self.ssn = ssn
        self.employee_id = None

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Employees (first_name, last_name, date_of_birth, address, city, state, zip_code, email, phone_number, ssn)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.first_name, self.last_name, self.date_of_birth, self.address, self.city, self.state, self.zip_code, self.email, self.phone_number, self.ssn))
        self.employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.employee_id
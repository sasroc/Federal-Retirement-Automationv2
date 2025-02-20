# models/employee.py
import sqlite3

class Employee:
    def __init__(self, first_name, last_name, dob):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Employees (first_name, last_name, dob) VALUES (?, ?, ?)',
                       (self.first_name, self.last_name, self.dob))
        employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return employee_id
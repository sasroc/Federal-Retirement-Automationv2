# models/application.py
import sqlite3

class Application:
    def __init__(self, employee_id, years_service, retirement_date, salary):
        self.employee_id = employee_id
        self.years_service = float(years_service)
        self.retirement_date = retirement_date
        self.salary = float(salary)

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Applications (employee_id, years_service, retirement_date, salary) VALUES (?, ?, ?, ?)',
                       (self.employee_id, self.years_service, self.retirement_date, self.salary))
        conn.commit()
        conn.close()
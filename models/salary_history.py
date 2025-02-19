import sqlite3

class SalaryHistory:
    def __init__(self, employee_id, effective_date, annual_salary):
        self.employee_id = employee_id
        self.effective_date = effective_date
        self.annual_salary = annual_salary

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO SalaryHistory (employee_id, effective_date, annual_salary)
            VALUES (?, ?, ?)
        ''', (self.employee_id, self.effective_date, self.annual_salary))
        conn.commit()
        conn.close()
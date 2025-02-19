import sqlite3

class LeaveBalances:
    def __init__(self, employee_id, annual_leave_hours, sick_leave_hours):
        self.employee_id = employee_id
        self.annual_leave_hours = annual_leave_hours
        self.sick_leave_hours = sick_leave_hours

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO LeaveBalances (employee_id, annual_leave_hours, sick_leave_hours)
            VALUES (?, ?, ?)
        ''', (self.employee_id, self.annual_leave_hours, self.sick_leave_hours))
        conn.commit()
        conn.close()
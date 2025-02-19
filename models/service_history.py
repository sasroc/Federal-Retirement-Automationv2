import sqlite3

class ServiceHistory:
    def __init__(self, employee_id, start_date, end_date, position, agency):
        self.employee_id = employee_id
        self.start_date = start_date
        self.end_date = end_date
        self.position = position
        self.agency = agency

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ServiceHistory (employee_id, start_date, end_date, position, agency)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.employee_id, self.start_date, self.end_date, self.position, self.agency))
        conn.commit()
        conn.close()
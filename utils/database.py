import sqlite3

def create_database():
    conn = sqlite3.connect('retirement.db')
    cursor = conn.cursor()
    
    # Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            email TEXT,
            phone_number TEXT,
            ssn TEXT NOT NULL
        )
    ''')
    
    # Service History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ServiceHistory (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            start_date TEXT NOT NULL,
            end_date TEXT,
            position TEXT,
            agency TEXT,
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        )
    ''')
    
    # Salary History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalaryHistory (
            salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            effective_date TEXT NOT NULL,
            annual_salary REAL NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        )
    ''')
    
    # Leave Balances table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LeaveBalances (
            leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            annual_leave_hours REAL NOT NULL,
            sick_leave_hours REAL NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
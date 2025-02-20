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
            dob TEXT NOT NULL,
            ssn TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            phone TEXT,
            email TEXT,
            is_us_citizen BOOLEAN
        )
    ''')
    
    # Applications table with hire_date
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            years_service REAL,
            retirement_date TEXT,
            salary REAL,
            agency TEXT,
            position_title TEXT,
            survivor_benefit TEXT,
            fehb_continue BOOLEAN,
            fegli_continue BOOLEAN,
            bank_name TEXT,
            account_number TEXT,
            routing_number TEXT,
            served_military BOOLEAN,
            military_retired_pay BOOLEAN,
            waived_military_pay BOOLEAN,
            sick_leave_hours REAL,
            has_court_orders BOOLEAN,
            submission_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted',
            benefits REAL,
            hire_date TEXT,
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        )
    ''')
    
    # Migration step: Add new columns if they don’t exist
    cursor.execute("PRAGMA table_info(Applications)")
    columns = [col[1] for col in cursor.fetchall()]
    new_columns = {
        'agency': 'TEXT',
        'position_title': 'TEXT',
        'survivor_benefit': 'TEXT',
        'fehb_continue': 'BOOLEAN',
        'fegli_continue': 'BOOLEAN',
        'bank_name': 'TEXT',
        'account_number': 'TEXT',
        'routing_number': 'TEXT',
        'served_military': 'BOOLEAN',
        'military_retired_pay': 'BOOLEAN',
        'waived_military_pay': 'BOOLEAN',
        'sick_leave_hours': 'REAL',
        'has_court_orders': 'BOOLEAN',
        'hire_date': 'TEXT'
    }
    for col, col_type in new_columns.items():
        if col not in columns:
            cursor.execute(f"ALTER TABLE Applications ADD COLUMN {col} {col_type}")
    
    conn.commit()
    conn.close()
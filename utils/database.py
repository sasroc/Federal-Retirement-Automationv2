import sqlite3

def create_database():
    conn = sqlite3.connect('retirement.db')
    cursor = conn.cursor()
    
    # Create Employees table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL
        )
    ''')
    
    # Create Applications table with the benefits column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            years_service REAL,
            retirement_date TEXT,
            salary REAL,
            submission_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted',
            benefits REAL,  -- Added benefits column
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        )
    ''')
    
    # Migration step: Add 'benefits' column if it doesn’t exist
    cursor.execute("PRAGMA table_info(Applications)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'benefits' not in columns:
        cursor.execute("ALTER TABLE Applications ADD COLUMN benefits REAL")
    
    conn.commit()
    conn.close()
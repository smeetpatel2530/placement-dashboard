
import sqlite3
import os

DB_PATH = 'placements.db'

def init_db():
    """Initialize database schema and handle migrations"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Create table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT,
            department TEXT,
            company TEXT,
            role TEXT,
            ctc_lpa REAL,
            ppo_type TEXT,
            ppo_type_raw TEXT,
            ppo_confirmed TEXT,
            stipend_pm REAL,
            date TEXT,
            batch_year INTEGER DEFAULT 2027
        )
    """)
    
    # Migration: Check for missing columns and add them
    existing_cols = [r[1] for r in conn.execute("PRAGMA table_info(students)").fetchall()]
    migrations = {
        "ppo_type_raw": "TEXT",
        "ppo_confirmed": "TEXT",
        "stipend_pm": "REAL",
        "batch_year": "INTEGER DEFAULT 2027"
    }
    
    for col, col_type in migrations.items():
        if col not in existing_cols:
            conn.execute(f"ALTER TABLE students ADD COLUMN {col} {col_type}")
            print(f"[DB] Migrated: added column '{col}'")

    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_students():
    """Fetch all students from database"""
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_students_filtered(department=None, company=None, min_ctc=None, max_ctc=None, ppo_type=None):
    conn = get_db()
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    
    if department and department != "All Departments":
        query += " AND department = ?"
        params.append(department)
    
    if company:
        query += " AND (company LIKE ? OR name LIKE ? OR role LIKE ?)"
        params.append(f"%{company}%")
        params.append(f"%{company}%")
        params.append(f"%{company}%")

    # If the user selects a specific type (FTE, PPO, Intern)
    if ppo_type and ppo_type != "All Types":
        query += " AND ppo_type = ?"
        params.append(ppo_type)
        
    if min_ctc is not None:
        query += " AND ctc_lpa >= ?"
        params.append(min_ctc)
        
    query += " ORDER BY ctc_lpa DESC NULLS LAST"
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Initialize database on import
init_db()
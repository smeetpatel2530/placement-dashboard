# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "placements.db"


# def get_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     conn = get_connection()
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS students (
#             id              INTEGER PRIMARY KEY AUTOINCREMENT,
#             name            TEXT,
#             roll_no         TEXT,
#             department      TEXT,
#             company         TEXT,
#             role            TEXT,
#             ppo_type        TEXT,
#             ppo_type_raw    TEXT,
#             ppo_confirmed   TEXT,
#             ctc_lpa         REAL,
#             stipend_pm      REAL,
#             date            TEXT,
#             batch_year      INTEGER DEFAULT 2027
#         )
#     """)

#     # ← Migrate existing DB that may be missing new columns
#     existing_cols = [r[1] for r in conn.execute("PRAGMA table_info(students)").fetchall()]
#     migrations = {
#         "batch_year":    "INTEGER DEFAULT 2027",
#         "ppo_type_raw":  "TEXT",
#         "ppo_confirmed": "TEXT",
#         "stipend_pm":    "REAL",
#     }
#     for col, col_type in migrations.items():
#         if col not in existing_cols:
#             conn.execute(f"ALTER TABLE students ADD COLUMN {col} {col_type}")
#             print(f"[DB] Migrated: added column '{col}'")

#     conn.commit()
#     conn.close()


# def clear_and_insert(records: list[dict]):
#     if not records:
#         print("[DB] WARNING: No records to insert!")
#         return

#     conn = get_connection()
#     conn.execute("DELETE FROM students")
#     conn.commit()

#     # Insert row by row for reliability (avoids pandas dtype issues)
#     inserted = 0
#     for r in records:
#         try:
#             conn.execute("""
#                 INSERT INTO students
#                     (name, roll_no, department, company, role,
#                      ppo_type, ppo_type_raw, ppo_confirmed,
#                      ctc_lpa, stipend_pm, date, batch_year)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 r.get("name"), r.get("roll_no"), r.get("department"),
#                 r.get("company"), r.get("role"), r.get("ppo_type"),
#                 r.get("ppo_type_raw"), r.get("ppo_confirmed"),
#                 r.get("ctc_lpa"), r.get("stipend_pm"),
#                 r.get("date"), r.get("batch_year", 2027),
#             ))
#             inserted += 1
#         except Exception as e:
#             print(f"[DB] Insert error for '{r.get('name')}': {e}")

#     conn.commit()
#     conn.close()
#     print(f"[DB] ✅ Inserted {inserted} records")


# def fetch_all_students() -> list[dict]:
#     conn = get_connection()
#     rows = conn.execute(
#         "SELECT * FROM students ORDER BY department, id"
#     ).fetchall()
#     conn.close()
#     return [dict(r) for r in rows]


# def fetch_students_filtered(
#     department=None, company=None,
#     min_ctc=None, max_ctc=None
# ) -> list[dict]:
#     query = "SELECT * FROM students WHERE 1=1"
#     params = []

#     if department:
#         query += " AND department = ?"
#         params.append(department)
#     if company:
#         query += " AND LOWER(company) LIKE ?"
#         params.append(f"%{company.lower()}%")
#     if min_ctc is not None:
#         query += " AND ctc_lpa >= ?"
#         params.append(min_ctc)
#     if max_ctc is not None:
#         query += " AND ctc_lpa <= ?"
#         params.append(max_ctc)

#     query += " ORDER BY ctc_lpa DESC NULLS LAST"

#     conn = get_connection()
#     rows = conn.execute(query, params).fetchall()
#     conn.close()
#     return [dict(r) for r in rows]

# import sqlite3
# import os

# DB_PATH = 'placements.db'

# def init_db():
#     """Initialize database schema"""
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
    
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS students (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             roll_no TEXT,
#             department TEXT,
#             company TEXT,
#             role TEXT,
#             ctc_lpa REAL,
#             ppo_type TEXT,
#             date TEXT,
#             batch_year INTEGER DEFAULT 2027
#         )
#     """)
    
#     conn.commit()
#     conn.close()

# def get_db():
#     """Get database connection"""
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn

# def fetch_all_students():
#     """Fetch all students from database"""
#     conn = get_db()
#     rows = conn.execute("SELECT * FROM students").fetchall()
#     conn.close()
#     return [dict(row) for row in rows]

# def fetch_students_filtered(department=None, company=None):
#     """Fetch students with optional filters"""
#     conn = get_db()
#     query = "SELECT * FROM students WHERE 1=1"
#     params = []
    
#     if department:
#         query += " AND department = ?"
#         params.append(department)
    
#     if company:
#         query += " AND company = ?"
#         params.append(company)
    
#     rows = conn.execute(query, params).fetchall()
#     conn.close()
#     return [dict(row) for row in rows]

# # Initialize database on import
# init_db()


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

def fetch_students_filtered(department=None, company=None, min_ctc=None, max_ctc=None):
    """
    Fetch students with filtering logic. 
    Accepts 4 arguments to match the API route in main.py
    """
    conn = get_db()
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    
    if department:
        query += " AND department = ?"
        params.append(department)
    
    if company:
        # Using LIKE to allow partial search (e.g., 'Micro' matches 'Micron')
        query += " AND company LIKE ?"
        params.append(f"%{company}%")
        
    if min_ctc is not None:
        query += " AND ctc_lpa >= ?"
        params.append(min_ctc)
        
    if max_ctc is not None:
        query += " AND ctc_lpa <= ?"
        params.append(max_ctc)
    
    # Add sorting so the best packages appear first
    query += " ORDER BY ctc_lpa DESC NULLS LAST"
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Initialize database on import
init_db()
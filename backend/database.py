import json
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "placements.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            roll_no     TEXT,
            department  TEXT,
            company     TEXT,
            role        TEXT,
            ppo_type    TEXT,
            ppo_type_raw TEXT, 
            ppo_confirmed TEXT,
            ctc_lpa     REAL,
            stipend_pm  REAL,
            date        TEXT,
            batch_year   INTEGER DEFAULT 2027
        )
    """)
    conn.commit()
    conn.close()

def clear_and_insert(records: list[dict]):
    conn = get_connection()
    conn.execute("DELETE FROM students")
    if records:
        df = pd.DataFrame(records)
        df.to_sql("students", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

def fetch_all_students() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY department, id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def fetch_students_filtered(department=None, company=None, min_ctc=None, max_ctc=None) -> list[dict]:
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    if department:
        query += " AND department = ?"
        params.append(department)
    if company:
        query += " AND LOWER(company) LIKE ?"
        params.append(f"%{company.lower()}%")
    if min_ctc is not None:
        query += " AND ctc_lpa >= ?"
        params.append(min_ctc)
    if max_ctc is not None:
        query += " AND ctc_lpa <= ?"
        params.append(max_ctc)
    query += " ORDER BY ctc_lpa DESC"
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]
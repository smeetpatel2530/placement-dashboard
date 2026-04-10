import sqlite3
import os

DB_PATH = "placements.db"


def init_db():
    """Initialize database schema and handle migrations"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

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


def _normalize_student_row(row):
    """Return frontend-friendly student shape"""
    data = dict(row)
    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "roll_no": data.get("roll_no"),
        "department": data.get("department"),
        "company": data.get("company"),
        "role": data.get("role"),
        "ctc_lpa": data.get("ctc_lpa"),
        "stipend_pm": data.get("stipend_pm"),
        "ppo_type": data.get("ppo_type"),
        "ppo_type_raw": data.get("ppo_type_raw"),
        "type": data.get("ppo_type_raw") or data.get("ppo_type") or "",
        "date": data.get("date"),
        "batch_year": data.get("batch_year"),
    }


def fetch_all_students():
    """Fetch all students from database"""
    conn = get_db()
    rows = conn.execute("""
        SELECT *
        FROM students
        ORDER BY
            CASE WHEN date IS NULL OR TRIM(date) = '' THEN 1 ELSE 0 END,
            date DESC,
            ctc_lpa DESC
    """).fetchall()
    conn.close()
    return [_normalize_student_row(row) for row in rows]


def fetch_students_filtered(
    department=None,
    search=None,
    min_ctc=None,
    max_ctc=None,
    type_filter=None
):
    """
    Filter students by department, search, ctc range, and raw type.
    type_filter uses ppo_type_raw for exact raw Excel-based filtering.
    """
    conn = get_db()
    query = """
        SELECT *
        FROM students
        WHERE 1=1
    """
    params = []

    if department and department not in ["All", "All Departments"]:
        query += " AND department = ?"
        params.append(department)

    if search:
        query += " AND (name LIKE ? OR company LIKE ? OR role LIKE ?)"
        search_value = f"%{search}%"
        params.extend([search_value, search_value, search_value])

    if type_filter and type_filter not in ["All", "All Types"]:
        query += " AND COALESCE(ppo_type_raw, ppo_type, '') = ?"
        params.append(type_filter)

    if min_ctc is not None:
        query += " AND ctc_lpa >= ?"
        params.append(min_ctc)

    if max_ctc is not None:
        query += " AND ctc_lpa <= ?"
        params.append(max_ctc)

    query += """
        ORDER BY
            CASE WHEN date IS NULL OR TRIM(date) = '' THEN 1 ELSE 0 END,
            date DESC,
            ctc_lpa DESC
    """

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [_normalize_student_row(row) for row in rows]


def fetch_distinct_types():
    """Fetch distinct raw types for dynamic frontend filter"""
    conn = get_db()
    rows = conn.execute("""
        SELECT DISTINCT COALESCE(ppo_type_raw, ppo_type, '') AS type_value
        FROM students
        WHERE TRIM(COALESCE(ppo_type_raw, ppo_type, '')) != ''
        ORDER BY type_value ASC
    """).fetchall()
    conn.close()
    return [row["type_value"] for row in rows]


# Initialize database on import
init_db()
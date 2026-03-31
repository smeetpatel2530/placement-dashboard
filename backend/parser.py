import pandas as pd
import re
from pathlib import Path
from database import clear_and_insert, init_db
import os

EXCEL_PATH = os.environ.get("EXCEL_PATH", "data/placements.xlsx")

def load_excel():
    if not os.path.exists(EXCEL_PATH):
        print(f"[Warning] Excel file not found at {EXCEL_PATH}. Starting with empty data.")
        return
# Map each sheet to a department label
SHEET_MAP = {
    "DSC": "DSC",
    "SWE": "SWE",
    "CSE": "CSE",
    "ITY": "ITY",
    "AFI": "AFI",
    "Research": "Research",
}

# Normalized column names (handles slight header variations across sheets)
COL_NAME       = ["NAME", "Name"]
COL_ROLL       = ["ROLL NO", "Roll No", "ROLL_NO"]
COL_COMPANY    = ["COMPANY", "Company"]
COL_ROLE       = ["ROLE", "Role"]
COL_PPO_TYPE   = ["PPO / INTERN", "PPO/INTERN", "PPO_INTERN"]
COL_PPO_STATUS = ["PPO Status", "PPO Confirmation Status", "PPO_Status"]
COL_CTC        = ["CTC (LPA)", "CTC(LPA)", "CTC"]
COL_STIPEND    = ["Stipend (PM)", "Stipend(PM)", "Stipend (k PM)", "STIPEND"]
COL_DATE       = ["Date", "DATE"]


def _pick_col(df_cols, candidates):
    for c in candidates:
        if c in df_cols:
            return c
    return None


def _safe_float(val):
    if val is None or val == "" or str(val).strip() in ["-", "–", "—", "NA", "na"]:
        return None
    try:
        return float(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def parse_excel(filepath: str) -> list[dict]:
    init_db()
    records = []
    xf = pd.ExcelFile(filepath, engine="openpyxl")

    for sheet_name in xf.sheet_names:
        dept = SHEET_MAP.get(sheet_name)
        if not dept:
            continue

        df = xf.parse(sheet_name, header=None)

        # Find the actual header row (row containing "NAME")
        header_row_idx = None
        for i, row in df.iterrows():
            row_vals = [str(v).strip() for v in row.values]
            if "NAME" in row_vals or "Name" in row_vals:
                header_row_idx = i
                break

        if header_row_idx is None:
            continue

        # Re-read with correct header
        df = xf.parse(sheet_name, header=header_row_idx, engine="openpyxl")
        df.columns = [str(c).strip() for c in df.columns]

        col_name       = _pick_col(df.columns, COL_NAME)
        col_roll       = _pick_col(df.columns, COL_ROLL)
        col_company    = _pick_col(df.columns, COL_COMPANY)
        col_role       = _pick_col(df.columns, COL_ROLE)
        col_ppo_type   = _pick_col(df.columns, COL_PPO_TYPE)
        col_ppo_status = _pick_col(df.columns, COL_PPO_STATUS)
        col_ctc        = _pick_col(df.columns, COL_CTC)
        col_stipend    = _pick_col(df.columns, COL_STIPEND)
        col_date       = _pick_col(df.columns, COL_DATE)

        for _, row in df.iterrows():
            name_val = str(row[col_name]).strip() if col_name else ""

            # Skip empty rows, summary rows, and header repetitions
            if not name_val or name_val in ["nan", "NAME", "Name", "Total", "TOTAL"]:
                continue
            # Skip rows where name looks like a number (COUNT column bled in)
            if re.match(r"^\d+$", name_val):
                continue

            record = {
                "name":          name_val,
                "roll_no":       str(row[col_roll]).strip() if col_roll and str(row[col_roll]) != "nan" else None,
                "department":    dept,
                "company":       str(row[col_company]).strip() if col_company and str(row[col_company]) != "nan" else "Unknown",
                "role":          str(row[col_role]).strip() if col_role and str(row[col_role]) != "nan" else None,
                "ppo_type":      str(row[col_ppo_type]).strip() if col_ppo_type and str(row[col_ppo_type]) != "nan" else None,
                "ppo_confirmed": str(row[col_ppo_status]).strip() if col_ppo_status and str(row[col_ppo_status]) != "nan" else None,
                "ctc_lpa":       _safe_float(row[col_ctc]) if col_ctc else None,
                "stipend_pm":    _safe_float(row[col_stipend]) if col_stipend else None,
                "date":          str(row[col_date]).strip() if col_date and str(row[col_date]) != "nan" else None,
            }
            records.append(record)

    clear_and_insert(records)
    print(f"[Parser] Loaded {len(records)} students from Excel.")
    return records